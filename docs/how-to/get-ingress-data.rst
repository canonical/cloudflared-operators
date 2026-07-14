.. meta::
	 :description: Retrieve ingress relation data from the cloudflare-configurator charm.

.. _how_to_get_ingress_data:

How to get ingress relation data
===============================

Use the ``get-ingress-data`` action to inspect the data that the charm receives on its
``ingress`` relation.

This is useful when you want to verify what application-level and unit-level ingress values
are available before troubleshooting routing behavior.

Prerequisites
-------------

- A deployed ``cloudflare-configurator`` application.
- At least one established ``ingress`` relation.

Run the action
--------------

Run the action on the leader unit:

.. code-block:: bash

	 juju run cloudflare-configurator/0 get-ingress-data

The action returns a result field named ``ingress``.
Its value is a JSON string with two top-level keys:

- ``application-data``: Ingress data for the related application.
- ``unit-data``: A list of ingress data entries for related units, sorted by ``host``.

To print a readable JSON view directly from the command output:

.. code-block:: bash

	 juju run cloudflare-configurator/0 get-ingress-data --format json \
		 | jq -r '.results.ingress' \
		 | jq


The decoded ``ingress`` JSON looks like this:

.. code-block:: json

	 {
		 "application-data": {
			 "model": "my-model",
			 "name": "my-app",
			 "port": 8080,
			 "redirect_https": false,
			 "scheme": "http",
			 "strip_prefix": false,
			 "healthcheck_params": null
		 },
		 "unit-data": [
			 {
				 "host": "my-app-0",
				 "ip": "10.0.0.1"
			 },
			 {
				 "host": "my-app-1",
				 "ip": "10.0.0.2"
			 }
		 ]
	 }

If there is no ``ingress`` relation, the action fails with:

.. code-block:: text

	 no ingress relation
