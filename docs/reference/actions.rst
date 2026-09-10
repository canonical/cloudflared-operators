
.. meta::
   :description: Reference documentation for all actions available in the __charm_name__ charm.

.. _reference_actions:

Actions
=======

.. TODO: Add link to the Charmhub actions tab.

See Actions.

.. seealso::


   Read more about actions in the Juju docs: `Action <https://documentation.ubuntu.com/juju/latest/user/reference/action/>`_

The ``cloudflared`` charm provides several Juju actions to manage the lifecycle of your Cloudflare Tunnels directly from the command line.

You can run these actions using the ``juju run`` command. For example:

.. code-block:: bash

   juju run cloudflared-k8s/leader get-ingress-data --param json

Available actions
-----------------

``create-tunnel``
  Provisions a new Cloudflare Tunnel in your Cloudflare account.

  **Parameters:**
  * ``tunnel-name`` (string, required): The desired name for the new tunnel.

``delete-tunnel``
  Permanently deletes an existing Cloudflare Tunnel.

  **Parameters:**
  * ``tunnel-id`` (string, required): The UUID of the tunnel to delete.

``get-tunnel-token``
  Retrieves the authentication token required for the ``cloudflared`` daemon to connect to the Cloudflare edge network. This token is automatically passed to the workload container upon creation.

  **Parameters:**
  * ``tunnel-id`` (string, required): The UUID of the tunnel.

``list-tunnels``
  Queries the Cloudflare API and returns a JSON list of all active tunnels associated with your Cloudflare account.

See also
--------

Read more about actions in the Juju docs: `Action <https://documentation.ubuntu.com/juju/latest/user/reference/action/>`_
