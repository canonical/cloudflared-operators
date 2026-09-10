.. meta::
   :description: Integrate the cloudflared charm with the Canonical Observability Stack.

.. _how_to_integrate_with_cos:

How to integrate with COS
=========================

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
