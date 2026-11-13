.. meta::
   :description: A high-level overview of the Cloudflared charms and their relations.

.. _reference_high_level_deployment:

High-level overview of Cloudflared deployment
==============================================

The ``cloudflared`` charm is a subordinate machine charm. It runs the
``charmed-cloudflared`` snap on a machine attached to a principal application
through ``juju-info``. The ``cloudflare-configurator`` charm supplies the tunnel
credential and optional DNS resolver over ``cloudflared-route``.

A frontend application can integrate with the configurator's ``ingress``
endpoint. The configurator publishes the public hostname on that relation. The
Cloudflare-side tunnel configuration still defines the origin service.

The deployment uses these relations:

* ``frontend:juju-info`` to ``cloudflared:juju-info`` attaches the subordinate.
* ``cloudflare-configurator:cloudflared-route`` to
  ``cloudflared:cloudflared-route`` sends tunnel settings.
* ``frontend:ingress`` to ``cloudflare-configurator:ingress`` publishes the
  public URL and receives ingress data.
* ``cloudflared:cos-agent`` publishes metrics and dashboards to a COS consumer.
