#!/usr/bin/env python
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link, TCLink,Intf
from subprocess import Popen, PIPE
from mininet.log import setLogLevel



if '__main__' == __name__:
  setLogLevel('info')
  net = Mininet(link=TCLink)
  key = "net.mptcp.mptcp_enabled"
  value = 1
  p = Popen("sysctl -w %s=%s" % (key, value), shell=True, stdout=PIPE, stderr=PIPE)
  stdout, stderr = p.communicate()
  print("stdout=",stdout,"stderr=", stderr)

  h1 = net.addHost('h1')
  h2 = net.addHost('h2')
  r1 = net.addHost('r1')
  r2 = net.addHost('r2')
  r3 = net.addHost('r3')
  r4 = net.addHost('r4')

  bwlink={'bw':1}
  bwlink2={'bw':0.5}

  net.addLink(r1,h1,cls=TCLink, **bwlink) #r1-eth0 h1-eth0
  net.addLink(r1,r2,cls=TCLink, **bwlink2) #r1-eth1 r2-eth0
  net.addLink(r1,r4,cls=TCLink, **bwlink) #r1-eth2 r2-eth0

  net.addLink(r3,h1,cls=TCLink, **bwlink) #r3-eth0 h1-eth1
  net.addLink(r3,r4,cls=TCLink, **bwlink2) #r3-eth1 r4-eth0
  net.addLink(r3,r2,cls=TCLink, **bwlink) #r3-eth2 r2-eth1

  net.addLink(r2,h2,cls=TCLink, **bwlink) #r2-eth2 h2-eth0
  net.addLink(r4,h2,cls=TCLink, **bwlink) #r4-eth2 h2-eth1

  net.build()

  h1.cmd("ifconfig h1-eth0 0")
  h2.cmd("ifconfig h2-eth0 0")
  r1.cmd("ifconfig r1-eth0 0")
  r2.cmd("ifconfig r2-eth0 0")
  r3.cmd("ifconfig r3-eth0 0")
  r4.cmd("ifconfig r4-eth0 0")
  
  h1.cmd("ifconfig h1-eth1 0")
  h2.cmd("ifconfig h2-eth1 0")
  r1.cmd("ifconfig r1-eth1 0")
  r2.cmd("ifconfig r2-eth1 0")
  r3.cmd("ifconfig r3-eth1 0")
  r4.cmd("ifconfig r4-eth1 0")
  
  r1.cmd("ifconfig r1-eth2 0")
  r2.cmd("ifconfig r2-eth2 0")
  r3.cmd("ifconfig r3-eth2 0")
  r4.cmd("ifconfig r4-eth2 0")

  r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
  r2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
  r3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
  r4.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

  h1.cmd("ifconfig h1-eth0 10.0.0.2 netmask 255.255.255.0")
  h1.cmd("ifconfig h1-eth1 10.0.1.2 netmask 255.255.255.0")

  h2.cmd("ifconfig h2-eth0 10.0.4.2 netmask 255.255.255.0")
  h2.cmd("ifconfig h2-eth1 10.0.5.2 netmask 255.255.255.0")

  r1.cmd("ifconfig r1-eth0 10.0.0.1 netmask 255.255.255.0")
  r1.cmd("ifconfig r1-eth1 10.0.2.1 netmask 255.255.255.0")
  r1.cmd("ifconfig r1-eth2 10.0.6.1 netmask 255.255.255.0")

  r2.cmd("ifconfig r2-eth0 10.0.2.2 netmask 255.255.255.0")
  r2.cmd("ifconfig r2-eth1 10.0.7.2 netmask 255.255.255.0")
  r2.cmd("ifconfig r2-eth2 10.0.4.1 netmask 255.255.255.0")

  r3.cmd("ifconfig r3-eth0 10.0.1.1 netmask 255.255.255.0")
  r3.cmd("ifconfig r3-eth1 10.0.3.1 netmask 255.255.255.0")
  r3.cmd("ifconfig r3-eth2 10.0.7.1 netmask 255.255.255.0")

  r4.cmd("ifconfig r4-eth0 10.0.6.2 netmask 255.255.255.0")
  r4.cmd("ifconfig r4-eth1 10.0.3.2 netmask 255.255.255.0")
  r4.cmd("ifconfig r4-eth2 10.0.5.1 netmask 255.255.255.0")
  
  h1.cmd("ip rule add from 192.168.0.1 table 1")
  h1.cmd("ip rule add from 192.168.1.1 table 2")
  h1.cmd("ip route add 192.168.0.0/24 dev h1-eth0 scope link table 1")
  h1.cmd("ip route add default via 192.168.0.2 dev h1-eth0 table 1")
  h1.cmd("ip route add 192.168.0.0/24 dev h1-eth1 scope link table 2")
  h1.cmd("ip routeadd default via 192.168.0.2 dev h1-eth1 table 2")
  h1.cmd("ip route add default scope global nexthop via 192.168.0.2 dev h1-eth0")
  h1.cmd("ip route add default scope global nexthop via 192.168.0.2 dev h1-eth1")
  
  h2.cmd("ip rule add from 192.168.7.2 table 1")
  h2.cmd("ip rule add from 192.168.6.2 table 2")
  h2.cmd("ip route add 192.168.7.0/24 dev h1-eth0 scope link table 1")
  h2.cmd("ip route add default via 192.168.7.2 dev h1-eth0 table 1")
  h2.cmd("ip route add 192.168.6.0/24 dev h1-eth1 scope link table 2")
  h2.cmd("ip routeadd default via 192.168.6.2 dev h1-eth1 table 2")
  h1.cmd("ip route add default via 192.168.6.2 dev h1-eth0 table 2")
  h1.cmd("ip route add default scope global nexthop via 192.168.7.2 dev h1-eth0")
  
  CLI(net)
  net.stop()
  
  1,21		TOP
