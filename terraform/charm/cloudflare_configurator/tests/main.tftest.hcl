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
    # renovate: depName="cloudflare-configurator"
    revision = 11
  }

  assert {
    condition     = output.application.name == "cloudflare-configurator"
    error_message = "cloudflare-configurator application name did not match expected"
  }

  assert {
    condition     = output.provides.cloudflared_route.endpoint == "cloudflared-route"
    error_message = "cloudflare-configurator module should provide 'provides.cloudflared_route' output"
  }

  assert {
    condition     = output.provides.ingress.endpoint == "ingress"
    error_message = "cloudflare-configurator module should provide 'provides.ingress' output"
  }
}
