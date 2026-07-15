#!/usr/bin/env python3
# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.
# pylint: disable=protected-access
"""Integration test fixtures."""

import json
import logging
import os
import pathlib
import random
import string
import textwrap
from collections.abc import Generator
from datetime import datetime

import jubilant
import pytest
import requests
from opcli.pytest_plugin import CharmPathList

PROJECT_BASE = pathlib.Path(__file__).parent.parent.parent.resolve()
JUJU_WAIT_TIMEOUT = 20 * 60  # 20 minutes
CLOUDFLARED_APP = "cloudflared"
CLOUDFLARED_ROUTE_PROVIDER_1 = "cloudflared-route-provider-one"
CLOUDFLARED_ROUTE_PROVIDER_2 = "cloudflared-route-provider-two"
DNSMASQ_APP = "dnsmasq"
logger = logging.getLogger(__name__)


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register the spread/opcli integration options.

    Args:
        parser: Pytest argument parser.
    """
    parser.addoption("--model", action="store", default=None)
    parser.addoption("--keep-models", action="store_true", default=False)


class CloudflareAPI:
    """Cloudflare API."""

    def __init__(self, account_id, api_token) -> None:
        """Initialize the Cloudflare API.

        Args:
            account_id: cloudflare account ID.
            api_token: cloudflare API token.
        """
        self._endpoint = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/cfd_tunnel"
        self._session = requests.Session()
        self._session.headers.update(
            {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
        )
        self._created_tunnels: list[str] = []
        self._tunnel_token_lookup: dict[str, str] = {}

    def _create_tunnel(self) -> str:
        """Create a Tunnel.

        Returns:
            Cloudflare tunnel ID.
        """
        name = datetime.now().strftime("%Y%m%d-%H%M%S-")
        # bandit complains about using random instead of secrets here
        name = name + "".join(random.choices(string.ascii_letters + string.digits, k=4))  # nosec
        response = self._session.post(
            self._endpoint, json={"name": name, "config_src": "cloudflare"}, timeout=10
        )
        response.raise_for_status()
        tunnel_id = response.json()["result"]["id"]
        logger.info("created tunnel %s", tunnel_id)
        self._created_tunnels.append(tunnel_id)
        return tunnel_id

    def _get_tunnel_token(self, tunnel_id: str) -> str:
        """Get tunnel token.

        Args:
            tunnel_id: cloudflare tunnel ID.

        Returns:
            Tunnel token.
        """
        response = self._session.get(f"{self._endpoint}/{tunnel_id}/token", timeout=10)
        response.raise_for_status()
        tunnel_token = response.json()["result"]
        self._tunnel_token_lookup[tunnel_token] = tunnel_id
        return tunnel_token

    def create_tunnel_token(self) -> str:
        """Create a tunnel and return its tunnel token.

        Returns:
            Tunnel token.
        """
        tunnel_id = self._create_tunnel()
        return self._get_tunnel_token(tunnel_id)

    def _get_tunnel_status(self, tunnel_id: str) -> str:
        """Get tunnel status.

        Args:
            tunnel_id: cloudflare tunnel ID.

        Returns:
            Tunnel status.
        """
        response = self._session.get(f"{self._endpoint}/{tunnel_id}", timeout=10)
        response.raise_for_status()
        return response.json()["result"]["status"]

    def get_tunnel_status_by_token(self, tunnel_token: str) -> str:
        """Get tunnel status by its tunnel token.

        Args:
            tunnel_token: cloudflare tunnel token.

        Returns:
            Tunnel status.
        """
        tunnel_id = self._tunnel_token_lookup[tunnel_token]
        return self._get_tunnel_status(tunnel_id)

    def delete_tunnel(self, tunnel_id: str) -> None:
        """Delete a tunnel.

        Args:
            tunnel_id: cloudflare tunnel ID.
        """
        logger.info("deleting tunnel %s", tunnel_id)
        connections_response = self._session.delete(
            f"{self._endpoint}/{tunnel_id}/connections", timeout=10
        )
        connections_response.raise_for_status()
        response = self._session.delete(f"{self._endpoint}/{tunnel_id}", timeout=10)
        response.raise_for_status()


@pytest.fixture(scope="module")
def cloudflare_api():
    """Cloudflare API fixture."""
    account_id = os.environ["CLOUDFLARE_ACCOUNT_ID"]
    api_token = os.environ["CLOUDFLARE_API_TOKEN"]
    api = CloudflareAPI(account_id=account_id, api_token=api_token)
    yield api
    for tunnel_id in api._created_tunnels:
        try:
            api.delete_tunnel(tunnel_id)
        except requests.exceptions.RequestException:
            logger.exception("failed to delete tunnel %s", tunnel_id)


@pytest.fixture(scope="module", name="juju")
def juju_fixture(request: pytest.FixtureRequest) -> Generator[jubilant.Juju, None, None]:
    """Jubilant juju fixture wrapping the spread-provided or a temporary model."""

    def show_debug_log(juju: jubilant.Juju):
        if request.session.testsfailed:
            print(juju.cli("status", "--relations"), end="")
            print(juju.debug_log(limit=1000), end="")

    model = request.config.getoption("--model")
    if model:
        juju = jubilant.Juju(model=model)
        juju.wait_timeout = JUJU_WAIT_TIMEOUT
        yield juju
        show_debug_log(juju)
        return
    keep_models = bool(request.config.getoption("--keep-models"))
    with jubilant.temp_model(keep=keep_models) as juju:
        juju.wait_timeout = JUJU_WAIT_TIMEOUT
        yield juju
        show_debug_log(juju)


@pytest.fixture(name="cloudflared_charm", scope="module")
def cloudflared_charm_fixture(juju: jubilant.Juju, charm_paths: dict[str, CharmPathList]) -> str:
    """Deploy the cloudflared charm and return its application name."""
    juju.deploy(charm_paths[CLOUDFLARED_APP].path, app=CLOUDFLARED_APP)
    return CLOUDFLARED_APP


SRC_OVERWRITE = json.dumps(
    {
        "any_charm.py": textwrap.dedent(
            """\
            import ops
            from cloudflared_route import CloudflaredRouteProvider
            from any_charm_base import AnyCharmBase
            class AnyCharm(AnyCharmBase):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.cloudflared_route = CloudflaredRouteProvider(
                        charm=self,
                        relation_name="provide-cloudflared-route"
                    )
                    self.unit.status = ops.ActiveStatus()
                def set_tunnel_token(self, tunnel_token):
                    return self.cloudflared_route.set_tunnel_token(tunnel_token)
                def unset_tunnel_token(self):
                    self.cloudflared_route.unset_tunnel_token()
                def set_nameserver(self, nameserver):
                    return self.cloudflared_route.set_nameserver(nameserver)
            """
        ),
        "cloudflared_route.py": (
            PROJECT_BASE / "lib/charms/cloudflare_configurator/v0/cloudflared_route.py"
        ).read_text(),
    }
)


@pytest.fixture(name="cloudflared_route_provider_1", scope="module")
def cloudflared_route_provider_1_fixture(juju: jubilant.Juju, cloudflared_charm: str) -> str:
    """Deploy a cloudflared-route provider using any-charm."""
    juju.deploy(
        "any-charm",
        app=CLOUDFLARED_ROUTE_PROVIDER_1,
        config={"src-overwrite": SRC_OVERWRITE},
        channel="latest/beta",
        base="ubuntu@24.04",
    )
    juju.integrate(f"{cloudflared_charm}:cloudflared-route", CLOUDFLARED_ROUTE_PROVIDER_1)
    return CLOUDFLARED_ROUTE_PROVIDER_1


@pytest.fixture(name="cloudflared_route_provider_2", scope="module")
def cloudflared_route_provider_2_fixture(juju: jubilant.Juju, cloudflared_charm: str) -> str:
    """Deploy a cloudflared-route provider using any-charm."""
    juju.deploy(
        "any-charm",
        app=CLOUDFLARED_ROUTE_PROVIDER_2,
        config={"src-overwrite": SRC_OVERWRITE},
        channel="latest/beta",
        base="ubuntu@24.04",
    )
    juju.integrate(f"{cloudflared_charm}:cloudflared-route", CLOUDFLARED_ROUTE_PROVIDER_2)
    return CLOUDFLARED_ROUTE_PROVIDER_2


@pytest.fixture(name="dnsmasq", scope="module")
def dnsmasq_fixture(juju: jubilant.Juju) -> str:
    """Deploy and configure a dnsmasq server."""
    juju.deploy("ubuntu", app=DNSMASQ_APP, channel="latest/edge")
    juju.wait(jubilant.all_agents_idle, error=jubilant.any_error)
    juju.cli("exec", "--application", DNSMASQ_APP, "--", "apt", "update")
    juju.cli("exec", "--application", DNSMASQ_APP, "--", "apt", "install", "dnsmasq", "-y")
    for line in (
        "server=1.1.1.1",
        "bind-interfaces",
        "log-queries",
        "log-facility=/var/log/dnsmasq.log",
    ):
        juju.cli(
            "exec",
            "--application",
            DNSMASQ_APP,
            "--",
            "bash",
            "-c",
            f"echo {line} >> /etc/dnsmasq.conf",
        )
    juju.cli("exec", "--application", DNSMASQ_APP, "--", "systemctl", "restart", "dnsmasq")
    return DNSMASQ_APP


@pytest.fixture(scope="module")
def dnsmasq_ip(juju: jubilant.Juju, dnsmasq: str) -> str:
    """Get the IP address of dnsmasq."""
    status = json.loads(juju.cli("status", "--format", "json"))
    units = status["applications"][dnsmasq]["units"]
    return next(iter(units.values()))["public-address"]
