import logging
import socket
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Optional
from unittest.mock import patch

import pgtoolkit.conf
import pytest
import yaml
from tenacity import retry
from tenacity.retry import retry_if_exception_type
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_fixed

from pglift import instances, postgresql, systemd
from pglift._compat import zip
from pglift.ctx import Context
from pglift.models import interface, system
from pglift.patroni import impl as patroni
from pglift.patroni.models import Service, ServiceManifest
from pglift.pgbackrest import base as pgbackrest
from pglift.pgbackrest import models as pgbackrest_models
from pglift.pgbackrest import repo_path
from pglift.settings import PatroniSettings, Settings
from pglift.systemd import service_manager
from pglift.types import ConfigChanges, Status

from ..etcd import Etcd
from . import AuthType, PostgresLogger, check_connect, passfile_entries
from .conftest import Factory
from .pgbackrest import PgbackrestRepoHost


@contextmanager
def reconfigure_instance(
    ctx: Context,
    manifest: interface.Instance,
    **confitems: Any,
) -> Iterator[ConfigChanges]:
    """Context manager to temporarily change instance settings.

    Upon enter, this applies provided settings (and possibly new port)
    and yields settings 'changes' dict.

    Upon exit, the previous settings is restored, and the 'changes' dict
    returned upon enter is updated to reflect this.
    """
    update: dict[str, Any] = {"restart_on_changes": manifest.restart_on_changes}
    if confitems:
        update["settings"] = manifest.settings.copy() | confitems
    assert update
    changes = instances.configure(ctx, manifest._copy_validate(update))
    try:
        yield changes
    finally:
        restored_changes = instances.configure(ctx, manifest)
        changes.clear()
        changes.update(restored_changes)


@pytest.fixture(scope="session", autouse=True)
def _patroni_available(patroni_execpath: Optional[Path]) -> None:
    if not patroni_execpath:
        pytest.skip("Patroni is not available")


@pytest.fixture(scope="module", autouse=True)
def _etcd_running(etcd_host: Etcd) -> Iterator[None]:
    with etcd_host.running():
        yield None


@pytest.fixture(scope="module", autouse=True)
def http_logs() -> None:
    logging.getLogger("httpx").setLevel(logging.DEBUG)
    logging.getLogger("httpcore").setLevel(logging.DEBUG)


@pytest.fixture
def patroni_settings(settings: Settings) -> PatroniSettings:
    return patroni.get_settings(settings)


@pytest.fixture(scope="module")
def cluster_name(postgresql_auth: AuthType) -> str:
    # Since instances are kept running while moving from one postgresql_auth
    # value to another, we need distinct cluster name for each.
    return f"pglift-tests-{postgresql_auth}"


def _make_instance(
    settings: Settings,
    manifest: interface.Instance,
    postgres_logger: PostgresLogger,
    pgbackrest_repo_host: Optional[PgbackrestRepoHost],
    pgbackrest_password: Optional[str],
) -> Iterator[system.Instance]:
    ctx = Context(settings=settings)
    assert instances.apply(ctx, manifest)
    instance = system.Instance.system_lookup(
        (manifest.name, manifest.version, settings)
    )
    postgres_logger(instance)
    if settings.pgbackrest:
        if not instance.standby:
            # make a pgbackrest backup so future standby could be initialized from
            # pgbackrest backup
            if pgbackrest_repo_host is not None:
                svc = instance.service(pgbackrest_models.Service)
                pgbackrest_repo_host.add_stanza(svc.stanza, instance)
                pgbackrest.check(
                    ctx, instance, svc, settings.pgbackrest, pgbackrest_password
                )
                pgbackrest_repo_host.run(
                    "backup",
                    "--stanza",
                    svc.stanza,
                    "--type",
                    "full",
                )
            else:
                repo_path.backup(ctx, instance, settings.pgbackrest)
        else:
            # ensure standby has been created from pgbackrest backup
            assert instance._settings.patroni is not None
            assert any(
                "replica has been created using pgbackrest" in line
                for line in patroni.logs(instance.qualname, instance._settings.patroni)
            )
    yield instance
    if instances.exists(instance.name, instance.version, instance._settings):
        instances.drop(ctx, instance)


