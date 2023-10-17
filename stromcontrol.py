from ats import tcl
from ats import tcl
from ats import aetest
from ats.log.utils import banner

from unicon.eal.dialogs import Dialog
from unicon.eal.dialogs import Statement

import time
import logging
import os
import sys
import re
import pdb
import json
import pprint
import socket
import struct
import inspect
import yaml
import random
import CSCwe41070_lib as buglib

from yaml import loader
from pyats.aetest.steps import Steps

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
global uut1

def storm(intf,mark,dev):
    cmd = """int %s
            %s storm-control broadcast level 1.00
            %s storm-control multicast level 1.00
            %s storm-control unicast level 1.00
            storm-control action trap
            no shutdown
            """%(intf,mark,mark,mark)
    status = True         
    try:
        dev.configure(cmd)
    except:
        log.error('Invalid CLI given: %s' % (cmd))
        status = False
    return status

def cc_check(dev):
    status = True         
    try:
        output = dev.execute(r"""show consistency-checker storm-control | n""", timeout=600)
        return output
    except:
        log.error('Invalid CLI given: %s' % (cmd))
        status = False
    return status


@aetest.test    
    def configuring_storm_control_on_the_interfaces(self,testbed,testscript):
        global interface
        log.info(banner("Configuring the storm-control on the ports"))
        # make changes in below line
        interface = [uut1_1_intf1,uut1_1_intf2,uut1_2_intf1,uut1_2_intf2,uut1_3_intf1,uut1_3_intf2]
        # till here
        up = ""
        for i in interface:
            output = buglib.storm(i,up,uut1)
   
    @aetest.test            
    def verifying_CC_before_LC_power_down(self,testbed,testscript):
        log.info(banner("Consistency Check of Line Card before -POWER DOWN- condition"))
        Out = buglib.cc_check(uut1)
        if 'FAILED' in Out:
            log.info("FAIL: CC is getting Failure for storm control configurations on interfaces")
            self.failed()
        else:
            log.info("PASSED: CC is passing successfully")
