.. meta::
   :description: Advanced operations for the Cloudflared charms.

.. _tutorial_advanced_deployment:

Advanced operations for cloudflared
===================================
This tutorial assumes that you completed the :ref:`basic deployment tutorial
<tutorial_basic_deployment>`. It covers settings that are useful when one
model manages more than one tunnel or needs observability.

Configure a custom nameserver
-----------------------------

Set a resolver on the configurator. The value is sent to each relation-backed
``cloudflared`` snap instance:

.. code-block:: bash

   juju config cloudflare-configurator nameserver=8.8.8.8

Unset the option to return to the resolver configuration of the host machine:

.. code-block:: bash

   juju config cloudflare-configurator nameserver=""

Manage multiple tunnel instances
--------------------------------

The ``cloudflared`` charm creates a separate snap instance for each active
``cloudflared-route`` relation. Add another route provider, then verify all
instances and relations:

.. code-block:: bash

   juju status --relations
   juju debug-log --replay

A direct ``tunnel-token`` configuration and a route-backed configuration cannot
be used at the same time. Remove the direct configuration before adding a route
provider.

Change the snap channel
-----------------------

Select a supported channel for the installed workload snap:

.. code-block:: bash

   juju config cloudflared charmed-cloudflared-snap-channel=latest/edge

The charm refreshes each installed snap instance after the configuration change.

Integrate with COS
------------------

Use the ``cos-agent`` relation to publish snap metrics endpoints and the
Cloudflared dashboard:

.. code-block:: bash

   juju integrate cloudflared:cos-agent cos-agent-consumer
