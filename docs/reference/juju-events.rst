.. meta::
   :description: Reference documentation for Juju events observed by the Cloudflared charms.

.. _reference_juju_events:

Juju events
===========

The ``cloudflared`` charm observes and reconciles these events:

* ``install`` enables parallel snap instances.
* ``config-changed`` and ``secret-changed`` recalculate tunnel specifications.
* ``cloudflared-route-relation-changed`` applies tunnel tokens and nameservers.
* ``cloudflared-route-relation-departed`` removes instances for departed
  relation-backed tunnels.
* ``juju-info-relation-changed`` attaches the subordinate to a principal.
* ``juju-info-relation-departed`` removes subordinate workload state.
* ``juju-info-relation-broken`` stops the workload when the principal is gone.
* ``stop`` removes installed ``charmed-cloudflared`` snap instances.

The ``cloudflare-configurator`` charm observes ``config-changed``, ingress data
changes, ``cloudflared-route`` relation changes, and the
``get-ingress-data`` action. Its reconciliation requires both ``domain`` and
``tunnel-token`` before it publishes or sends tunnel data.
