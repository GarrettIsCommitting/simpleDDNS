# simpleDDNS
A simple DDNS implementation in Python

[![simpleDDNS Docker Image CI](https://github.com/GarrettIsCommitting/simpleDDNS/actions/workflows/docker-image.yaml/badge.svg)](https://github.com/GarrettIsCommitting/simpleDDNS/actions/workflows/docker-image.yaml)

### Caveats
This is primarily written for educational purposes 
and should not be used in production.
The initial version is targeted at the Cloudflare API
but will be structured so that additional providers 
may be added as modules.

### Purpose
To create and manage an A record entry that reflects the
current public IPv4 address of the network where this runs.

### Deployment
For ease of use this is primarily intended to run inside
a docker container, but local configuration will be possible as well.

#### Docker
1. Replace the dummy values in `.env` with real values
2. At the root of the project run `docker compose up -d`
