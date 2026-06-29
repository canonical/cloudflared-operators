# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.
"""Fixtures for charm integration tests."""

import json
import pathlib
import textwrap
from collections.abc import Generator

import jubilant
import pytest
from opcli.pytest_plugin import CharmPathList

PROJECT_BASE = pathlib.Path(__file__).parent.parent.parent.resolve()
JUJU_WAIT_TIMEOUT = 20 * 60  # 20 minutes
CONFIGURATOR_APP = "cloudflare-configurator"
INGRESS_REQUIRER_APP = "ingress-requirer"
CLOUDFLARED_ROUTE_REQUIRER_APP = "cloudflared-route-requirer"


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register the spread/opcli integration options.

    Args:
        parser: Pytest argument parser.
    """
    parser.addoption("--model", action="store", default=None)
    parser.addoption("--keep-models", action="store_true", default=False)


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


@pytest.fixture(scope="module")
def cloudflare_configurator(juju: jubilant.Juju, charm_paths: dict[str, CharmPathList]) -> str:
    """Deploy the cloudflare-configurator charm and return its application name."""
    juju.deploy(charm_paths[CONFIGURATOR_APP].path, app=CONFIGURATOR_APP)
    return CONFIGURATOR_APP


@pytest.fixture(scope="module")
def ingress_requirer(juju: jubilant.Juju) -> str:
    """Deploy an ingress requirer using any-charm."""
    ingress_requirer_src = textwrap.dedent(
        """\
        import ops
        from ingress import IngressPerAppRequirer
        from any_charm_base import AnyCharmBase
        class AnyCharm(AnyCharmBase):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.ingress = IngressPerAppRequirer(self, port=8080)
                self.unit.status = ops.ActiveStatus()
        """
    )
    juju.deploy(
        "any-charm",
        app=INGRESS_REQUIRER_APP,
        config={
            "src-overwrite": json.dumps(
                {
                    "any_charm.py": ingress_requirer_src,
                    "ingress.py": (
                        PROJECT_BASE / "lib/charms/traefik_k8s/v2/ingress.py"
                    ).read_text(),
                }
            ),
            "python-packages": "pydantic",
        },
        num_units=2,
        channel="latest/edge",
    )
    return INGRESS_REQUIRER_APP


@pytest.fixture(scope="module")
def cloudflared_route_requirer(juju: jubilant.Juju) -> str:
    """Deploy a cloudflared-route requirer using any-charm."""
    src = textwrap.dedent(
        """\
        import ops
        from cloudflared_route import CloudflaredRouteRequirer
        from any_charm_base import AnyCharmBase
        class AnyCharm(AnyCharmBase):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.cloudflared_route = CloudflaredRouteRequirer(
                    charm=self,
                    relation_name="require-cloudflared-route"
                )
                self.unit.status = ops.ActiveStatus()
            def get_tunnel_tokens(self):
                return [
                    self.cloudflared_route.get_tunnel_token(relation)
                    for relation in self.model.relations["require-cloudflared-route"]
                ]
        """
    )
    juju.deploy(
        "any-charm",
        app=CLOUDFLARED_ROUTE_REQUIRER_APP,
        config={
            "src-overwrite": json.dumps(
                {
                    "any_charm.py": src,
                    "cloudflared_route.py": (
                        PROJECT_BASE / "lib/charms/cloudflare_configurator/v0/cloudflared_route.py"
                    ).read_text(),
                }
            ),
        },
        num_units=2,
        channel="latest/edge",
    )
    return CLOUDFLARED_ROUTE_REQUIRER_APP
