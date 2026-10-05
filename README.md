# cloudflared operators

This repository provides a collection of operators related to Cloudflare's `cloudflared` tunnel.
This repository contains the code for the following charms:
1. `cloudflared`: A subordinate machine charm that deploys and manages the `cloudflared` tunnel. See the [cloudflared-operator README](cloudflared-operator/README.md) for more information.
2. `cloudflare-configurator`: A charm that configures the `cloudflared` charm. See the [cloudflare-configurator-operator README](cloudflare-configurator-operator/README.md) for more information.
The repository also contains the snapped workload of some charms:
1. `charmed-cloudflared`: A snap of the `cloudflared` workload made for the `cloudflared` charm. See the [charmed-cloudflared-snap README](charmed-cloudflared-snap/README.md) for more information.

## Repository layout

```
charmed-cloudflared-snap/        # Snap packaging for the cloudflared workload used by the charm
  snap/                          # Snapcraft project files
  tests/                         # Snap tests

cloudflare-configurator-operator/ # Juju charm: configures cloudflared and publishes ingress data
  src/                           # Charm source code
  lib/                           # Charm libraries
  tests/                         # Charm tests

cloudflared-operator/            # Juju subordinate charm: runs and manages cloudflared on a principal machine
  src/                           # Charm source code
  lib/                           # Charm libraries
  docs/                          # Component-level documentation assets
  tests/                         # Charm tests

docs/                            # Product documentation
```

## Components

| Component | Path | Role |  |
| --- | --- | --- | --- |
| `cloudflared` | [`cloudflared-operator/`](cloudflared-operator/) | A subordinate machine charm that deploys and manages the `cloudflared` tunnel. |  |
| `cloudflare-configurator` | [`cloudflare-configurator-operator/`](cloudflare-configurator-operator/) | A charm that configures the `cloudflared` charm. |  |
| `charmed-cloudflared` | [`charmed-cloudflared-snap/`](charmed-cloudflared-snap/) | A snap of the `cloudflared` workload made for the `cloudflared` charm. |  |

The deployment relationship is described in more detail in [High-level deployment overview](docs/reference/high-level-deployment.rst) and [Charm architecture](docs/reference/charm-architecture.rst).

### Charmhub and Snapcraft

| Name | Listing |
| --- | --- |
| `cloudflare-configurator` | https://charmhub.io/cloudflare-configurator |
| `cloudflared` | https://charmhub.io/cloudflared |
| `charmed-cloudflared` | https://snapcraft.io/charmed-cloudflared |

## Get started

Start with the in-repository [basic deployment tutorial](docs/tutorial/basic-deployment.rst), which deploys both charms, integrates them with a principal application, and configures the tunnel secret and hostname.

## Integrations

See [Relation endpoints](docs/reference/relation-endpoints.rst).

## Documentation

Our documentation is stored in the `docs` directory. In structuring, the
documentation employs the [Diataxis](https://diataxis.fr/) approach.

You may open a pull request with your documentation changes, or you can
[file a bug](https://github.com/canonical/cloudflared-operators/issues) to
provide constructive feedback or suggestions.

GitHub runs automatic checks on the documentation to verify links and style
guide compliance.

You can (and should) run the same checks locally:

```bash
make lychee
make vale
```

## Project and community

The cloudflared-operators project is a member of the Ubuntu family. It is an open source project that warmly welcomes community projects, contributions, suggestions, fixes and constructive feedback.

* [Code of conduct](https://ubuntu.com/community/code-of-conduct)
* [Get support](https://discourse.charmhub.io/)
* [Issues](https://github.com/canonical/cloudflared-operators/issues)
* [Matrix](https://matrix.to/#/#charmhub-charmdev:ubuntu.com)
* [Contribute](https://github.com/canonical/cloudflared-operators/blob/main/CONTRIBUTING.md)

## Licensing and trademark

See [`LICENSE`](LICENSE) for details.
