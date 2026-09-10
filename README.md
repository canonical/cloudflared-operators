# cloudflared operators
This repository provides a collection of operators related to Cloudflare's `cloudflared` tunnel.
This repository contains the code for the following charms:
1. `cloudflared`: A subordinate machine charm that deploys and manages the `cloudflared` tunnel. See the [cloudflared-operator README](cloudflared-operator/README.md) for more information.
2. `cloudflare-configurator`: A charm that configures the `cloudflared` charm. See the [cloudflare-configurator-operator README](cloudflare-configurator-operator/README.md) for more information.
The repository also contains the snapped workload of some charms:
1. `charmed-cloudflared`: A snap of the `cloudflared` workload made for the `cloudflared` charm. See the [charmed-cloudflared-snap README](charmed-cloudflared-snap/README.md) for more information.

## Charmhub and Snapcraft

| Name | Listing |
|------|---------|
| `cloudflare-configurator` | https://charmhub.io/cloudflare-configurator |
| `cloudflared` | https://charmhub.io/cloudflared |
| `charmed-cloudflared` | https://snapcraft.io/charmed-cloudflared |

## Project and community
The cloudflared-operators project is a member of the Ubuntu family. It is an open source project that warmly welcomes community projects, contributions, suggestions, fixes and constructive feedback.
* [Code of conduct](https://ubuntu.com/community/code-of-conduct)
* [Get support](https://discourse.charmhub.io/)
* [Issues](https://github.com/canonical/cloudflared-operators/issues)
* [Matrix](https://matrix.to/#/#charmhub-charmdev:ubuntu.com)
* [Contribute](https://github.com/canonical/cloudflared-operators/blob/main/CONTRIBUTING.md)
## Documentation
Our documentation is stored in the `docs` directory.
It is based on the Canonical starter pack
and hosted on [Read the Docs](https://about.readthedocs.com/). In structuring,
the documentation employs the [Diataxis](https://diataxis.fr/) approach.
You may open a pull request with your documentation changes, or you can
[file a bug](https://github.com/canonical/cloudflared-operators/issues) to provide constructive feedback or suggestions.