@pytest.fixture(scope="module")
def instance1_manifest(
    settings: Settings,
    instance_manifest_factory: Factory[interface.Instance],
    cluster_name: str,
    tmp_port_factory: Iterator[int],
) -> interface.Instance:
    name = "test1"
    host = socket.gethostbyname(socket.gethostname())
    extras = {}
    if settings.pgbackrest:
        extras = {"pgbackrest": {"stanza": "patroni"}}
    return instance_manifest_factory(
        settings,
        name,
        state="started",
        patroni={
            "cluster": cluster_name,
            "node": name,
            "restapi": {
                "connect_address": f"{host}:{next(tmp_port_factory)}",
                "listen": f"{host}:{next(tmp_port_factory)}",
            },
        },
        auth={"host": "password"},
        settings={
            "listen_addresses": "*",
            "work_mem": "8MB",
        },
        **extras,
    )


@pytest.fixture(scope="module")
def instance1(
    settings: Settings,
    instance1_manifest: interface.Instance,
    postgres_logger: PostgresLogger,
    pgbackrest_repo_host: Optional[PgbackrestRepoHost],
    pgbackrest_password: Optional[str],
) -> Iterator[system.Instance]:
    yield from _make_instance(
        settings,
        instance1_manifest,
        postgres_logger,
        pgbackrest_repo_host,
        pgbackrest_password,
    )


@pytest.fixture(scope="module")
def instance2_manifest(
    settings: Settings,
    instance_manifest_factory: Factory[interface.Instance],
    cluster_name: str,
    tmp_port_factory: Iterator[int],
    instance1: system.Instance,
) -> interface.Instance:
    name = "test2"
    host = socket.gethostbyname(socket.gethostname())
    extras = {}
    if settings.pgbackrest:
        extras = {"pgbackrest": {"stanza": "patroni"}}
    return instance_manifest_factory(
        settings,
        name,
        state="started",
        patroni={
            "cluster": cluster_name,
            "node": name,
            "restapi": {
                "connect_address": f"{host}:{next(tmp_port_factory)}",
                "listen": f"{host}:{next(tmp_port_factory)}",
            },
        },
        auth={"host": "password"},
        settings={
            "listen_addresses": "*",
            "work_mem": "8MB",
        },
        **extras,
    )


@pytest.fixture(scope="module")
def instance2(
    settings: Settings,
    instance2_manifest: interface.Instance,
    postgres_logger: PostgresLogger,
    pgbackrest_repo_host: Optional[PgbackrestRepoHost],
    pgbackrest_password: Optional[str],
) -> Iterator[system.Instance]:
    yield from _make_instance(
        settings,
        instance2_manifest,
        postgres_logger,
        pgbackrest_repo_host,
        pgbackrest_password,
    )


@pytest.fixture
def primary_standby(
    instance1: system.Instance, instance2: system.Instance
) -> tuple[system.Instance, system.Instance]:
    if instance1.standby:
        assert not instance2.standby
        return instance2, instance1
    else:
        assert instance2.standby
        return instance1, instance2


@pytest.fixture
def primary(
    primary_standby: tuple[system.Instance, system.Instance]
) -> system.Instance:
    return primary_standby[0]


@pytest.fixture
def standby(
    primary_standby: tuple[system.Instance, system.Instance]
) -> system.Instance:
    return primary_standby[1]


def test_service_and_config(
    patroni_settings: PatroniSettings,
    instance1: system.Instance,
    instance1_manifest: interface.Instance,
    instance2: system.Instance,
    instance2_manifest: interface.Instance,
    cluster_name: str,
) -> None:
    for instance, manifest in (
        (instance1, instance1_manifest),
        (instance2, instance2_manifest),
    ):
        check_server_and_config(instance, manifest, patroni_settings, cluster_name)


