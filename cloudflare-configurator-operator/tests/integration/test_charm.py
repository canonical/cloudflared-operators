#!/usr/bin/env python3
# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.
"""Integration tests."""

import json
import logging

import jubilant

logger = logging.getLogger(__name__)


def test_build_and_deploy(
    juju, cloudflare_configurator, ingress_requirer, cloudflared_route_requirer
):
    """
    arrange: deploy the cloudflare-configurator charm with related charms.
    act: relate the cloudflare-configurator charm with related charms.
    assert: no error happens.
    """
    juju.integrate(f"{cloudflare_configurator}:ingress", f"{ingress_requirer}:ingress")
    juju.integrate(f"{cloudflare_configurator}:cloudflared-route", cloudflared_route_requirer)
    juju.wait(jubilant.all_agents_idle)


def test_set_tunnel_token(juju, cloudflare_configurator, cloudflared_route_requirer):
    """
    arrange: deploy the cloudflare-configurator charm with related charms.
    act: set tunnel-token charm configuration of the cloudflare-configurator charm.
    assert: cloudflare-configurator charm pass the tunnel-token to cloudflared-route requirers.
    """
    secret_uri = juju.add_secret("tunnel-token", {"tunnel-token": "foobar"})
    juju.grant_secret("tunnel-token", cloudflare_configurator)
    juju.config(
        cloudflare_configurator, {"domain": "example.com", "tunnel-token": str(secret_uri)}
    )
    juju.wait(jubilant.all_active)
    task = juju.run(f"{cloudflared_route_requirer}/0", "rpc", {"method": "get_tunnel_tokens"})
    assert json.loads(task.results["return"]) == ["foobar"]


def test_get_ingress_data(juju, cloudflare_configurator, ingress_requirer):
    """
    arrange: deploy the cloudflare-configurator charm with related charms.
    act: run get-ingress-data charm action.
    assert: get-ingress-data charm action dumps ingress integration data.
    """
    task = juju.run(f"{cloudflare_configurator}/0", "get-ingress-data")
    ingress_data = json.loads(task.results["ingress"])
    assert ingress_data["application-data"]["model"] == juju.model
    assert ingress_data["application-data"]["name"] == ingress_requirer
    assert len(ingress_data["unit-data"]) == len(juju.status().apps[ingress_requirer].units)
