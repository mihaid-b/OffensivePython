from scapy.all import *
from scapy.layers.inet import ICMP


def printData(x):
    d = chr(x[ICMP].code)
    print(d,end="",flush=True)

sniff(filter="icmp", prn=printData)
