.. meta::
   :description: Reference documentation for configurations available in the Cloudflared charms.

.. _reference_configurations:

Configurations
==============

This page details the configuration options available for the
``cloudflared`` and ``cloudflare-configurator`` charms.

cloudflare-configurator
-----------------------

The configurator manages the public hostname and sends tunnel settings to the
workload over ``cloudflared-route``.

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Key
     - Type
     - Description
   * - ``domain``
     - String
     - The public hostname to publish through the ``ingress`` relation. Both
       ``domain`` and ``tunnel-token`` are required before the configurator
       publishes or sends route data.
   * - ``nameserver``
     - String
     - Optional DNS server for resolving origin names. If unset, the charm
       attempts to resolve ``kube-dns.kube-system.svc``. Set this option
       explicitly when that service is not resolvable in the deployment model.
   * - ``tunnel-token``
     - Secret
     - A Juju secret containing a ``tunnel-token`` key. Grant the secret to
       ``cloudflare-configurator`` before setting this option.

cloudflared
-----------

The ``cloudflared`` subordinate consumes tunnel settings from the
``cloudflared-route`` relation. It can also be configured directly when no
route provider is used:

.. list-table::
   :widths: 35 15 50
   :header-rows: 1

   * - Key
     - Type
     - Description
   * - ``tunnel-token``
     - Secret
     - A Juju secret containing a ``tunnel-token`` key. This option cannot be
       used at the same time as a ``cloudflared-route`` relation.
   * - ``charmed-cloudflared-snap-channel``
     - String
     - Channel used for the installed ``charmed-cloudflared`` snap. The
       default is ``latest/stable``.

.. seealso::

   Read more about configurations in the Juju docs: `Configuration <https://documentation.ubuntu.com/juju/latest/user/reference/configuration/>`_.
