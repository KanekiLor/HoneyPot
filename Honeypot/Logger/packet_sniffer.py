from scapy.all import *

def detect_mysql(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(IP):
        if pkt[TCP].dport == 3306 or pkt[TCP].sport == 3306:
            payload = bytes(pkt[TCP].payload)
            if len(payload)> 0 :
                decoded = payload.decode(errors="ignore")
                print(f"[MySQL] {pkt[IP].src} la {pkt[IP].dst} | Payload = {decoded}")
            
sniff(filter="tcp port 3306", prn=detect_mysql, store=0)
