from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import TCP, IP, UDP

ports = [25, 80, 53, 443, 445, 8080, 8443]


def SynScan(host):
    ans, unans = sr(IP(dst=host) / TCP(dport=ports, flags="S"), timeout=2, verbose=0)
    print("Open ports at %s:" % host)
    for (s, r,) in ans:
        if s[TCP].dport == r[TCP].sport:
            print(s[TCP].dport)


def DNSScan(host):
    ans, unans = sr(IP(dst=host) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="google.com")), timeout=2, verbose=0)
    if ans:
        print("DNS Server at %s" % host)


host = "8.8.8.8"

SynScan(host)
DNSScan(host)