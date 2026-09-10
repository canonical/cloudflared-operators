.. _tutorial_basic_deployment:

Deploy the cloudflared and cloudflare-configurator charms
=========================================================

This tutorial guides you through deploying the ``cloudflared`` and ``cloudflare-configurator`` charms on a Kubernetes environment using Juju.

What you'll do
--------------

1. Deploy the ``cloudflared`` workload charm.
2. Deploy the ``cloudflare-configurator`` charm.
3. Integrate the two charms.
4. Verify the deployment status.

What you'll need
----------------

- A working workstation with AMD64 architecture.
- Juju 3.x installed.
- MicroK8s 1.28+ installed and running.

Set up the environment
----------------------

Create a new Juju model to isolate this tutorial's workload:

.. code-block:: bash

   juju add-model cloudflare-tutorial

Deploy the charms
-----------------

Deploy the ``cloudflared`` and ``cloudflare-configurator`` charms from Charmhub:

.. code-block:: bash

   juju deploy cloudflared-k8s
   juju deploy cloudflare-configurator-k8s

Integrate the charms
--------------------

The ``cloudflare-configurator`` charm passes configuration data to the ``cloudflared`` charm via the ``cloudflared-route`` relation. Integrate them using the following command:

.. code-block:: bash

   juju integrate cloudflared-k8s:cloudflared-route cloudflare-configurator-k8s:cloudflared-route

   Run ``juju status`` to check the current status of the deployment.
The output should be similar to the following:

.. TODO: Add the output of juju status into a command block, showing a successful deployment.
         If using the starter pack, use the terminal directive: https://github.com/canonical/sphinx-terminal/blob/main/README.md

Verify the deployment
---------------------

Run ``juju status`` to check the current status of the deployment:

.. code-block:: bash

   juju status --watch 5s

The deployment is finished when the status for both applications shows as ``active`` and the workload status indicates that the tunnel configuration has been applied.

Clean up the environment
------------------------

You have successfully deployed and integrated the ``cloudflared`` and ``cloudflare-configurator`` charms to establish a secure Cloudflare Tunnel on your Kubernetes cluster.

You can clean up your environment by following this guide:
`Tear down your test environment <https://documentation.ubuntu.com/juju/3.6/howto/manage-your-juju-deployment/tear-down-your-juju-deployment-local-testing-and-development/>`_

Next steps
----------

You achieved a basic deployment of the charm. If you want to go farther in your deployment
or learn more about the charm, check out these pages:

- Learn how to :ref:`configure custom DNS settings <how_to_configure_dns>`.
- Learn how to :ref:`expose a front-end application <how_to_expose_frontend>`.
