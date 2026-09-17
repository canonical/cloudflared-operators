.. meta::
   :description: Manage multiple Cloudflare Tunnel instances with Juju.

.. _tutorial_advanced_deployment:

Manage multiple Cloudflare Tunnel instances
===========================================

This tutorial assumes that you completed the :ref:`basic deployment tutorial
<tutorial_basic_deployment>`. A second tunnel provider can give a separate
team or environment an independent tunnel lifecycle and credentials. This
tutorial shows how to attach it to the same ``cloudflared`` subordinate. Each
active ``cloudflared-route``
relation creates a separate ``charmed-cloudflared`` snap instance.

What you'll need
----------------

- A healthy basic deployment.
- A second Cloudflare Tunnel and its token in
  ``CLOUDFLARE_SECOND_TUNNEL_TOKEN``.
- A hostname for the second tunnel in ``CLOUDFLARE_SECOND_PUBLIC_HOSTNAME``.

Create the second tunnel and configure its public hostname in Cloudflare before
continuing. Save the tunnel token and hostname in the environment variables
shown above. See the `Cloudflare Tunnel documentation
<https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/>`_
for the Cloudflare-side setup.

Deploy a second configurator
----------------------------

Deploy another instance of the configurator charm and connect it to
``cloudflared``. The existing ``cloudflare-configurator`` application remains
the first tunnel provider:

.. code-block:: bash

   juju deploy cloudflare-configurator tunnel-b
   juju integrate tunnel-b:cloudflared-route cloudflared:cloudflared-route

Configure the second tunnel
---------------------------

Create a separate Juju secret for the second tunnel. Grant the secret to the
second configurator and set its hostname:

.. code-block:: bash

   secret_id="$(juju add-secret cloudflare-tunnel-b \
       tunnel-token="$CLOUDFLARE_SECOND_TUNNEL_TOKEN" | awk '/secret:/ {print $1}')"
   juju grant-secret "$secret_id" tunnel-b
   juju config tunnel-b tunnel-token="$secret_id" \
       domain="$CLOUDFLARE_SECOND_PUBLIC_HOSTNAME"

Verify both tunnel instances
----------------------------

Check that both route relations are present:

.. code-block:: bash

   juju status --relations

The ``cloudflared`` unit should have two active ``cloudflared-route``
relations, one from each configurator application. The subordinate creates one
snap instance for each relation. You can inspect the instances on the
subordinate unit:

.. code-block:: bash

   juju exec --unit cloudflared/0 -- snap list | grep charmed-cloudflared

The two tunnel tokens and public host names are managed independently. Removing one
``cloudflared-route`` relation removes only the corresponding snap instance.

Clean up
--------

Remove the second configurator when you finish with the additional tunnel:

.. code-block:: bash

   juju remove-application tunnel-b

This removes the second route relation and its corresponding snap instance
while leaving the basic deployment in place.

Next steps
----------

- Learn how to :ref:`integrate with COS <how_to_integrate_with_cos>`.
- Learn how to :ref:`upgrade the charms <how_to_upgrade>`.
