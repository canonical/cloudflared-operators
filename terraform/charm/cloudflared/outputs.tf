# Copyright 2026 Canonical Ltd.
# See LICENSE file for licensing details.

output "application" {
  description = "The deployed application object."
  value       = juju_application.cloudflared
}

output "provides" {
  description = "Map of the provided integration endpoints."
  value = {
    cos_agent = {
      kind     = "endpoint"
      name     = juju_application.cloudflared.name
      endpoint = "cos-agent"
    }
  }
}

output "requires" {
  description = "Map of the required integration endpoints."
  value = {
    cloudflared_route = {
      kind     = "endpoint"
      name     = juju_application.cloudflared.name
      endpoint = "cloudflared-route"
    }
    juju_info = {
      kind     = "endpoint"
      name     = juju_application.cloudflared.name
      endpoint = "juju-info"
    }
  }
}
