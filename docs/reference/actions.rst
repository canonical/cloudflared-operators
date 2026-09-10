.. meta::
   :description: Reference documentation for actions provided by the cloudflare-configurator charm.

.. _reference_actions:

Actions
=======

The ``cloudflare-configurator`` charm provides one action. The ``cloudflared``
charm does not declare Juju actions.

Get ingress data
----------------

Run the action on the configurator leader:

.. code-block:: bash

   juju run cloudflare-configurator/0 get-ingress-data

The action returns an ``ingress`` result containing a JSON string with:

* ``application-data``: ingress data for the related application.
* ``unit-data``: ingress data for related units, sorted by ``host``.

The action fails with ``no ingress relation`` when the configurator has no
related ingress application. See :ref:`How to get ingress relation data
<how_to_get_ingress_data>` for a complete example.

See also
--------

Read more about actions in the Juju docs: `Action <https://documentation.ubuntu.com/juju/latest/user/reference/action/>`_.
See the `cloudflare-configurator actions on Charmhub <https://charmhub.io/cloudflare-configurator/actions>`_.
