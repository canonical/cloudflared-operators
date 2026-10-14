# Copyright 2026 Canonical Ltd.
# See LICENSE file for licensing details.

variables {
  app_name    = "cloudflared"
  base        = "ubuntu@24.04"
  channel     = "latest/edge"
  config      = {}
  constraints = "arch=amd64"
  model_uuid  = "00000000-0000-0000-0000-000000000001"
  revision    = 10
}

mock_provider "juju" {
  mock_resource "juju_application" {
    override_during = plan
    defaults = {
      id         = "cloudflared"
      model_type = "iaas"
    }
  }
}

run "deploys_application" {
  command = plan

  assert {
    condition     = output.application.name == "cloudflared" && output.application.model_uuid == "00000000-0000-0000-0000-000000000001" && output.application.charm[0].name == "cloudflared" && output.application.charm[0].channel == "latest/edge" && output.application.charm[0].base == "ubuntu@24.04" && output.application.charm[0].revision == 10
    error_message = "application identity did not match the expected deployment"
  }

  assert {
    condition     = output.application.constraints == "arch=amd64"
    error_message = "application constraints did not match expected"
  }

  assert {
    condition = output.provides == {
      cos_agent = {
        kind     = "endpoint"
        name     = "cloudflared"
        endpoint = "cos-agent"
      }
    }
    error_message = "provides outputs did not match expected structure"
  }

  assert {
    condition = output.requires == {
      cloudflared_route = {
        kind     = "endpoint"
        name     = "cloudflared"
        endpoint = "cloudflared-route"
      }
      juju_info = {
        kind     = "endpoint"
        name     = "cloudflared"
        endpoint = "juju-info"
      }
    }
    error_message = "requires outputs did not match expected structure"
  }
}
