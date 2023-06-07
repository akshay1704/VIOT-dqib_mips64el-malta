"""Used for virtual IoT device test
"""
import os
# Import the Portal object.
import geni.portal as portal
# Emulab specific extensions.
import geni.rspec.emulab as emulab
# Import the ProtoGENI library.
import geni.rspec.pg as rspec


# Create a portal context, needed to defined parameters
pc = portal.Context()
#
# This is a git repo with my dot files and junk I like.
#


imageList = [('urn:publicid:IDN+emulab.net+image+Super-Fuzzing:vm-with-mac', 'UBUNTU 18.04 with packages'),
#     ('urn:publicid:IDN+clemson.cloudlab.us+image+emulab-ops:UBUNTU20-PPC-OSCP-U', '20.04 PPC'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD', 'UBUNTU 18.04'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU20-64-STD', 'UBUNTU 20.04')]

pc.defineParameter("osImage", "Select OS image",
                   portal.ParameterType.IMAGE,
                   imageList[1], imageList,
                   longDescription="")

params = pc.bindParameters()

USER = os.environ["USER"]



DEPLOY_ENV = "sudo sh /local/repository/env.sh"
# RUN_INSTANCE = "sudo ./50_run_controller_relaunch_main_schedule_versatilepb.sh eth0 test 600 600 36000"
RUN_INSTANCE = "sudo sh /local/repository/run.sh"

# Create a Request object to start building the RSpec.
request = portal.context.makeRequestRSpec()


# Add a raw PC to the request.
node = request.RawPC("node")
node.hardware_type = "m510"
# node.hardware_type = "d750"
# node.hardware_type = "ibm8335"
# node.hardware_type = "c240g5"
iface = node.addInterface()
node.disk_image = params.osImage


node.addService(rspec.Execute(shell="bash", command=DEPLOY_ENV))
node.addService(rspec.Execute(shell="bash", command=RUN_INSTANCE))

portal.context.printRequestRSpec(request)
