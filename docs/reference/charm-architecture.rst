.. meta::
   :description: Technical overview of the Cloudflared charm architecture and workload.

.. _reference_charm_architecture:

Charm architecture
==================

The repository contains two charms. ``cloudflare-configurator`` manages
configuration, while ``cloudflared`` is a subordinate machine charm that runs
the ``charmed-cloudflared`` snap on the principal application's machine.

The ``cloudflared`` charm does not run a Pebble workload container. On install
and configuration changes it manages parallel snap instances, updates their
resolver and CA certificate files, and restarts the snap services when needed.
A relation-backed deployment creates one snap instance for each active
``cloudflared-route`` relation.

Charm code overview
-------------------

The charm entry points are ``cloudflared-operator/src/charm.py`` and
``cloudflare-configurator-operator/src/charm.py``. Both classes inherit from
``ops.CharmBase`` and reconcile configuration and relation changes.

The configurator reads ``domain``, ``nameserver``, and the Juju secret named by
``tunnel-token``. It publishes the configured URL through ``ingress`` and sends
tunnel settings through ``cloudflared-route``. The workload charm consumes
those settings and manages the installed snap instances.

See :ref:`Relation endpoints <reference_relation_endpoints>` and
:ref:`Configurations <reference_configurations>` for the public interfaces.
