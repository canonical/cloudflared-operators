# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

# pylint: disable=protected-access,too-many-arguments,too-many-positional-arguments

"""Integration tests."""

import json
import logging
import subprocess  # nosec
import time

import jubilant

logger = logging.getLogger(__name__)


def wait_for_tunnel_healthy(cloudflare_api, tunnel_token):
    """Wait for a cloudflared tunnel to become healthy.

    Args:
        cloudflare_api (obj): Cloudflare API object.
        tunnel_token (str): Tunnel token.

    Raises:
        TimeoutError: If tunnel fails to become healthy in given timeout.
    """
    deadline = time.time() + 300
    while time.time() < deadline:
        tunnel_status = cloudflare_api.get_tunnel_status_by_token(tunnel_token)
        logger.info("tunnel status: %s", tunnel_status)
        if tunnel_status != "healthy":
            time.sleep(10)
        else:
            return
    raise TimeoutError("timeout waiting for tunnel healthy")


def reboot_application(juju: jubilant.Juju, app: str) -> None:
    """Reboot the LXD containers hosting an application.

    Args:
        juju: Jubilant juju instance.
        app: Application name.
    """
    status = json.loads(juju.cli("status", "--format", "json"))
    machines = status.get("machines", {})
    applications = status.get("applications", {})

    machine_ids: set[str] = set()
    for unit in applications.get(app, {}).get("units", {}).values():
        if "machine" in unit:
            machine_ids.add(unit["machine"])
    if not machine_ids:
        for principal in applications.values():
            for unit in principal.get("units", {}).values():
                subordinates = unit.get("subordinates", {})
                if any(sub.split("/")[0] == app for sub in subordinates) and "machine" in unit:
                    machine_ids.add(unit["machine"])

    for machine in machine_ids:
        container = machines.get(machine, {}).get("instance-id")
        if container is None:
            continue
        logger.info("restarting LXD container %s for %s", container, app)
        subprocess.run(["lxc", "restart", container], check=True)  # nosec


def test_tunnel_token_config(juju, cloudflare_api, cloudflared_charm):
    """
    arrange: deploy the cloudflared charm.
    act: provide the tunnel-token charm config.
    assume: cloudflared tunnels provided in the charm config is up and healthy
    """
    base_app = "any-charm"
    juju.deploy("any-charm", app=base_app, channel="latest/beta", base="ubuntu@24.04")
    juju.integrate(f"{base_app}:juju-info", f"{cloudflared_charm}:juju-info")
    tunnel_token = cloudflare_api.create_tunnel_token()
    secret_uri = juju.add_secret("test-tunnel-token", {"tunnel-token": tunnel_token})
    juju.grant_secret("test-tunnel-token", cloudflared_charm)
    juju.config(cloudflared_charm, {"tunnel-token": str(secret_uri)})
    juju.wait(jubilant.all_agents_idle, error=jubilant.any_error)
    # required for deploying in LXD containers
    reboot_application(juju, base_app)
    juju.wait(jubilant.all_agents_idle, error=jubilant.any_error)
    wait_for_tunnel_healthy(cloudflare_api, tunnel_token)


def test_cloudflared_route_integration(
    juju,
    cloudflare_api,
    cloudflared_charm,
    cloudflared_route_provider_1,
    cloudflared_route_provider_2,
):
    """
    arrange: deploy the cloudflared charm and cloudflared-route provider charms.
    act: provide some cloudflared tunnel tokens using cloudflared-route provider charms.
    assume: cloudflared tunnels provided in the integration is up and healthy.
    """
    juju.config(cloudflared_charm, {"tunnel-token": ""})
    juju.wait(jubilant.all_agents_idle, error=jubilant.any_error)
    tunnel_token_1 = cloudflare_api.create_tunnel_token()
    tunnel_token_2 = cloudflare_api.create_tunnel_token()
    juju.run(
        f"{cloudflared_route_provider_1}/0",
        "rpc",
        {"method": "set_tunnel_token", "args": json.dumps([tunnel_token_1])},
    )
    juju.run(
        f"{cloudflared_route_provider_2}/0",
        "rpc",
        {"method": "set_tunnel_token", "args": json.dumps([tunnel_token_2])},
    )
    juju.wait(jubilant.all_agents_idle, error=jubilant.any_error)
    # required for deploying in LXD containers
    reboot_application(juju, cloudflared_charm)
    juju.wait(jubilant.all_agents_idle, error=jubilant.any_error)
    wait_for_tunnel_healthy(cloudflare_api, tunnel_token_1)
    wait_for_tunnel_healthy(cloudflare_api, tunnel_token_2)


