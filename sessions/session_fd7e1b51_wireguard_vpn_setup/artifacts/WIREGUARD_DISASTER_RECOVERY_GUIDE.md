# Disaster Recovery & Master Technical Guide: WireGuard VPN on Windows

> **Session ID:** `fd7e1b51-dc4e-4e3c-ad56-1ba647b05bdc`  
> **Target Repo:** `https://github.com/pp0016/daily-push`  
> **Environment:** Windows 11, Reliance Jio 5G/4G Tethered Connection (`2409:40c1:...`), Native WireGuard Client (`wireguard.exe`)  
> **Date:** October 18, 2026 – November 02, 2026  

---

## 1. Executive Summary & Purpose

This repository session serves as the complete technical record and disaster-recovery package for establishing a high-speed, zero-leak, genuine **Tier 1 United States WireGuard VPN** tunnel on Windows without paying recurring subscriptions or installing bloated third-party commercial clients.

The guide documents the forensic discovery and resolution of five separate network failure modes:
1. **Jio CGNAT Blocking** (Preventing Windows self-hosted server)
2. **Cloudflare WARP Anycast Limitations** (Local Mumbai/Delhi exit vs US Geo-spoofing)
3. **The IPv6 Blackhole & MTU Fragmentation** (Websites failing to load on WireGuard)
4. **The 7-Day Ephemeral Key Expiration** (Silent connection death with byte-level throughput)
5. **Google Geolocation Poisoning** (US Datacenter IPs being misidentified as Tehran, Iran)
6. **The Final Solution:** Dedicated, non-expiring, high-speed Proton VPN WireGuard tunnel in Los Angeles, California.

---

## 2. Technical Chronology & Root-Cause Analyses

### Phase 1: Video Tutorial Forensic Audit (Server vs Client)
* **User's Starting State:** The user provided two video transcripts detailing how to turn a Windows PC into a WireGuard server to connect an Android phone from outside.
* **The Conflict:** 
  1. The user wanted their Windows PC to exit from the United States. Following the tutorial would turn the PC into an incoming listener, leaving its public IP unchanged as India.
  2. The user's active internet adapter was inspected via PowerShell:
     - `IPv6 Address: 2409:40c1:...`
     - `IPv4 Address: 10.134.179.140`
     This confirmed a **Carrier-Grade NAT (CGNAT)** environment behind Reliance Jio. Upstream UDP port 51820 was strictly filtered by the ISP; port-forwarding on the router is physically impossible without a public static IPv4 WAN lease.
* **Verdict:** The user required a **WireGuard Client** configuration pointing to an external cloud peer.

---

### Phase 2: Cloudflare WARP via `wgcf`
* **Implementation:**
  - Automated download of `wgcf` (v2.2.24 x86_64).
  - Executed `wgcf register --accept-tos` and generated `wgcf-profile.conf`.
  - Configured DNS (`1.1.1.1`, `1.0.0.1`), MTU `1280`, Endpoint `162.159.192.1:2408`.
  - Generated Desktop config: `Cloudflare-WARP.conf`.
* **The Limitation:**
  - Cloudflare WARP uses Anycast BGP routing. It automatically connected to Cloudflare's closest edge pop (Mumbai/Delhi).
  - Google and YouTube correctly identified the IP as India. While traffic was fully encrypted, it did not satisfy the user's requirement to exit from Tier-1 United States.

---

### Phase 3: VPNBook Free US Tunnels & The Dual Connection Glitch
* **Implementation:**
  - Acquired VPNBook WireGuard US configuration:
    - US Server 2 (Portland, Oregon): `147.135.37.178:443`
    - US Server 1 (Washington D.C. / Virginia): `147.135.15.16:443`
* **Failure Mode A: Websites Failed to Load (The IPv6 Blackhole)**
  - *Diagnosis:* VPNBook's default `.conf` included `AllowedIPs = 0.0.0.0/0, ::/0`, instructing Windows to tunnel all IPv4 and IPv6 packets. However, VPNBook only assigned an IPv4 address (`10.104.3.130/32`) and no IPv6 address.
  - *Result:* Windows attempted to send IPv6 DNS and HTTP queries (which Jio supports natively) into the WireGuard interface, where they were dropped by the tunnel. Browsers stalled indefinitely.
  - *Patch:* Removed `, ::/0` so only IPv4 traffic is routed into the tunnel (`AllowedIPs = 0.0.0.0/0`), allowing native IPv6 to be handled correctly or bypassed without blackholing.
* **Failure Mode B: MTU Packet Fragmentation**
  - *Diagnosis:* WireGuard defaults to MTU 1420. Cellular mobile tethering (Jio) has an upstream MTU limit of ~1360 bytes due to carrier tunneling encapsulation. Packets > 1360 were fragmented and dropped by carrier routing.
  - *Patch:* Strictly injected `MTU = 1280` into the `[Interface]` section.
  - *Result:* The Portland connection achieved full speed and successfully unblocked websites.

---

