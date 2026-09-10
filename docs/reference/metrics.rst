.. meta::
   :description: Reference documentation for metrics exposed by the Cloudflared charm.

.. _reference_metrics:

Metrics
=======

The ``cloudflared`` charm exposes metrics through its ``cos-agent`` relation.
The metrics are provided by the installed ``charmed-cloudflared`` snap
instances rather than by a custom HTTP server in the charm.

Metric ports are allocated as follows:

* ``15299`` is used for an instance configured with the direct ``tunnel-token``
  option.
* Relation-backed instances use ``15300 + relation ID``.

The charm also publishes the dashboard in
``cloudflared-operator/src/grafana_dashboards/cloudflared.json`` through the COS
relation. See :ref:`How to integrate with COS <how_to_integrate_with_cos>` for
the integration command.
