.. meta::
   :description: Technical reference documentation for the Cloudflared charms.

.. _reference_index:

Reference
=========

This section contains technical details about the ``cloudflared`` subordinate
machine charm and the ``cloudflare-configurator`` charm. It documents their
configuration, actions, events, relations, and operational interfaces.

Charm usage
-----------

The following pages provide reference information for deploying and integrating
the charms.

.. vale Canonical.013-Spell-out-numbers-below-10 = NO
.. vale Canonical.500-Repeated-words = NO
.. vale Canonical.004-Canonical-product-names = NO

.. toctree::
    :hidden:
    :maxdepth: 1

    Actions <actions>
    Configurations <configurations>
    Relation endpoints <relation-endpoints>
    Juju events <juju-events>
    Metrics <metrics>

.. vale Canonical.004-Canonical-product-names = YES

Architecture and deployments
----------------------------

These pages describe the subordinate workload, the configurator, and their
relations to a principal application.

.. toctree::
    :hidden:
    :maxdepth: 1

    Charm architecture <charm-architecture>
    High-level deployment overview <high-level-deployment>

Advanced topics
---------------

These pages cover cryptographic boundaries and the current Terraform status.

.. toctree::
    :hidden:
    :maxdepth: 1

    Cryptographic overview <cryptographic-overview>
    Terraform <terraform>
