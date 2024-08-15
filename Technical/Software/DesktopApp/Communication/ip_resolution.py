import scapy.all as scapy

def find_robot_ip_address(mac_id):
    target_ip = "192.168.43.1/24"
    arp = scapy.ARP(pdst=target_ip)
    ether = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = scapy.srp(packet, timeout=3, verbose=0)[0]
    clients = []
    for sent, received in result:
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})
    for client in clients:
        print(client)
        mac_found=client['mac'].split(":")
        mac_found_str="".join(mac_found)
        if mac_found_str == mac_id:
            return client['ip']
        else:
            return "192.168.43.232"
