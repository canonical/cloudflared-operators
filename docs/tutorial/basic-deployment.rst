.. meta::
   :description: Deploy and integrate the cloudflared and cloudflare-configurator Juju charms.

.. _tutorial_basic_deployment:

Deploy the cloudflared charms
==============================

This tutorial deploys the ``cloudflared`` subordinate machine charm and the
``cloudflare-configurator`` charm. It assumes that a principal application
named ``frontend`` is already deployed in a machine-cloud model and provides
``juju-info`` while requiring ``ingress``.

What you'll do
--------------

1. Create an isolated Juju model.
2. Deploy both Cloudflare charms.
3. Integrate the charms with the ``frontend`` application.
4. Configure the tunnel secret and public hostname.
5. Verify the deployment status.

What you'll need
----------------

.. vale Canonical.013-Spell-out-numbers-below-10 = NO

.. SPREAD SKIP

You will need a working station, e.g., a laptop, with AMD64 architecture. Your working station
should have at least 4 CPU cores, 8 GB of RAM, and 50 GB of disk space.

.. tip::

    You can use Multipass to create an isolated environment by running:

    .. code-block::

        multipass launch 24.04 --name charm-tutorial-vm --cpus 4 --memory 8G --disk 50G


This tutorial requires the following software to be installed on your working station
(either locally or in the Multipass VM):

- Juju 3

Use `Concierge <https://github.com/canonical/concierge>`_ to set up Juju and LXD:

.. code-block::

    sudo snap install --classic concierge
    sudo concierge prepare -p machine

This first command installs Concierge, and the second command uses Concierge to install
and configure Juju and LXD.

For this tutorial, Juju must be bootstrapped to a LXD controller. Concierge should
complete this step for you, and you can verify by checking for
``msg="Bootstrapped Juju" provider=lxd``
in the terminal output and by running ``juju controllers``.

If Concierge did not perform the bootstrap, run:

.. code-block::

    juju bootstrap localhost tutorial-controller


To be able to work inside the Multipass VM, log in with the following command:

.. code-block:: bash

    multipass shell charm-tutorial-vm

.. note::

    If you're working locally, you don't need to do this step.

.. SPREAD SKIP END


Set up the environment
----------------------

Create and select a model for this tutorial:

.. code-block:: bash

   juju add-model cloudflare-tutorial
   juju switch cloudflare-tutorial

Deploy the charms
-----------------

Deploy both charms from Charmhub:

.. code-block:: bash

   juju deploy cloudflared
   juju deploy cloudflare-configurator

Integrate the charms
--------------------

Attach the subordinate and connect the configurator to the frontend and
workload charms:

.. code-block:: bash

   juju integrate frontend:juju-info cloudflared:juju-info
   juju integrate frontend:ingress cloudflare-configurator:ingress
   juju integrate cloudflared:cloudflared-route cloudflare-configurator:cloudflared-route

* ``juju-info`` attaches the subordinate ``cloudflared`` charm to the
  principal application's machine.
* ``ingress`` lets ``cloudflare-configurator`` publish the configured public
  hostname to the frontend application.
* ``cloudflared-route`` sends the tunnel token and resolver settings from
  ``cloudflare-configurator`` to ``cloudflared``.

Configure the tunnel
--------------------

Create a Juju secret, grant it to the configurator, and configure the hostname:

.. code-block:: bash

   secret_id="$(juju add-secret cloudflare-tunnel tunnel-token="$CLOUDFLARE_TUNNEL_TOKEN" | awk '/secret:/ {print $1}')"
   juju grant-secret "$secret_id" cloudflare-configurator
   juju config cloudflare-configurator tunnel-token="$secret_id" domain="$CLOUDFLARE_PUBLIC_HOSTNAME"

The tunnel token secret stores authentication credentials for the ``cloudflared``
process with an existing Cloudflare Tunnel. The configurator passes the
secret-backed value to ``cloudflared`` through the ``cloudflared-route`` relation.

The hostname is the public URL associated with the tunnel. The configurator
publishes it to a related frontend through ``ingress``. DNS records and the
Cloudflare-side origin route must still be configured separately in Cloudflare.

Verify the deployment
---------------------

Run ``juju status`` to check the current status and relations:

.. code-block:: bash

   juju status --relations

A healthy deployment has the subordinate attached to ``frontend``, an active
configurator unit, and connected ``cloudflared-route`` and ``ingress``
relations. The exact unit addresses and machine IDs depend on the model. A
successful status has the following shape:

.. code-block:: text

   App                     Version  Status  Scale  Charm
   cloudflare-configurator          active      1  cloudflare-configurator
   cloudflared                       active      1  cloudflared
   frontend                          active      1  frontend

   Relation                      Provides                 Consumes
   cloudflared-route             cloudflare-configurator  cloudflared
   ingress                       cloudflare-configurator  frontend
   juju-info                     frontend                  cloudflared

Clean up the environment
------------------------

Destroy the model when you finish:

.. code-block:: bash

   juju destroy-model cloudflare-tutorial --destroy-storage --force

Next steps
----------

- Learn how to :ref:`configure custom DNS settings <how_to_configure_dns>`.
- Learn how to :ref:`manage multiple tunnel instances <tutorial_advanced_deployment>`.
- Learn how to :ref:`expose a front-end application <how_to_expose_frontend>`.
- Learn how to :ref:`use the configurator charm <how_to_use_configurator>`.