def test_pgpass(
    patroni_settings: PatroniSettings,
    primary: system.Instance,
    standby: system.Instance,
    replrole_password: str,
) -> None:
    primary_pgpass = patroni._pgpass(primary.qualname, patroni_settings)
    assert not primary_pgpass.exists()
    standby_pgpass = patroni._pgpass(standby.qualname, patroni_settings)
    assert standby_pgpass.exists()
    (replication_entry,) = passfile_entries(standby_pgpass, role="replication")
    assert replication_entry.endswith(
        f":{primary.port}:*:replication:{replrole_password}"
    )


def check_server_and_config(
    instance: system.Instance,
    manifest: interface.Instance,
    settings: PatroniSettings,
    cluster_name: str,
) -> None:
    s = instance.service(Service)
    assert s and s.cluster == cluster_name
    configpath = patroni._configpath(instance.qualname, settings)
    with configpath.open() as f:
        config = yaml.safe_load(f)
    listen_addr = manifest.patroni.restapi.listen  # type: ignore[attr-defined]
    assert config["restapi"]["listen"] == listen_addr
    assert config["postgresql"]["listen"] == f"*:{instance.port}"
    assert config["postgresql"]["parameters"]["listen_addresses"] == "*"
    assert config["postgresql"]["parameters"]["work_mem"] == "8MB"
    assert config["bootstrap"]["dcs"]["loop_wait"] == 1


def test_postgresql_conf(instance1: system.Instance) -> None:
    pgconf = pgtoolkit.conf.parse(instance1.datadir / "postgresql.base.conf")
    assert "lc_messages" in pgconf.as_dict()
    assert "lc_monetary" in pgconf.as_dict()


def test_logpath(patroni_settings: PatroniSettings, instance1: system.Instance) -> None:
    logpath = patroni_settings.logpath / instance1.qualname
    assert logpath.exists()
    assert (logpath / "patroni.log").exists()


def logs(instance: system.Instance, settings: PatroniSettings) -> list[str]:
    return [
        line.split("INFO: ", 1)[-1].strip()
        for line in patroni.logs(instance.qualname, settings)
    ]


def test_logs(
    patroni_settings: PatroniSettings,
    instance1: system.Instance,
    instance2: system.Instance,
) -> None:
    logs1 = logs(instance1, patroni_settings)
    logs2 = logs(instance2, patroni_settings)
    leader = instance1.name
    secondary = instance2.name
    assert f"no action. I am ({leader}), the leader with the lock" in logs1
    assert (
        f"no action. I am ({secondary}), a secondary, and following a leader ({leader})"
        in logs2
    )


@pytest.mark.parametrize(
    "setting,expected",
    [
        ("work_mem", "8MB"),
        ("listen_addresses", "*"),
    ],
)
def test_postgresql_config(
    instance1: system.Instance, setting: str, expected: Any
) -> None:
    pgconf = instance1.config()
    assert pgconf[setting] == expected


def test_configure_postgresql(
    ctx: Context,
    patroni_settings: PatroniSettings,
    instance1_manifest: interface.Instance,
    instance1: system.Instance,
    tmp_port_factory: Iterator[int],
) -> None:
    postgresql_conf = instance1.datadir / "postgresql.conf"
    mtime = postgresql_conf.stat().st_mtime

    # Retry assertions on postgresql.conf, waiting for patroni reload (1s, per
    # loop_wait).
    @retry(
        retry=(
            retry_if_exception_type(ValueError)
            | retry_if_exception_type(AttributeError)
        ),
        wait=wait_fixed(0.5),
        stop=stop_after_attempt(5),
        reraise=True,
    )
    def check_postgresql_config(work_mem: str, mtime: float) -> float:
        mtime_after = postgresql_conf.stat().st_mtime
        if mtime_after <= mtime:
            raise ValueError
        pgconf = pgtoolkit.conf.parse(postgresql_conf)
        assert pgconf.work_mem == work_mem
        return mtime_after

    with reconfigure_instance(ctx, instance1_manifest, work_mem="10MB") as changes:
        config = patroni.config(instance1.qualname, patroni_settings)
        assert config.postgresql.parameters["work_mem"] == "10MB"
        mtime = check_postgresql_config("10MB", mtime)
        assert changes == {"work_mem": ("8MB", "10MB")}

    assert changes == {"work_mem": ("10MB", "8MB")}
    config = patroni.config(instance1.qualname, patroni_settings)
    assert config.postgresql.parameters["work_mem"] == "8MB"
    check_postgresql_config("8MB", mtime)


