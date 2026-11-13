# Copyright 2026 Canonical Ltd.
# See LICENSE file for licensing details.

output "application" {
  description = "The deployed application object."
  value       = juju_application.cloudflare_configurator
}

output "provides" {
  description = "Map of the provided integration endpoints."
  value = {
    cloudflared_route = {
      kind     = "endpoint"
      name     = juju_application.cloudflare_configurator.name
      endpoint = "cloudflared-route"
    }
    ingress = {
      kind     = "endpoint"
      name     = juju_application.cloudflare_configurator.name
      endpoint = "ingress"
    }
  }
}

output "requires" {
  description = "Map of the required integration endpoints."
  value       = {}
}
