.. meta::
   :description: Discover the Cloudflared charm, a Juju operator that deploys and manages Cloudflared.

.. vale Canonical.007-Headings-sentence-case = NO

.. _index:

Cloudflared operator
========================

.. vale Canonical.007-Headings-sentence-case = YES

   Add a 1-2 sentence description of what the charm software does.

A `Juju <https://juju.is/>`_ `charm <https://documentation.ubuntu.com/juju/3.6/reference/charm/>`_
deploying and managing Cloudflare Tunnels on Kubernetes.

Like any Juju charm, this charm supports one-line deployment, configuration, integration,
scaling, and more.
For the cloudflared and cloudflare-configurator charms, this includes:

* Securely exposing internal applications to the internet via Cloudflare Tunnels.
* Centralized configuration management for tunnel routing, DNS, and ingress.
* Seamless integration with the Juju ecosystem and Kubernetes workloads.

These charms will make operating Cloudflare Tunnels simple and straightforward for DevOps or
SRE teams through Juju's clean interface.

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
      - :ref:`Overview <explanation_security>` | Relevant how-to guides | Relevant reference pages

How this documentation is organized
------------------------------------

This documentation uses the `Diátaxis documentation structure <https://diataxis.fr/>`_.

- The :ref:`Tutorial <tutorial_index>` takes you step-by-step through a basic deployment of the Cloudflare charms.
- :ref:`How-to guides <how_to_index>` assume you have basic familiarity with the Cloudflare charms. Learn more about setting up, using, maintaining, and contributing to this charm.
- :ref:`Reference <reference_index>` provides a guide to actions, configurations, relations, and other technical details.
- :ref:`Explanation <explanation_index>` includes topic overviews, background and context and detailed discussion.
- :ref:`Release notes <release_notes_index>` holds all the release notes for the charm, including any system or upgrade requirements.

Contributing to this documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Documentation is an important part of this project, and we take the same open-source approach
to the documentation as the code. As such, we welcome community contributions, suggestions, and
constructive feedback on our documentation.
See :ref:`How to contribute <how_to_contribute>` for more information.

If there's a particular area of documentation that you'd like to see that's missing, please
file a bug.

.. TODO: Add link to GitHub issues page for "file a bug"

Project and community
---------------------

The cloudflared Operator is a member of the Ubuntu family. It's an open-source project that warmly welcomes community
projects, contributions, suggestions, fixes, and constructive feedback.

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

Thinking about using the cloudflared Operator for your next project?
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