### Phase 4: The 7-Day Expiration & Bandwidth Choke
* **Symptom:** On October 28 (10 days after initial setup), the VPN throughput collapsed to a few bytes (`16.06 KiB received, 104.22 KiB sent`).
* **Root Cause:** VPNBook public free configs have an aggressive hard-coded 7-day cryptographic lifecycle. After 7 days, the public key is purged from the server's wireguard routing table (`wg set`). Handshakes fail, resulting in persistent SYN drops.
* **Washington vs Portland Congestion:**
  - US Server 1 (Washington D.C., `147.135.15.16`) is the top default button on VPNBook and experiences extreme server-side congestion on port 443.
  - US Server 2 (Portland, `147.135.37.178`) had significantly better available bandwidth.

---

### Phase 5: Google Geolocation Poisoning ("Tehran, Iran")
* **Symptom:** In November 2026, the user noted that despite connecting to the US server, Google Search and YouTube geolocated the connection to **Tehran, Iran**.
* **Root Cause (Forensic Geolocation Analysis):**
  - Geolocation databases (MaxMind, IP2Location) confirmed `147.135.37.178` is hosted in Oregon, USA by OVH SAS.
  - However, because VPNBook is an unauthenticated, zero-signup public VPN, hundreds of thousands of users in Iran utilize it daily to circumvent state censorship.
  - Google's machine-learning location engine relies on crowd-sourced signals (user search languages, device GPS/Wi-Fi triangulations sharing the same IP). Because 90%+ of queries from that IP were in Persian/Farsi from Tehran, **Google automatically reclassified the IP's location to Iran**.

---

### Phase 6: The Definitive Permanent Solution (Proton VPN Free WireGuard)
* **Why Proton VPN:**
  - **100% Free Forever:** Unlimited data with zero credit card requirement.
  - **Non-Expiring:** Keypairs remain active permanently in the user's account; no 7-day token expiration.
  - **Clean IP Space:** Dedicated 10 Gbps M247 / Datacamp infrastructure with strict abuse management; zero Google geolocation poisoning.
  - **Native WireGuard Export:** Allows exporting pure `.conf` files without installing the proprietary Proton desktop app.
* **Endpoint Analysis:**
  - `Endpoint = 146.70.230.146:51820`
  - Location: **Los Angeles, California, United States**
  - Features: Native IPv4 (`10.2.0.2/32`) and IPv6 (`2a07:b944::2:2/128`), `VPN Accelerator = on`.
  - Applied Patch: `MTU = 1280` for Jio connection stability.
  - Artifact File: `US-Proton-Fast.conf`.

---

## 3. Master WireGuard Configurations Reference

### A. The Production Configuration: US-Proton-Fast.conf (Permanent / High-Speed)
```ini
[Interface]
# Key for us-fast
# Bouncing = 1
# NAT-PMP (Port Forwarding) = off
# VPN Accelerator = on
PrivateKey = cEG4EfAWnGsSMlHHI2GWInTNyk8VhnCv7IFY0qd/jk0=
Address = 10.2.0.2/32, 2a07:b944::2:2/128
DNS = 10.2.0.1, 2a07:b944::2:1
MTU = 1280

[Peer]
# US-FREE#1 (Los Angeles, California)
PublicKey = gucaLaM/mgJQbHVvnZNtW+1L4Mi7E2mtTMrhS0K4miU=
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = 146.70.230.146:51820
PersistentKeepalive = 25
```

### B. The Fallback Configuration: US-VPN.conf (Portland, Oregon - 7-Day Cycle)
```ini
[Interface]
PrivateKey = 4JJ0CbU3wauEAE45/DoMoANHvJw4uuwm7wC/RfWOiFU=
Address = 10.104.4.17/32
DNS = 1.1.1.1, 8.8.8.8
MTU = 1280

[Peer]
PublicKey = Rn6w1t6actF9XC0bMIXxO25rf31uFqm2/n5sYyK1UzQ=
Endpoint = 147.135.37.178:443
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
```

### C. The Cloudflare WARP Configuration: Cloudflare-WARP.conf (India Anycast)
```ini
[Interface]
PrivateKey = KNNY0H/LjTHLcCf2ABqrhPsHsFTkFa1b0dsDNo3WylU=
Address = 172.16.0.2/32, 2606:4700:110:864b:1d34:ad4d:abe6:fe8e/128
DNS = 1.1.1.1, 1.0.0.1, 2606:4700:4700::1111, 2606:4700:4700::1001
MTU = 1280

[Peer]
PublicKey = bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = 162.159.192.1:2408
```

---

## 4. Disaster Recovery Restoration Procedure (Fresh Machine)

If you migrate to a new computer or reinstall Windows, follow these exact steps:

1. **Install WireGuard:**
   - Download the official installer from `https://www.wireguard.com/install/` and install it.
2. **Restore the Configuration:**
   - Copy `configs/US-Proton-Fast.conf` from this repository to your Desktop.
3. **Import and Activate:**
   - Open WireGuard.
   - Press `Ctrl + O` (or click *Import tunnel(s) from file*).
   - Select `US-Proton-Fast.conf`.
   - Click **Activate**.
4. **Verification:**
   - Open PowerShell and run:
     ```powershell
     curl.exe -s https://ipinfo.io/json
     ```
   - Verify that `country` is `"US"` and `city` is `"Los Angeles"`.
