.. meta::
   :description: Reference documentation for configurations available in the cloudflared and
   cloudflare-configurator charms.

.. _reference_configurations:

Configurations
==============

This page details the configuration options available for the charms in the 
``cloudflared-operators`` repository.

cloudflare-configurator
-----------------------

The ``cloudflare-configurator`` charm handles the public-facing domain and routing logic.

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Key
     - Type
     - Description
   * - ``domain``
     - String
     - The public hostname (e.g., ``app.example.com``) that your application will be exposed on via
     Cloudflare.
   * - ``nameserver``
     - String
     - The DNS server the tunnel should use for resolving internal service names. If not provided,
     the charm defaults to the Kubernetes cluster's internal DNS (``kube-dns.kube-system.svc``).
   * - ``tunnel-token``
     - String
     - The authentication token required to connect the tunnel to your Cloudflare Zero Trust
     account. Both ``domain`` and ``tunnel-token`` must be set for the route to become active.

cloudflared
-----------

The ``cloudflared`` subordinate charm manages the tunnel workload. It primarily consumes
configurations from the ``cloudflare-configurator`` charm via relations (such as the
``nameserver`` passed to its ``resolv.conf``), but it also supports specific workload 
configurations if needed.

.. seealso::
   
   Read more about configurations in the Juju docs: `Configuration <https://documentation.ubuntu.com/juju/latest/user/reference/configuration/>`_
