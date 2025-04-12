# CN_ASS_3

## Task 1

### Create topology
```bash
$ sudo python Task1.py
```

### Ping hosts
```bash
mininet> h3 ping -c 3 h1
```

---

## Task 2

### Create topology with NAT capabilities on host h9
```bash
$ sudo python Task2.py
```

#### Configure h9 so that h1, h2, and h9 can ping each other
```bash
mininet> h9 ip link add name br0 type bridge
mininet> h9 ip link set h9-eth1 master br0
mininet> h9 ip link set h9-eth2 master br0
mininet> h9 ip link set br0 up
mininet> h9 ip addr add 10.1.1.1/24 dev br0
```

#### Configure NAT on h9 so internal hosts can ping external hosts
```bash
mininet> h9 iptables -t nat -A POSTROUTING -s 10.1.1.0/24 -o h9-eth0 -j MASQUERADE
```

#### Run iperf3 server on h1
```bash
mininet> h1 iperf -s > /dev/null 2>&1 &
```

#### Configure NAT on h9 so external hosts can connect to iperf3 server running on internal host
```bash
mininet> h9 iptables -t nat -A PREROUTING -p tcp --dport 5001 -j DNAT --to-destination 10.1.1.2:5001
mininet> h9 iptables -A FORWARD -p tcp -d 10.1.1.2 --dport 5001 -j ACCEPT
```

#### Run iperf3 client on host h6 for 120 seconds
```bash
mininet> h6 iperf -c h9 -t 120
```

### Similarly, start iperf3 server on external host h8. NAT is already configured on h9 so internal hosts can connect to external hosts.

---

## Task 3

### Compile code
```bash
$ cd Task3
$ gcc prog3.c node0.c node1.c node2.c node3.c nodeutil.c -o prog3
```

### Execute program
```bash
$ ./prog3
```

---

## Python Requirement
> **Note**: All the above code was tested on Debian Testing (Kali 2025.1) system.
