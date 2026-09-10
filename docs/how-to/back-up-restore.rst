.. meta::
   :description: How to back up and restore Cloudflared charm configuration.

.. _how_to_back_up_restore:

How to back up and restore
===========================

The charms do not manage an application database or other persistent application
data. A backup should preserve the Juju model definition, application
configuration, relation topology, and the Cloudflare-side tunnel configuration.

Keep the tunnel token in a Juju secret. Preserve the secret and its grant to
``cloudflare-configurator`` without exporting the token into a public backup.
When restoring into a new model, recreate the secret, grant it to the
application, and reapply the ``domain`` and ``nameserver`` configuration.
