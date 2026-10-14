# Copyright 2026 Canonical Ltd.
# See LICENSE file for licensing details.

variables {
  app_name    = "cloudflare-configurator"
  base        = "ubuntu@24.04"
  channel     = "latest/edge"
  config      = {}
  constraints = "arch=amd64"
  model_uuid  = "00000000-0000-0000-0000-000000000001"
  revision    = 10
  units       = 2
}

mock_provider "juju" {
  mock_resource "juju_application" {
    override_during = plan
    defaults = {
      id         = "cloudflare-configurator"
      model_type = "iaas"
    }
  }
}

run "deploys_application" {
  command = plan

  assert {
    condition     = output.application.name == "cloudflare-configurator" && output.application.model_uuid == "00000000-0000-0000-0000-000000000001" && output.application.charm[0].name == "cloudflare-configurator" && output.application.charm[0].channel == "latest/edge" && output.application.charm[0].base == "ubuntu@24.04" && output.application.charm[0].revision == 10
    error_message = "application identity did not match the expected deployment"
  }

  assert {
    condition     = output.application.constraints == "arch=amd64"
    error_message = "application constraints did not match expected"
  }

  assert {
    condition     = output.application.units == 2
    error_message = "application units did not match expected"
  }

  assert {
    condition = output.provides == {
      cloudflared_route = {
        kind     = "endpoint"
        name     = "cloudflare-configurator"
        endpoint = "cloudflared-route"
      }
      ingress = {
        kind     = "endpoint"
        name     = "cloudflare-configurator"
        endpoint = "ingress"
      }
    }
    error_message = "provides outputs did not match expected structure"
  }

  assert {
    condition     = output.requires == {}
    error_message = "requires outputs did not match expected structure"
  }
}
