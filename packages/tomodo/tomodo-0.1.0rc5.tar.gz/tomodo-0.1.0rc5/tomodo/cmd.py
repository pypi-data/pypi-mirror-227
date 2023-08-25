import logging
from typing import Dict

import typer
from rich.console import Console
from rich.logging import RichHandler

from tomodo.common.config import Config
from tomodo.common.upgrader import Upgrader
from tomodo.common.util import parse_2d_separated_string, parse_semver

console = Console()

cli = typer.Typer()

logging.basicConfig(
    level=logging.INFO, format="%(message)s", datefmt="%d/%m/%Y %H:%M:%S.%f %z", handlers=[RichHandler()]
)

logger = logging.getLogger("rich")

UPGRADE_VERSION_PATH = {
    "3.6": "4.0",
    "4.0": "4.2",
    "4.2": "4.4",
    "4.4": "5.0",
    "5.0": "6.0",
    "6.0": "7.0",
}


@cli.command(
    help="Upgrade a standalone MongoDB instance or a MongoDB Replica Set to a target version.",
    no_args_is_help=True)
def upgrade(
        hostname: str = typer.Option(help="The MongoDB connection string to the replica set or standalone instance"),
        target_version: str = typer.Option(help="The target MongoDB version to upgrade to"),
        standalone: bool = typer.Option(default=False,
                                        help="Use it the target instance is a standalone instance (not a replica set)"),
        image_registry_name: str = typer.Option(
            default="mongo",
            help="Image registry name to use. Omit to pull the default 'mongo:tag' repo"
        ),
        container_creation_retries: int = typer.Option(
            default=5,
            help="How many times the container creation should be retried"
        ),
        container_creation_delay: int = typer.Option(
            default=5,
            help="# of seconds to wait between each failed container creation"
        ),
        mongodb_operation_retries: int = typer.Option(
            default=5,
            help="How many times any MongoDB operation should be retried"
        ),
        mongodb_operation_delay: int = typer.Option(
            default=5,
            help="# of seconds to wait between each failed MongoDB operation"
        ),
        image_tag_mapping: str = typer.Option(
            default=None,
            help="Override the default image tags. (ex. '4.0=4.0-custom,4.2=4.2-custom')",
        ),
        username: str = typer.Option(
            default=None,
            help="MongoDB username",
        ),
        password: str = typer.Option(
            default=None,
            help="MongoDB password",
        )
):
    config = Config(
        target_version=target_version,
        hostname=hostname,
        image_registry_name=image_registry_name,
        standalone=standalone,
        container_creation_retries=container_creation_retries,
        container_creation_delay=container_creation_delay,
        mongodb_operation_retries=mongodb_operation_retries,
        mongodb_operation_delay=mongodb_operation_delay,
        image_tag_mapping=parse_2d_separated_string(image_tag_mapping)
    )

    upgrader = Upgrader(config=config)

    target_maj, target_min, _ = parse_semver(target_version)
    target_min = f"{target_maj}.{target_min}"
    current_version = upgrader.get_mongodb_version()
    current_maj, current_min, current_patch = parse_semver(current_version)
    current_min = f"{current_maj}.{current_min}"
    logger.info(f"This will upgrade {hostname} from {current_min} to {target_min}")

    upgrade_path = []
    append = False
    for v_from, v_to in UPGRADE_VERSION_PATH.items():
        if target_min == v_to:
            upgrade_path.append(target_version)
            break
        if v_from == current_min:
            append = True
        if append:
            upgrade_path.append(v_to)
    logger.info(f"The upgrade path is {current_version} --> {' --> '.join(upgrade_path)}.")
    logger.info(f"This means that {len(upgrade_path)} upgrades will be performed serially.")
    for next_version in upgrade_path:
        if not standalone:
            logger.info(f"Now upgrading replica set from version {current_version} to {next_version}")
            upgrader.upgrade_replica_set(target_version=next_version)
            logger.info(f"Upgraded to {next_version} successfully.")
            current_version = upgrader.get_mongodb_version()
        else:
            # TODO: implement standalone (non-rs) upgrade
            logger.error("Standalone upgrades aren't supported yet")


@cli.command(
    help="Print an upgrade plan for a standalone MongoDB instance or a MongoDB Replica Set to a target version.",
    no_args_is_help=True)
def explain(
        hostname: str = typer.Option(help="The MongoDB connection string to the replica set or standalone instance"),
        target_version: str = typer.Option(default="6.0", help="The target MongoDB version to upgrade to"),
        standalone: bool = typer.Option(default=False,
                                        help="Use it the target instance is a standalone instance (not a replica set)"),
        docker_host: str = typer.Option(default="local",
                                        help="Set a docker daemon hostname different from the local daemon")
):
    raise NotImplementedError("Explain is not implemented")


def run():
    cli()


if __name__ == "__main__":
    run()
