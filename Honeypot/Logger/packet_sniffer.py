from scapy.all import sniff, TCP, IP
import logging
from logging.handlers import RotatingFileHandler

log_handler = RotatingFileHandler(
    "mysql_detected.log",
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=5,  # păstrează ultimele 5 fișiere
    encoding="utf-8"
)
log_handler.setLevel(logging.INFO)

formatter = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
log_handler.setFormatter(formatter)

logger = logging.getLogger("mysql_sniffer")
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

def detect_mysql(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(IP):
        if pkt[TCP].dport == 3306 or pkt[TCP].sport == 3306:
            payload = bytes(pkt[TCP].payload)
            if len(payload) > 0:
                decoded = payload.decode(errors="ignore")
                log_msg = f"[MySQL] {pkt[IP].src} -> {pkt[IP].dst} | Payload = {decoded}"
                
                logger.info(log_msg)
                
                print(log_msg)

if __name__ == "__main__":
    sniff(
        filter="tcp port 3306",
        iface="ens33",
        prn=detect_mysql,
        store=0
    )
