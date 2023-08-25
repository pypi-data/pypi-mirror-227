import logging
from io import StringIO
from time import sleep
from typing import Dict, List, Callable

import docker
from docker.models.containers import Container
from pymongo import MongoClient
from pymongo.errors import AutoReconnect
from rich.console import Console
from rich.table import Table

from tomodo.common.config import Config
from tomodo.common.util import parse_semver, with_retry

io = StringIO()

console = Console(file=io)
logger = logging.getLogger("rich")


def get_primary(members: List) -> Dict:
    for m in members:
        state_str: str = m.get("stateStr")
        if state_str == "PRIMARY":
            return m
    raise Exception("Primary node could not be found")


def get_rs_members_table(members: any, title: str = "Replica Set Members") -> str:
    io.truncate(0)
    console.file.truncate(0)
    table = Table(title=title)
    table.add_column("Name")
    table.add_column("State")
    table.add_column("Health")
    table.add_column("Uptime")
    for m in members:
        table.add_row(m.get("name"), m.get("stateStr"), str(m.get("health")), str(m.get("uptime")))
    console.print(table)
    output = console.file.getvalue()
    return output


class Upgrader:

    def __init__(self, config: Config):
        self.config = config
        # The retry decorators need to read configurations dynamically, thus
        # wrapping their wrapped methods in the code and not with the '@decorator' notation
        self.init_decorators(config)

    @classmethod
    def init_decorators(cls, config: Config):
        setattr(cls, "get_mongodb_version", cls._mongodb_retry_decorator(config, cls.get_mongodb_version))
        setattr(cls, "list_rs_members", cls._mongodb_retry_decorator(config, cls.list_rs_members))
        setattr(cls, "set_fcv", cls._mongodb_retry_decorator(config, cls.set_fcv))
        setattr(cls, "step_down_primary", cls._mongodb_retry_decorator(config, cls.step_down_primary))
        setattr(cls, "get_deployment_containers", cls._container_retry_decorator(config, cls.get_deployment_containers))
        setattr(cls, "upgrade_container", cls._container_retry_decorator(config, cls.upgrade_container))

    @classmethod
    def _container_retry_decorator(cls, config: Config, func: Callable) -> Callable:
        return with_retry(
            max_attempts=config.container_creation_retries,
            delay=config.container_creation_delay,
            retryable_exc=(Exception,)
        )(func)

    @classmethod
    def _mongodb_retry_decorator(cls, config: Config, func: Callable) -> Callable:
        return with_retry(
            max_attempts=config.mongodb_operation_retries,
            delay=config.mongodb_operation_delay,
            retryable_exc=(AutoReconnect, Exception)
        )(func)

    def get_mongodb_version(self):
        mongo_client = MongoClient(self.config.hostname)
        server_version = mongo_client.server_info().get("version")
        return server_version

    def list_rs_members(self, replica_set_host: str):
        mongo_client = MongoClient(replica_set_host)
        rs_status = mongo_client.admin.command("replSetGetStatus")
        return rs_status.get("members")

    def set_fcv(self, member_name: str, target_version: str):
        mongo_client = MongoClient(f"mongodb://{member_name}/")
        target_fcv = target_version
        if len(target_version.split(".")) > 2:
            target_fcv = ".".join(target_version.split(".")[:-1])
        tmj, _, _ = parse_semver(target_version)
        if int(tmj) == 7:
            mongo_client.admin.command("setFeatureCompatibilityVersion", target_fcv, confirm=True)
        else:
            mongo_client.admin.command("setFeatureCompatibilityVersion", target_fcv)
        sleep(1)
        logger.info(f"{member_name} is now configured with FCV {target_fcv}")

    def step_down_primary(self, member_name: str):
        logger.info(f"Stepping down {member_name}")
        mongo_client = MongoClient(f"mongodb://{member_name}/")
        timeout = 5
        try:
            mongo_client.admin.command("replSetStepDown", 10)
        except AutoReconnect:
            pass
        sleep(timeout)
        return True

    def get_deployment_containers(self, container_search_term: str):
        docker_client = docker.from_env()
        containers = []
        for container in docker_client.containers.list():
            if container_search_term.lower() in container.attrs.get("Name").lower():
                containers.append(container)
        return containers

    def upgrade_container(self, old_container: Container, target_version) -> (str, str):
        # TODO: Add image tag mapping
        # TODO: Derive image name dynamically in outer container
        # TODO: Add environment variables
        docker_client = docker.from_env()
        image_tag = target_version
        if self.config.image_tag_mapping:
            if target_version in self.config.image_tag_mapping:
                image_tag = self.config.image_tag_mapping.get(target_version)
            else:
                [maj_v, min_v, _] = parse_semver(target_version)
                maj_min = f"{maj_v}.{min_v}"
                if maj_min in self.config.image_tag_mapping:
                    image_tag = self.config.image_tag_mapping.get(maj_min)

        networks: Dict = old_container.attrs.get("NetworkSettings", {}).get("Networks")
        network_name = None
        if networks:
            network_name = list(networks.keys())[0]
        docker_client.containers.get(old_container.id).rename(f"{old_container.name}-{target_version}-old")
        ports = old_container.attrs.get("HostConfig", {}).get("PortBindings")
        container_id = old_container.id
        command = [old_container.attrs.get("Path"), *old_container.attrs.get("Args")]

        # environment_vars_lst: List = old_container.attrs.get("Config", {}).get("Env")
        # environment_vars = {
        #     a: "" for a in environment_vars_lst
        # }
        if "--storageEngine" not in command:
            command = [*command, "--storageEngine", "wiredTiger"]
        name = old_container.name
        old_container.stop()
        new_container = docker_client.containers.run(
            image=f"{self.config.image_registry_name}:{image_tag}",
            detach=True,
            volumes_from=[container_id],
            ports=ports,
            command=command,
            name=name,
            network=network_name or None,
            # environment={}
        )
        old_container.remove()
        return new_container.short_id, new_container.attrs.get("Config", {}).get("Image")

    def upgrade(self, member_name: str, target_version: str) -> (str, str):
        container_name = member_name.split(":")[0]
        containers = self.get_deployment_containers(container_name)
        if len(containers) != 1:
            raise Exception(f"Could not find exactly one container under the name '{container_name}'")
        container: Container = containers[0]
        return self.upgrade_container(old_container=container, target_version=target_version)

    def upgrade_replica_set(self, target_version: str = "4.0"):
        logger.info("Starting a rolling restart")
        members = self.list_rs_members(self.config.hostname)
        logger.info(get_rs_members_table(members))
        primary = None
        secondaries = []
        for m in members:
            state_str: str = m.get("stateStr")
            if state_str == "PRIMARY":
                primary = {**m, "upgraded": False}
            elif state_str == "SECONDARY":
                secondaries.append({**m, "upgraded": False})
            else:
                logger.info(f"{m.get('name')} is unhealthy; state: {state_str}")
        if not primary:
            logger.info("No primary in the replica set!")
        members_state = [primary, *secondaries]

        for m in [*members_state]:
            member_name = m.get("name")

            current_primary = get_primary(members)
            if len(members_state) == 1:
                logger.info("Single-node Replica Set: no need to ask the primary to step down")
            elif current_primary.get("name") != member_name:
                logger.info("Not a primary; no need to step down")
            else:
                self.step_down_primary(member_name)
            container_id, tag = self.upgrade(member_name=member_name, target_version=target_version)
            logger.info(f"New container ID: {container_id} with image tag {tag}")
            members = self.list_rs_members(self.config.hostname)
            logger.info(get_rs_members_table(members, title="Current RS state"))

        logger.info("All member containers were upgraded successfully")
        logger.info("Setting FCV for each member")
        for m in members:
            sleep(5)
            self.set_fcv(member_name=m.get("name"), target_version=target_version)
