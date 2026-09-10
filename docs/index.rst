.. meta::
   :description: Discover the Cloudflared charms, Juju operators for managing Cloudflare Tunnels.

.. vale Canonical.007-Headings-sentence-case = NO

.. _index:

Cloudflared operator
====================

.. vale Canonical.007-Headings-sentence-case = YES

The Cloudflared Operators project provides Juju charms for running and configuring
Cloudflare Tunnels on machines managed by Juju.

The ``cloudflared`` subordinate charm runs the ``charmed-cloudflared`` snap on a
principal application's machine. The ``cloudflare-configurator`` charm manages
tunnel credentials, DNS settings, and the public URL published through the
``ingress`` relation. Cloudflare-side origin routing remains configured in
Cloudflare.

These charms are useful to DevOps and SRE teams that want to manage Cloudflare
Tunnel processes and their Juju integrations through a consistent operator
interface.

In this documentation
---------------------

.. list-table::
    :header-rows: 1

    * -
      -
    * - Get started
      - :ref:`Guided tutorial <tutorial_index>` | :ref:`High-level deployment <reference_high_level_deployment>`
    * - Deployment
      - :ref:`Configure DNS <how_to_configure_dns>` | :ref:`Expose a front-end <how_to_expose_frontend>`
    * - Operations
      - :ref:`Integrate with COS <how_to_integrate_with_cos>` | :ref:`Upgrade <how_to_upgrade>` | :ref:`Troubleshoot <how_to_troubleshoot>`
    * - Product-specific feature
      - :ref:`Use the configurator charm <how_to_use_configurator>` | :ref:`Actions <reference_actions>`
    * - Design
      - :ref:`Architecture <reference_charm_architecture>` | :ref:`Design <explanation_charm_design>`
    * - Security
      - :ref:`Overview <explanation_security>` | :ref:`Configurations <reference_configurations>`

How this documentation is organized
------------------------------------

This documentation uses the `Diátaxis documentation structure <https://diataxis.fr/>`_.

- The :ref:`Tutorial <tutorial_index>` takes you step-by-step through a basic deployment of the Cloudflared charms.
- :ref:`How-to guides <how_to_index>` assume you have basic familiarity with the Cloudflared charms.
- :ref:`Reference <reference_index>` provides actions, configurations, relations, and other technical details.
- :ref:`Explanation <explanation_index>` includes design, security, and operational context.
- :ref:`Release notes <release_notes_index>` holds release information and upgrade requirements.

Contributing to this documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Documentation is an important part of this project. See :ref:`How to contribute <how_to_contribute>`
for contribution guidance. To report a missing topic or an error, open an issue in the
`cloudflared-operators issue tracker <https://github.com/canonical/cloudflared-operators/issues>`_.

Project and community
---------------------

The cloudflared Operators project is a member of the Ubuntu family. It welcomes
community projects, contributions, suggestions, fixes, and constructive feedback.

Governance and policies
^^^^^^^^^^^^^^^^^^^^^^^

- `Code of conduct <https://ubuntu.com/community/code-of-conduct>`_

Get involved
^^^^^^^^^^^^

- `Get support <https://discourse.charmhub.io/>`_
- `Join our online chat <https://matrix.to/#/#charmhub-charmdev:ubuntu.com>`_
- :ref:`Contribute <how_to_contribute>`

Releases
^^^^^^^^

- :ref:`Release notes <release_notes_index>`

Thinking about using the Cloudflared Operators for your next project?
`Get in touch <https://matrix.to/#/#charmhub-charmdev:ubuntu.com>`_!

.. vale Canonical.013-Spell-out-numbers-below-10 = NO
.. vale Canonical.500-Repeated-words = NO

.. toctree::
    :hidden:
    :maxdepth: 1

    Tutorial <tutorial/index>
    How-to guides <how-to/index>
    Reference <reference/index>
    Explanation <explanation/index>
    Release notes <release-notes/index>
    Changelog <changelog>
