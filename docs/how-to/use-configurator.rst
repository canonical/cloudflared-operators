.. _how_to_use_configurator:

Use the cloudflare-configurator charm
=====================================

The ``cloudflare-configurator`` charm acts as a centralized configuration manager for the ``cloudflared`` charm. Instead of configuring the workload charm directly, you configure the ``cloudflare-configurator``, which safely passes settings (like DNS nameservers, ingress rules, and tunnel credentials) to ``cloudflared`` via the ``cloudflared-route`` relation.

Prerequisites
-------------

You must have both the ``cloudflared`` and ``cloudflare-configurator`` charms deployed and integrated. If you haven't done this yet, follow the :ref:`Basic Deployment Tutorial <tutorial_basic_deployment>`.

Update tunnel configurations
----------------------------

To update the configuration for your Cloudflare Tunnel, apply the settings to the ``cloudflare-configurator`` charm.

For example, to update custom headers or routing metrics, use the ``juju config`` command:

.. code-block:: bash

   juju config cloudflare-configurator-k8s nameserver=8.8.8.8

Once the configuration is applied, the ``config-changed`` event will trigger. The configurator charm will format the data and pass it across the relation endpoint to the ``cloudflared`` charm, which will automatically reload the ``cloudflared`` daemon with the new settings.

Managing Tunnel Credentials
---------------------------

If your architecture requires injecting a specific Cloudflare Tunnel token or certificate, you can provide it via the configurator charm's relation or configuration options. This ensures sensitive data is handled securely and passed to the workload container without modifying the workload charm's direct environment.

