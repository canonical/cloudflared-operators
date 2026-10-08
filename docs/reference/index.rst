.. meta::
   :description: Technical reference documentation for the Cloudflared charms.

.. _reference_index:

Reference
=========

Technical specifications and architectural details about the `cloudflared`
subordinate charm and the `cloudflare-configurator` charm.

Charm usage
-----------

Operators control charm behavior through configuration options, Juju actions,
and Juju integrations. Learn the inner workings of the charm, which can help
you understand the current charm configuration interface and debug problems.

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

Peek into the design and architecture of the charm, which is useful if you want to
audit or contribute to the Cloudflared charm project.

.. toctree::
    :hidden:
    :maxdepth: 1

    Charm architecture <charm-architecture>
    High-level deployment overview <high-level-deployment>
    Security and cryptographic overview <cryptographic-overview>
