from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
import os
import subprocess
import time

P4_SWITCH_JSON = "iisyswitch.json/iisyswitch.json"
THRIFT_PORT = 9090
SWITCH_NAME = 's1'
COMMANDS_FILE = 'commands.txt'

def setup():
    setLogLevel('info')

    print("[INFO] Starting Bmv2 simple switch ")
    bmv2_process = subprocess.Popen(
        [
            "simple_switch", "--log-console", "--thrift-port", str(THRIFT_PORT), "-i", "0@veth0", "-i", "1@veth1", P4_SWITCH_JSON 
        ]
    )


    time.sleep(2)
    print("[INFO] Loading flow rules....")

    subprocess.run(
        [
            "simple_switch_CLI", "--thrift-port", str(THRIFT_PORT), "--input", COMMANDS_FILE
        ]
    )
    return bmv2_process


def run_mininet():
    print("[INFO] Launching Mininet topology")
    net = Mininet(controller = None, switch = OVSKernelSwitch, link = TCLink)
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    
    s1 = net.addSwitch(SWITCH_NAME, failMode = 'standalone')

    net.addLink(h1, s1)
    net.addLink(h2, s1)

    h1.setIP('10.0.0.1/24')
    h2.setIP('10.0.0.2/24')
    
    print("[INFO] Sending ping with crafted ToS (DiffServ) field")
    h1.cmd("ping -c 3 -Q 0xb0 10.0.0.2")
    CLI(net)
    net.stop()


if __name__ == "__main__":
    bmv2 = setup()
    try:
        run_mininet()
    finally:
        print("[INFO] Cleaning up BmV2")
        bmv2.terminate()




