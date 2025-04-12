from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import Node
from mininet.cli import CLI
from mininet.log import setLogLevel

class NATHost(Node):
    """A Node with NAT capabilities."""

    def config(self, **params):
        super().config(**params)
        # Enable IP forwarding, which ensure that node has NAT Capabilities.
        self.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    def terminate(self):
        # Clean up NAT rules
        self.cmd('iptables -F')
        self.cmd('iptables -t nat -F')
        super().terminate()

class CustomTopo(Topo):
    def build(self):
        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Internal hosts h1, h2 with internal IPs
        h1 = self.addHost('h1', ip='10.1.1.2/24')
        h2 = self.addHost('h2', ip='10.1.1.3/24')

        # Hosts with original setup
        h3 = self.addHost('h3', ip='172.16.10.4/24')
        h4 = self.addHost('h4', ip='172.16.10.5/24')
        h5 = self.addHost('h5', ip='172.16.10.6/24')
        h6 = self.addHost('h6', ip='172.16.10.7/24')
        h7 = self.addHost('h7', ip='172.16.10.8/24')
        h8 = self.addHost('h8', ip='172.16.10.9/24')

        # NAT Gateway Host (public IP)
        h9 = self.addHost('h9', cls=NATHost, ip='172.16.10.10/24')

        # Switch-switch links
        self.addLink(s1, s2, cls=TCLink, delay='7ms')
        self.addLink(s2, s3, cls=TCLink, delay='7ms')
        self.addLink(s3, s4, cls=TCLink, delay='7ms')
        self.addLink(s4, s1, cls=TCLink, delay='7ms')
        self.addLink(s1, s3, cls=TCLink, delay='7ms')

        # Host-switch links
        self.addLink(h3, s2, cls=TCLink, delay='5ms')
        self.addLink(h4, s2, cls=TCLink, delay='5ms')
        self.addLink(h5, s3, cls=TCLink, delay='5ms')
        self.addLink(h6, s3, cls=TCLink, delay='5ms')
        self.addLink(h7, s4, cls=TCLink, delay='5ms')
        self.addLink(h8, s4, cls=TCLink, delay='5ms')

        # Connect h9 to s1 (public interface)
        self.addLink(h9, s1, cls=TCLink, delay='5ms')

        # Connect h1 and h2 to h9 as internal network
        self.addLink(h9, h1, cls=TCLink, delay='5ms')
        self.addLink(h9, h2, cls=TCLink, delay='5ms')

def run():
    topo = CustomTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()

    h1, h2, h9 = net.get('h1', 'h2', 'h9')

    # Setup routes on h1 and h2 to use h9 as gateway
    h1.cmd('ip route add default via 10.1.1.1')
    h2.cmd('ip route add default via 10.1.1.1')

    # Enabling STP on switches
    for sw in net.switches:
        sw.cmd(f'ovs-vsctl set Bridge {sw.name} stp_enable=true')
    
    print("\n **** Topology is active with NAT capabilities on Host h9 ****")
    print("\n **** Gateway of h1 and h1 are h9 wiht Public IP : 172.16.10.10 *****")
    print("\n **** Starting CLI to perform give task ****")
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
