# Copyright 2026 Canonical Ltd.
# See LICENSE file for licensing details.

run "setup_tests" {
  module {
    source = "./tests/setup"
  }
}

run "basic_deploy" {
  variables {
    model_uuid = run.setup_tests.model_uuid
    base       = "ubuntu@24.04"
    channel    = "latest/edge"
    # renovate: depName="cloudflared"
    revision = 40
  }

  assert {
    condition     = output.application.name == "cloudflared"
    error_message = "cloudflared application name did not match expected"
  }

  assert {
    condition     = output.provides.cos_agent.endpoint == "cos-agent"
    error_message = "cloudflared module should provide 'provides.cos_agent' output"
  }

  assert {
    condition     = output.requires.cloudflared_route.endpoint == "cloudflared-route"
    error_message = "cloudflared module should provide 'requires.cloudflared_route' output"
  }

  assert {
    condition     = output.requires.juju_info.endpoint == "juju-info"
    error_message = "cloudflared module should provide 'requires.juju_info' output"
  }
}
