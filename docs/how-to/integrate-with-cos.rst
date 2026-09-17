.. meta::
   :description: Learn how to integrate the cloudflared charm with the Canonical Observability Stack.

.. _how_to_integrate_with_cos:

How to integrate with Canonical Observability Stack (COS)
=========================================================

The `Canonical Observability Stack (COS) <https://documentation.ubuntu.com/observability/latest/>`_
is a collection of charms that is used to provide observability, metrics and
tracing for a charm and its workload.

The ``cloudflared`` charm provides the ``cos-agent`` relation. It publishes the
metrics endpoints for its installed ``charmed-cloudflared`` snap instances and
its Grafana dashboard through this relation.

Deploy a COS agent consumer in the same model, then integrate it with the
charm:

.. code-block:: bash

   juju integrate cloudflared:cos-agent cos-agent-consumer

The charm creates metrics port ``15299`` for a direct ``tunnel-token``
configuration. Relation-backed tunnel instances use port ``15300`` plus the
relation ID. Confirm the relation and workload status with:

.. code-block:: bash

   juju status --relations
