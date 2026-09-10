.. _how_to_expose_frontend:

Expose a front-end application
==============================

Cloudflare Tunnels allow you to securely expose internal applications to the public internet without opening public ingress ports on your firewall. This guide explains how to expose a front-end web application (such as a React, Vue, or static HTML server) running inside your Kubernetes cluster.

Prerequisites
-------------

- A deployed front-end application charm (e.g., an HTTP server or Nginx charm) running in the same Juju model.
- The ``cloudflared`` and ``cloudflare-configurator`` charms deployed and integrated.

Define the Ingress Rule
-----------------------

To route external traffic to your front-end application, you must define an ingress rule in the ``cloudflare-configurator`` charm. This rule maps a public hostname to the internal service name and port of your front-end app.

Set the ingress configuration on the ``cloudflare-configurator`` charm. Replace ``frontend`` and ``8080`` with your actual application's service name and port:

.. code-block:: bash

   juju config cloudflare-configurator ingress='{
     "hostname": "frontend.example.com",
     "service": "http://frontend:8080"
   }'

*Note: The exact configuration key for ingress rules may vary based on your specific charm revision. Consult the :ref:`Configurations Reference <reference_configurations>` for the exact dictionary schema.*

Verify External Access
----------------------

1. Ensure your DNS records in Cloudflare point ``frontend.example.com`` to your Cloudflare Tunnel's CNAME.
2. Open a web browser and navigate to ``https://frontend.example.com``.
3. The ``cloudflared`` daemon will intercept the traffic at the Cloudflare edge and securely route it through the tunnel to your front-end application pod.

