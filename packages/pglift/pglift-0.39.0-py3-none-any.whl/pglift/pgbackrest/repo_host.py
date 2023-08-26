import configparser
import logging
from collections.abc import Iterator
from pathlib import Path
from typing import ClassVar, Optional, Union

import pgtoolkit.conf as pgconf

from .. import cmd, exceptions, hookimpl
from .. import service as service_mod
from .. import systemd, util
from ..ctx import Context
from ..models import interface, system
from ..settings import PgBackRestSettings, Settings
from . import base, models
from . import register_if as base_register_if
from .base import get_settings, parser

HostRepository = PgBackRestSettings.HostRepository
logger = logging.getLogger(__name__)


def register_if(settings: Settings) -> bool:
    if not base_register_if(settings):
        return False
    s = get_settings(settings)
    return isinstance(s.repository, HostRepository)


@hookimpl
def site_configure_install(settings: Settings) -> None:
    s = get_settings(settings)
    logger.info("installing pgbackrest server configuration")
    srv_configpath = server_configpath(s)
    srv_configpath.parent.mkdir(parents=True, exist_ok=True)
    config = server_config(s)
    with srv_configpath.open("w") as f:
        config.write(f)

    logger.info("installing base pgbackrest configuration")
    global_configpath = base.base_configpath(s)
    global_configpath.parent.mkdir(parents=True, exist_ok=True)
    config = base_config(s)
    with global_configpath.open("w") as f:
        config.write(f)
    base.create_include_directory(s)

    # Also create the log directory here, redundantly with __init__.py,
    # because it's needed when starting the server and we cannot rely on
    # __init__.py hook call as it would happen too late.
    s.logpath.mkdir(exist_ok=True, parents=True)

    srv = Server(s)
    logger.info("starting %s", srv)
    ctx = Context(settings=settings)
    service_mod.start(ctx, srv, foreground=False)
    logger.debug("pinging %s", srv)
    cmd.run(srv.ping_cmd(), check=True)


@hookimpl
def site_configure_uninstall(settings: Settings) -> None:
    s = get_settings(settings)
    srv = Server(s)
    logger.info("stopping %s", srv)
    ctx = Context(settings=settings)
    service_mod.stop(ctx, srv)

    logger.info("uninstalling pgbackrest server configuration")
    server_configpath(s).unlink(missing_ok=True)
    base.delete_include_directory(s)
    logger.info("uninstalling base pgbackrest configuration")
    base.base_configpath(s).unlink(missing_ok=True)


@hookimpl
def site_configure_uninstalled(settings: Settings) -> None:
    s = get_settings(settings)
    for f in (server_configpath(s), base.config_directory(s), base.base_configpath(s)):
        if not f.exists():
            raise exceptions.InstallationError(
                f"pgBackRest configuration path {f} missing"
            )


SYSTEMD_SERVICE_NAME = "pglift-pgbackrest.service"


@hookimpl
def systemd_unit_templates(
    settings: "Settings", content: bool
) -> Union[Iterator[str], Iterator[tuple[str, str]]]:
    if not content:
        yield SYSTEMD_SERVICE_NAME
        return
    s = get_settings(settings)
    yield SYSTEMD_SERVICE_NAME, systemd.template(SYSTEMD_SERVICE_NAME).format(
        executeas=systemd.executeas(settings),
        configpath=server_configpath(s),
        execpath=s.execpath,
    )


@hookimpl
def instance_configured(
    ctx: "Context",
    manifest: interface.Instance,
    config: pgconf.Configuration,
    upgrading_from: Optional[system.Instance],
) -> None:
    instance = system.PostgreSQLInstance.system_lookup(
        (manifest.name, manifest.version, ctx.settings)
    )

    settings = get_settings(ctx.settings)
    service_manifest = manifest.service_manifest(models.ServiceManifest)
    service = base.service(instance, service_manifest, settings, upgrading_from)
    base.setup(ctx, service, settings, config, instance.datadir)

    srv = Server(settings)
    logger.debug("pinging pgBackRest remote repository %s", srv)
    r = cmd.run(srv.ping_cmd())
    if r.returncode != 0:
        logger.warning("pgBackRest remote repository %s looks unreachable", srv)


@hookimpl
def instance_dropped(ctx: "Context", instance: system.Instance) -> None:
    try:
        service = instance.service(models.Service)
    except ValueError:
        return
    settings = get_settings(ctx.settings)
    base.revert_setup(ctx, service, settings, instance.config(), instance.datadir)


class Server:
    """A pgBackRest TLS server, with a Runnable interface."""

    __service_name__: ClassVar = "pgbackrest"
    name: Optional[str] = None

    def __init__(self, settings: PgBackRestSettings) -> None:
        self.settings = settings
        assert isinstance(settings.repository, HostRepository)
        self.repo_settings: HostRepository = settings.repository

    def __str__(self) -> str:
        return f"pgBackRest TLS server '{self.repo_settings.host}:{self.repo_settings.port}'"

    def args(self) -> list[str]:
        return [
            str(self.settings.execpath),
            "server",
            f"--config={server_configpath(self.settings)}",
        ]

    def pidfile(self) -> Path:
        return Path(str(self.repo_settings.pid_file).format(self.name))

    def env(self) -> Optional[dict[str, str]]:
        return None

    def ping_cmd(self, timeout: int = 1) -> list[str]:
        return [
            str(self.settings.execpath),
            "--config=/dev/null",
            "--tls-server-address=*",
            f"--tls-server-port={self.repo_settings.port}",
            "--log-level-file=off",
            "--log-level-console=off",
            "--log-level-stderr=info",
            f"--io-timeout={timeout}",
            "server-ping",
        ]


def repository_settings(settings: PgBackRestSettings) -> HostRepository:
    assert isinstance(settings.repository, HostRepository)
    return settings.repository


def server_configpath(settings: PgBackRestSettings) -> Path:
    return settings.configpath / "server.conf"


def server_config(settings: PgBackRestSettings) -> configparser.ConfigParser:
    """Build the base configuration for the pgbackrest server running on the
    database host.

    This defines the database host as a TLS server, following:
    https://pgbackrest.org/user-guide-rhel.html#repo-host/config
    """
    cp = parser()
    cp.read_string(util.template("pgbackrest", "server.conf").format(**dict(settings)))
    s = repository_settings(settings)
    cp["global"].update(
        {
            "tls-server-address": "*",
            "tls-server-auth": f"{s.cn}=*",
            "tls-server-ca-file": str(s.certificate.ca_cert),
            "tls-server-cert-file": str(s.certificate.cert),
            "tls-server-key-file": str(s.certificate.key),
            "tls-server-port": str(s.port),
        }
    )
    return cp


def base_config(settings: PgBackRestSettings) -> configparser.ConfigParser:
    """Build the base configuration for pgbackrest clients on the database
    host.
    """
    cp = parser()
    cp.read_string(
        util.template("pgbackrest", "pgbackrest.conf").format(**dict(settings))
    )
    s = repository_settings(settings)
    rhost = {
        "repo1-host-type": "tls",
        "repo1-host": s.host,
    }
    if s.host_port:
        rhost["repo1-host-port"] = str(s.host_port)
    if s.host_config:
        rhost["repo1-host-config"] = str(s.host_config)
    rhost.update(
        {
            "repo1-host-ca-file": str(s.certificate.ca_cert),
            "repo1-host-cert-file": str(s.certificate.cert),
            "repo1-host-key-file": str(s.certificate.key),
        }
    )
    cp["global"].update(rhost)
    return cp
