from typing import Dict

from ruamel.yaml import YAML, yaml_object

yaml = YAML()


@yaml_object(yaml)
class Config:
    def __init__(
            self,
            target_version: str,
            hostname: str,
            image_registry_name: str = "mongo",
            standalone: bool = False,
            container_creation_retries: int = 5,
            container_creation_delay: int = 5,
            mongodb_operation_retries: int = 5,
            mongodb_operation_delay: int = 5,
            image_tag_mapping: Dict | None = None
    ):
        self.target_version = target_version
        self.standalone = standalone
        self.hostname = hostname
        self.image_registry_name = image_registry_name
        self.container_creation_retries = container_creation_retries
        self.container_creation_delay = container_creation_delay
        self.mongodb_operation_retries = mongodb_operation_retries
        self.mongodb_operation_delay = mongodb_operation_delay
        self.image_tag_mapping = image_tag_mapping


def from_file(file_path: str):
    # TODO: make configurable with YAML?
    pass