def test_update_snap_channel(juju, cloudflared_charm):
    """
    arrange: deploy the cloudflared charm.
    act: update the charmed-cloudflared-snap-channel charm configuration.
    assume: cloudflared charm should refresh all charmed-cloudflared snap instances.
    """
    juju.config(cloudflared_charm, {"charmed-cloudflared-snap-channel": "latest/edge"})
    juju.wait(jubilant.all_agents_idle, error=jubilant.any_error)
    snap_list = juju.cli("exec", "--unit", "any-charm/0", "--", "snap", "list")
    assert "charmed-cloudflared_" in snap_list
    for line in snap_list.splitlines():
        if "charmed-cloudflared_" in line:
            assert "latest/edge" in line


def test_nameserver(
    juju,
    cloudflare_api,
    cloudflared_charm,
    cloudflared_route_provider_1,
    dnsmasq,
    dnsmasq_ip,
):
    """
    arrange: deploy the cloudflared charm and cloudflared-route provider charms.
    act: provide cloudflared tunnel token with a specific nameserver setting for cloudflared
        using cloudflared-route provider charms.
    assume: cloudflared tunnels should use the given nameserver.
    """
    juju.config(cloudflared_charm, {"tunnel-token": ""})
    juju.wait(jubilant.all_agents_idle, error=jubilant.any_error)
    tunnel_token = cloudflare_api.create_tunnel_token()
    logger.info("use dnsmasq nameserver: %s", dnsmasq_ip)
    juju.run(
        f"{cloudflared_route_provider_1}/0",
        "rpc",
        {"method": "set_nameserver", "args": json.dumps([dnsmasq_ip])},
    )
    juju.run(
        f"{cloudflared_route_provider_1}/0",
        "rpc",
        {"method": "set_tunnel_token", "args": json.dumps([tunnel_token])},
    )
    juju.wait(jubilant.all_agents_idle, error=jubilant.any_error)
    # required for deploying in LXD containers
    reboot_application(juju, cloudflared_charm)
    juju.wait(jubilant.all_agents_idle, error=jubilant.any_error)
    wait_for_tunnel_healthy(cloudflare_api, tunnel_token)
    dnsmasq_logs = juju.cli("exec", "--unit", f"{dnsmasq}/0", "--", "cat", "/var/log/dnsmasq.log")
    assert "argotunnel.com" in dnsmasq_logs


def test_remove(juju, cloudflared_charm):
    """
    arrange: deploy the cloudflared charm and cloudflared-route provider charms.
    act: remove the cloudflared charm.
    assume: cloudflared charm should uninstall all charmed-cloudflared snap instances.
    """
    snap_list = juju.cli("exec", "--unit", "any-charm/0", "--", "snap", "list")
    assert "charmed-cloudflared_" in snap_list
    logger.info("snap list before removal: %s", snap_list)
    juju.remove_relation(cloudflared_charm, "any-charm")
    juju.wait(lambda status: not status.apps[cloudflared_charm].units)
    deadline = time.time() + 300
    while True:
        snap_list = juju.cli("exec", "--unit", "any-charm/0", "--", "snap", "list")
        if "charmed-cloudflared_" not in snap_list or time.time() > deadline:
            break
        time.sleep(5)
    assert "charmed-cloudflared_" not in snap_list
    logger.info("snap list after removal: %s", snap_list)
    juju.integrate("any-charm", cloudflared_charm)


def test_secret_config_permission(
    juju, cloudflared_charm, cloudflared_route_provider_1, cloudflared_route_provider_2
):
    """
    arrange: create a tunnel token juju secret without granting the secret access to the charm.
    act: configure the charm with the incorrect juju secret.
    assume: cloudflared charm should enter error state.
    """
    juju.remove_relation(cloudflared_charm, cloudflared_route_provider_1)
    juju.remove_relation(cloudflared_charm, cloudflared_route_provider_2)
    secret_uri = juju.add_secret("error-tunnel-token", {"tunnel-token": "foobar"})
    juju.config(cloudflared_charm, {"tunnel-token": str(secret_uri)})
    juju.wait(jubilant.any_error)
    juju_status = juju.cli("status")
    logger.info("current juju status: %s", juju_status)
    assert "error" in juju_status
