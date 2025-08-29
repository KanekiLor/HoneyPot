# HoneyPot MITM & Data Exfiltration Simulation

This project demonstrates **HTTPS/HTTP traffic interception (MITM)** and a **brute-force + data exfiltration scenario** across 3 virtual machines:

- **VM1 = Malware (Attacker)** – sends requests, runs brute-force, performs exfiltration  
- **VM2 = Honeypot (Interceptor)** – routes traffic through `mitmproxy` (transparent mode) and logs it  
- **VM3 = Server** – receives the exfiltrated data  

---

##  Architecture

```
VM1 (malware) → VM2 (honeypot/interceptor + mitmproxy) → VM3 (server)
HTTP/HTTPS REDIRECT: 80 / 443 / 4443 → 8080
```

---

##  Requirements

**VM1 (Malware):**
- Any client (e.g., Python `requests`, `curl`)  
- **Default gateway = VM2 IP**  

**VM2 (Honeypot/Interceptor):**
- Ubuntu 20.04+  
- `mitmproxy`, `iptables` (or compatible)  
- IP forwarding enabled  

**VM3 (Server):**
- Simple HTTP/HTTPS endpoint to receive exfiltrated data  

---

##  Configuration

### 1) VM1 (Malware): route traffic via VM2
```bash
sudo ip route replace default via <IP_VM2>
```

---

### 2) VM2 (Honeypot/Interceptor): enable forwarding + redirect

#### Editable Variables
```bash
INGRESS_IF=ens33      # traffic from VM1 (malware) to VM2
EGRESS_IF=ens33       # traffic leaving VM2 towards Internet/VM3
MITM_PORT=8080        # port where mitmproxy listens
```

#### Step 1: Enable IP forwarding (runtime + persistent)
```bash
sudo sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
```

#### Step 2: Redirect HTTP/HTTPS to mitmproxy (transparent mode)
```bash
sudo iptables -t nat -A PREROUTING -i "$INGRESS_IF" -p tcp --dport 80   -j REDIRECT --to-port "$MITM_PORT"
sudo iptables -t nat -A PREROUTING -i "$INGRESS_IF" -p tcp --dport 443  -j REDIRECT --to-port "$MITM_PORT"
sudo iptables -t nat -A PREROUTING -i "$INGRESS_IF" -p tcp --dport 4443 -j REDIRECT --to-port "$MITM_PORT"
```

#### Step 3: NAT outbound traffic
```bash
sudo iptables -t nat -A POSTROUTING -o "$EGRESS_IF" -j MASQUERADE
```

---

### 3) VM2: Run mitmproxy in transparent mode

Save TLS keys for Wireshark decryption:
```bash
mkdir -p ~/.mitmproxy
touch ~/.mitmproxy/sslkeylogfile.txt
chmod 600 ~/.mitmproxy/sslkeylogfile.txt
export SSLKEYLOGFILE="$HOME/.mitmproxy/sslkeylogfile.txt"
```

Run mitmproxy:
```bash
sudo mitmproxy --mode transparent --showhost
```

 In Wireshark (VM2): `Edit → Preferences → Protocols → TLS → (Pre)-Master-Secret log filename = ~/.mitmproxy/sslkeylogfile.txt`

---

##  Scenarios

### 1) MITM HTTPS (encrypted traffic)
- VM1 generates HTTPS traffic towards a service/server  
- VM2 intercepts ports 80/443/4443 and redirects them to mitmproxy (8080)  
- mitmproxy decrypts and logs requests/responses  

### 2) Brute-force DB + Exfiltration
- VM1 performs a brute-force (dictionary) attack against DB/service on VM2  
- After retrieving data, VM1 exfiltrates it to VM3  
- VM2 (with mitmproxy) logs the entire flow (attack + exfiltration)  

---

##  Notes

- Ensure VM1 actually routes through VM2 (default gateway must be VM2)
- If you're using a self-signed certificate you must set mitmproxy to --ssl-insecure  
- Persisting iptables rules: The iptables rules are restored at boot using a custom **systemd service** instead of `setup-routes`.


---

## Conclusion
This setup allows simulating a **realistic attack scenario** where an attacker (VM1) communicates through a honeypot (VM2) before exfiltrating sensitive data to an external server (VM3).  
The honeypot transparently intercepts and logs both **encrypted HTTPS traffic** and **malicious exfiltration payloads**, providing valuable insights into attacker behavior.