def test_instance_get(
    ctx: Context,
    patroni_settings: PatroniSettings,
    instance1: system.Instance,
    instance2: system.Instance,
    surole_password: Optional[str],
    cluster_name: str,
) -> None:
    for instance in (instance1, instance2):
        if surole_password is not None and instance is instance2:
            with patch.dict("os.environ", {"PGPASSWORD": surole_password}):
                i = instances.get(ctx, instance)
        else:
            i = instances.get(ctx, instance)
        p = i.service_manifest(ServiceManifest)
        assert p is not None and p.cluster == cluster_name
        assert p.cluster == cluster_name
        assert {m.name for m in p.cluster_members} == {"test1", "test2"}


def test_check_api_status(
    patroni_settings: PatroniSettings, instance1: system.Instance
) -> None:
    assert patroni.check_api_status(instance1.qualname, patroni_settings)


def test_cluster_members(
    patroni_settings: PatroniSettings,
    instance1: system.Instance,
    instance2: system.Instance,
) -> None:
    members = patroni.cluster_members(instance1.qualname, patroni_settings)
    assert len(members) == 2, members
    for m, i in zip(members, (instance1, instance2), strict=True):
        assert m.port == i.port


def test_cluster_leader(
    patroni_settings: PatroniSettings,
    instance1: system.Instance,
    instance2: system.Instance,
) -> None:
    assert patroni.cluster_leader(instance1.qualname, patroni_settings) == "test1"
    assert patroni.cluster_leader(instance2.qualname, patroni_settings) == "test1"


def test_connect(
    ctx: Context,
    postgresql_auth: AuthType,
    instance1_manifest: interface.Instance,
    instance1: system.Instance,
    instance2_manifest: interface.Instance,
    instance2: system.Instance,
) -> None:
    check_connect(ctx, postgresql_auth, instance1_manifest, instance1)
    check_connect(ctx, postgresql_auth, instance2_manifest, instance2)


def test_start_stop(
    ctx: Context,
    settings: Settings,
    instance1: system.Instance,
    patroni_settings: PatroniSettings,
) -> None:
    use_systemd = settings.service_manager == "systemd"

    assert postgresql.is_running(instance1)
    if use_systemd:
        assert systemd.is_active(
            ctx, service_manager.unit("patroni", instance1.qualname)
        )
    assert patroni.check_api_status(instance1.qualname, patroni_settings)

    with instances.stopped(ctx, instance1):
        assert postgresql.status(instance1) == Status.not_running
        if use_systemd:
            assert not systemd.is_active(
                ctx, service_manager.unit("patroni", instance1.qualname)
            )
        assert not patroni.check_api_status(instance1.qualname, patroni_settings)


def test_restart(
    ctx: Context, instance1: system.Instance, patroni_settings: PatroniSettings
) -> None:
    assert postgresql.is_running(instance1)
    assert patroni.check_api_status(instance1.qualname, patroni_settings)
    instances.restart(ctx, instance1)
    assert postgresql.is_running(instance1)
    assert patroni.check_api_status(instance1.qualname, patroni_settings)


def test_reload(ctx: Context, instance1: system.Instance) -> None:
    instances.reload(ctx, instance1)


def test_stop(
    ctx: Context, instance1: system.Instance, instance2: system.Instance
) -> None:
    # Mostly to avoid keeping two instances running while we're moving to the
    # next 'auth' flavour.
    instances.stop(ctx, instance2)
    instances.stop(ctx, instance1)
