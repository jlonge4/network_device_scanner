import time

from scapy.all import ARP, Ether, srp
import sys

from requests import get

__version__ = "1.0"


class Macpyoui:
    def __init__(self, api):
        self.api = api


site = "https://api.macvendors.com/"
data = Macpyoui(site)

def searchmac(mac_addy):
    macsend = data.api + mac_addy
    vendorsearch = get(macsend).text
    return vendorsearch


target_ip = "192.168.1.1/24"
# IP Address for the destination
# create ARP packet
arp = ARP(pdst=target_ip)
# create the Ether broadcast packet
# ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
# stack them
packet = ether/arp

result = srp(packet, timeout=3, verbose=0)[0]

# a list of clients, we will fill this in the upcoming loop
clients = []
vendors_list = []


for sent, received in result:
    # for each response, append ip and mac address to `clients` list
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})

# print clients
print("Available devices in the network:")
print("IP" + " "*18+"MAC" + " "*18+"MAN")

i = 0
for client in clients:
    manufacturer = searchmac(client['mac'])
    time.sleep(0.05)
    print("{:16}    {}".format(client['ip'], client['mac']) + " "*4 + manufacturer + '\n' + '-'*52 )
    time.sleep(1)

