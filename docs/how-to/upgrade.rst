.. meta::
   :description: How to upgrade the Cloudflared charms safely.

.. _how_to_upgrade:

How to upgrade
==============

The charms do not manage persistent application data, so no database migration
or backup is required before a charm refresh. Confirm that the model is healthy:

.. code-block:: bash

   juju status

Refresh each application from the channel it was originally deployed from:

.. code-block:: bash

   juju refresh cloudflared
   juju refresh cloudflare-configurator

After the refresh, verify that units, relations, and snap instances are active:

.. code-block:: bash

   juju status --relations

Juju secrets, relation topology, and Cloudflare-side tunnel settings are not
changed by a charm refresh. Review the release notes before upgrading across a
compatibility boundary.
