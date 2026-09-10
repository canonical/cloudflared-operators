.. meta::
   :description: Reference documentation for relations supported by the Cloudflared charms.

.. _reference_relation_endpoints:

Relation endpoints
==================

The charms use these relations to attach the subordinate, transfer tunnel
settings, publish ingress data, and expose metrics.

cloudflared-route
-----------------

* **Interface**: ``cloudflared-route``
* **Provider**: ``cloudflare-configurator:cloudflared-route``
* **Requirer**: ``cloudflared:cloudflared-route``
* **Data**: tunnel token and optional nameserver.

.. code-block:: bash

   juju integrate cloudflared:cloudflared-route cloudflare-configurator:cloudflared-route

Juju relation
-------------

* **Interface**: ``juju-info``
* **Provider**: the principal application.
* **Requirer**: ``cloudflared:juju-info``.
* **Purpose**: attaches the subordinate charm to the principal application.

.. code-block:: bash

   juju integrate frontend:juju-info cloudflared:juju-info

Ingress relation
-----------------

* **Interface**: ``ingress``
* **Provider**: ``cloudflare-configurator:ingress``
* **Requirer**: a frontend application that supports the ``ingress`` interface.
* **Data**: the configurator publishes the configured HTTPS URL and reads
  application and unit ingress data.

.. code-block:: bash

   juju integrate frontend:ingress cloudflare-configurator:ingress

COS agent relation
-------------------

* **Interface**: ``cos_agent``
* **Provider**: ``cloudflared:cos-agent``
* **Requirer**: a COS agent consumer.
* **Data**: metrics scrape endpoints and the Cloudflared Grafana dashboard.

.. code-block:: bash

   juju integrate cloudflared:cos-agent cos-agent-consumer
