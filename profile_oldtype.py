kube_description= \
"""
Levi: Four pure Ubuntu 18.04 VMs running DoH traffic captures.
"""
kube_instruction= \
"""
Check the following github repo for more information
https://github.com/cslev/doh_cloudlabs
"""


# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab
import geni.rspec.igext as IG
import geni.rspec.pg as RSpec

# Create a portal object
pc = portal.Context()
pc.defineParameter(
    "osNodeType", "Hardware Type",
    portal.ParameterType.NODETYPE, "utah-m400",
    [("", "any available type"), "utah-dl360", "utah-d2950", "utah-m510", "utah-xl170", "utah-m400", "utah-r720"],
    longDescription="http://docs.cloudlab.us/hardware.html A specific hardware type to use for each node.  Cloudlab clusters all have machines of specific types. When you set this field to a value that is a specific hardware type, you will only be able to instantiate this profile on clusters with machines of that type.  If unset, the experiment may have machines of any available type allocated.")
params = pc.bindParameters()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()


#rspec = RSpec.Request()
tour = IG.Tour()
tour.Description(IG.Tour.TEXT,kube_description)
tour.Instructions(IG.Tour.MARKDOWN,kube_instruction)
request.addTour(tour)

# doh_resolvers = {'cloudflare':1,
#                  'google':2,
#                  'cleanbrowsing':3,
#                  'quad9':4}

doh_resolvers={'cloudflare':1}

interfaces = []
for key in doh_resolvers:
    # node doh_cloudflare
    kube_doh = request.RawPC(str(key))
    kube_doh.hardware_type = params.osNodeType
    kube_doh.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
    kube_doh.Site(str(key))

    iface0 = kube_doh.addInterface('interface-0')
    iface0.component_id="eth1"
    ip_address_end = doh_resolvers[key]
    ip_address_base="10.10.0."
    iface0.addAddress(pg.IPv4Address(ip_address_base + str(ip_address_end),"255.255.255.0"))
    interfaces.append(iface0)

    bs0 = kube_doh.Blockstore('bs0', '/mnt/extra')
    bs0.size = '1GB'
    bs0.placement = 'NONSYSVOL'

    #start doh_capture
    kube_doh.addService(pg.Execute(shell="bash", command="/local/repository/cloudlabs_start.sh "+str(doh_resolvers[key])))

# connecting containers
link_m = request.Link('link-0')
link_m.Site('undefined')
link_m.addInterface(iface0)
for iface in interfaces:
    link_m.addInterface(iface)

# Print the generated rspec
pc.printRequestRSpec(request)
