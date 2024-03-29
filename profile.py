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
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab
import geni.rspec.igext as IG

# Create a portal object
pc = portal.Context()
# pc.defineParameter(
    # "osNodeType", "Hardware Type",
    # portal.ParameterType.NODETYPE, "utah-m400",
    # [("", "any available type"), "utah-dl360", "utah-d2950", "utah-m510", "utah-xl170", "utah-m400", "utah-r720"],
    # longDescription="http://docs.cloudlab.us/hardware.html A specific hardware type to use for each node.  Cloudlab clusters all have machines of specific types. When you set this field to a value that is a specific hardware type, you will only be able to instantiate this profile on clusters with machines of that type.  If unset, the experiment may have machines of any available type allocated.")

# pc.defineParameter(
#     "osNodeType", "Hardware Type",
#     portal.ParameterType.NODETYPE, "wisconsin-c220g1",
#     [("", "any available type"), "wisconsin-c220g2", "wisconsin-c220g5", "wisconsin-c240g1", "wisconsin-c240g1"],
#     longDescription="http://docs.cloudlab.us/hardware.html A specific hardware type to use for each node.  Cloudlab clusters all have machines of specific types. When you set this field to a value that is a specific hardware type, you will only be able to instantiate this profile on clusters with machines of that type.  If unset, the experiment may have machines of any available type allocated.")
# params = pc.bindParameters()
# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()


tour = IG.Tour()
tour.Description(IG.Tour.TEXT,kube_description)
tour.Instructions(IG.Tour.MARKDOWN,kube_instruction)
request.addTour(tour)


#for key in doh_resolvers:
    # node = request.DockerContainer(str(key))
    # node.docker_dockerfile = "https://raw.githubusercontent.com/cslev/doh_docker/master/Dockerfile.noautostart"
    # node.docker_extimage = "cslev/doh_docker:noautostart"
    # node.docker_tbaugmentation = 'full'
    # node.docker_tbaugmentation_update=True
    # node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//docker-debian9-std"
    # node.docker_cmd = "apt-get update && apt-get install git && mkdir -p /doh_project/ && git clone https://github.com/cslev/doh_cloudlabs /doh_project"
    #install all dependencies
    # node.addService(pg.Execute(shell="bash", command="apt-get update && apt-get install git"))

# node doh_cloudflare
for i in range(1,5):
  key = str("doh_docker_{}".format(i))
  kube_doh = request.RawPC(str(key))
  kube_doh.hardware_type = "m400" ##ARM
  #kube_doh.hardware_type = "xl170" ##AMD64
  #kube_doh.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:DEB8-64-STD' #<-- does not work
  kube_doh.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
  kube_doh.Site(str(key))

  #START the docker-based version
  kube_doh.addService(pg.Execute(shell="bash", command="/local/repository/cloudlabs_start_docker.sh"))

portal.context.printRequestRSpec()
