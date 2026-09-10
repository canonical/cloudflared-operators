.. meta::
   :description: Understand the architectural design decisions and code structure of the Cloudflared charms.

.. _explanation_charm_design:

Charm design
============

The project separates tunnel execution from configuration management.
``cloudflared`` is a subordinate machine charm. It attaches to a principal
application through ``juju-info`` and manages one or more parallel
``charmed-cloudflared`` snap instances on that machine.

The ``cloudflare-configurator`` charm is the configuration provider. It reads the
public ``domain``, optional ``nameserver``, and the Juju secret named by
``tunnel-token``. It sends the tunnel token and resolver through
``cloudflared-route`` and publishes the configured HTTPS URL through ``ingress``.

This design keeps secret and routing configuration in one charm while allowing
the workload charm to remain reusable with either a relation provider or its
direct ``tunnel-token`` configuration. The Cloudflare-side origin route is
outside the charm boundary and remains managed through Cloudflare.
