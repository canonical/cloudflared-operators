.. meta::
   :description: Terraform support for the Cloudflared charms.

.. _how_to_terraform:

How to use Terraform
====================

This repository does not currently contain Terraform modules or ``.tf`` files.
Deploy and relate the charms with Juju as described in the
:ref:`basic deployment tutorial <tutorial_basic_deployment>`.

If a Terraform module is added later, document its source directory, required
Juju model, secret handling, and relation resources here. Do not put tunnel
tokens directly into Terraform configuration or state without following the
secret-management guidance for the chosen provider.
