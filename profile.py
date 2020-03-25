kube_description= \
"""
Levi: Four pure Ubuntu 18.04 VMs running DoH traffic captures.
"""
kube_instruction= \
"""
Check the following github repo for more information
https://github.com/cslev/doh_cloudlabs
"""

import geni.portal as portal
import geni.rspec.pg as pg

request = portal.context.makeRequestRSpec()

doh_resolvers = {'cloudflare':1,
                 'google':2,
                 'cleanbrowsing':3,
                 'quad9':4}

# doh_resolvers={'cloudflare':1}

for key in doh_resolvers:
    node = request.DockerContainer(str(key))
    node.docker_dockerfile = "https://raw.githubusercontent.com/cslev/doh_docker/master/Dockerfile.noautostart"
    node.docker_tbaugmentation = 'full'
    node.docker_tbaugmentation_update=True




    # node.docker_extimage = "debian:bullseye"
    # node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//docker-debian9-std"
    #install all dependencies
    # node.addService(pg.Execute(shell="bash", command="apt-get update && apt-get install git"))

portal.context.printRequestRSpec()
