# CN_ASS_3

##Task 1 - 
### create topology -
'''
$ sudo python Task1.py
'''


### Ping hosts -
'''
mininet>h3 ping -c 3 h1
'''

## Task 2 -
###Create topology with NAT Capabilities on host h9 -
''' bash
$ sudo Task2.py
'''
###### Configure h9 so that h1, h2, and h9 are ping each-other

mininet> h9 ip link add name br0 type bridge
mininet> h9 ip link set h9-eth1 master br0
mininet> h9 ip link set h9-eth2 master br0
mininet> h9 ip link set br0 up
mininet> h9 ip addr add 10.1.1.1/24 dev br0

##### configure NAT on h9 such that internal host ping extenal host

mininet> h9 iptables -t nat -A POSTROUTING -s 10.1.1.0/24 -o h9-eth0 -j MASQUERADE


#### run iperf3 server on h1

mininet> h1 iperf -s > /dev/null 2>&1 &

#### configure NAT on h9 such that external host connect with iperf3 server running on h9

mininet> h9 iptables -t nat -A PREROUTING -p tcp --dport 5001 -j DNAT --to-destination 10.1.1.2:5001
mininet> h9 iptables -A FORWARD -p tcp -d 10.1.1.2 --dport 5001 -j ACCEPT

#### run iperf3 client on host h6 for 120 second

mininet> h6 iperf -c h9 -t 120


### similary start iperf3 server on external host h8 and we already configure NAT on h9 such that internal host can connect with external host.

### Task 3
##### compile code

$ cd Task3
$ gcc prog3.c node0.c node1.c node2.c node3.c nodeutil.c -o prog3

###### execute program

$ ./prog3
```
##### python requirement-
Note - all the above code tested on Debian Testing (Kali 2025.1) system.
