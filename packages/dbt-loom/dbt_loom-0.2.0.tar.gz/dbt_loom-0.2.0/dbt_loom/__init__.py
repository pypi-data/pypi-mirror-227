import json
import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


import yaml
from dbt.contracts.graph.node_args import ModelNodeArgs
from dbt.plugins.manager import dbt_hook, dbtPlugin
from dbt.plugins.manifest import PluginNodes
from networkx import DiGraph
from pydantic import BaseModel

from .clients.dbt_cloud import DbtCloud


class ManifestReferenceType(str, Enum):
    """Type of ManifestReference"""

    file = "file"
    dbt_cloud = "dbt_cloud"


class FileReferenceConfig(BaseModel):
    """Configuration for a file reference"""

    path: Path


class DbtCloudReferenceConfig(BaseModel):
    """Configuration for a dbt Cloud reference."""

    account_id: int
    job_id: int
    api_endpoint: Optional[str] = None
    step: Optional[int] = None


class ManifestReference(BaseModel):
    """Reference information for a manifest to be loaded into dbt-loom."""

    name: str
    type: ManifestReferenceType
    config: Union[FileReferenceConfig, DbtCloudReferenceConfig]


class dbtLoomConfig(BaseModel):
    """Configuration for dbt Loom"""

    manifests: List[ManifestReference]


class LoomConfigurationError(BaseException):
    """Error raised when dbt-loom has been misconfigured."""


class ManifestLoader:
    def __init__(self):
        self.loading_functions = {
            ManifestReferenceType.file: self.load_from_local_filesystem,
            ManifestReferenceType.dbt_cloud: self.load_from_dbt_cloud,
        }

    @staticmethod
    def load_from_local_filesystem(config: FileReferenceConfig) -> Dict:
        """Load a manifest dictionary from a local file"""
        if not config.path.exists():
            raise LoomConfigurationError(f"The path `{config.path}` does not exist.")

        return json.load(open(config.path))

    @staticmethod
    def load_from_dbt_cloud(config: DbtCloudReferenceConfig) -> Dict:
        """Load a manifest dictionary from dbt Cloud."""
        client = DbtCloud(
            account_id=config.account_id, api_endpoint=config.api_endpoint
        )

        return client.get_models(config.job_id, step=config.step)

    def load(self, manifest_reference: ManifestReference) -> Dict:
        """Load a manifest dictionary based on a ManifestReference input."""

        if manifest_reference.type not in self.loading_functions:
            raise LoomConfigurationError(
                f"The manifest reference provided for {manifest_reference.name} does "
                "not have a valid type."
            )

        return self.loading_functions[manifest_reference.type](
            manifest_reference.config
        )


def identify_public_node_subgraph(manifest) -> Dict[str, Any]:
    """
    Identify all nodes that are ancestors of public nodes, and the public nodes
    themselves.
    """
    graph: DiGraph = DiGraph()
    public_nodes = set()
    selected_node_ids = set()

    for unique_id, node in manifest["nodes"].items():
        graph.add_edges_from(
            [
                (parent, unique_id)
                for parent in node.get("depends_on", {"nodes": []}).get("nodes", [])
                if parent.startswith("model")
            ]
        )

        if node.get("access", "protected") == "public":
            public_nodes.add(unique_id)
    selected_node_ids.update(public_nodes)

    return {
        unique_id: manifest.get("nodes", {}).get(unique_id)
        for unique_id in selected_node_ids
    }


def convert_model_nodes_to_model_node_args(
    selected_nodes: Dict[str, Any]
) -> Dict[str, ModelNodeArgs]:
    """Generate a dictionary of ModelNodeArgs based on a dictionary of ModelNodes"""
    return {
        unique_id: ModelNodeArgs(
            name=node.get("name"),
            package_name=node.get("package_name"),
            identifier=node.get("relation_name").split(".")[-1].replace('"', ""),
            schema=node.get("schema"),
            database=node.get("database"),
            relation_name=node.get("relation_name"),
            version=node.get("version"),
            latest_version=node.get("latest_version"),
            deprecation_date=node.get("deprecation_date"),
            access=node.get("access", "public"),
            generated_at=node.get("created_at"),
            depends_on_nodes=list(),
            enabled=node["config"].get("enabled"),
        )
        for unique_id, node in selected_nodes.items()
        if node is not None
    }


class dbtLoom(dbtPlugin):
    """
    dbtLoom is a dbt plugin that loads manifest files, parses a DAG from the manifest,
    and injects public nodes from imported manifest.
    """

    def __init__(self, project_name: str):
        configuration_path = Path(
            os.environ.get("DBT_LOOM_CONFIG", "dbt_loom.config.yml")
        )

        self._manifest_loader = ManifestLoader()

        self.config: Optional[dbtLoomConfig] = self.read_config(configuration_path)
        self.models: Dict[str, ModelNodeArgs] = {}

        super().__init__(project_name)

    def read_config(self, path: Path) -> Optional[dbtLoomConfig]:
        """Read the dbt-loom configuration file."""
        if not path.exists():
            return None

        return dbtLoomConfig(**yaml.load(open(path), yaml.SafeLoader))

    def initialize(self) -> None:
        """Initialize the plugin"""

        print("Initializing dbt-loom")

        if self.models != {} or not self.config:
            return

        print(self.config.manifests)

        for manifest_reference in self.config.manifests:
            manifest = self._manifest_loader.load(manifest_reference)
            if manifest is None:
                continue

            selected_nodes = identify_public_node_subgraph(manifest)
            self.models.update(convert_model_nodes_to_model_node_args(selected_nodes))

        for key, value in self.models.items():
            print(key, value)

    @dbt_hook
    def get_nodes(self) -> PluginNodes:
        """
        Inject PluginNodes to dbt for injection into dbt's DAG.
        """
        print("injecting nodes")
        return PluginNodes(models=self.models)


plugins = [dbtLoom]
