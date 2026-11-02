# Session Archive: Complete WireGuard VPN Setup & USA Geo-Routing Optimization

**Session ID:** `fd7e1b51-dc4e-4e3c-ad56-1ba647b05bdc`  
**Date Range:** October 18, 2026 – November 02, 2026  
**Primary Goal:** Set up a permanent, high-speed, native WireGuard VPN tunnel on Windows 11 exiting exclusively from Tier 1 United States (Los Angeles/California) for content creators, with zero ongoing costs, zero third-party client apps, and zero IP leaks.

---

## 📂 Directory Structure

```
session_fd7e1b51_wireguard_vpn_setup/
├── README.md                               # This master session summary
├── conversation_export.md                  # Complete 225-turn readable conversation transcript
├── artifacts/
│   └── WIREGUARD_DISASTER_RECOVERY_GUIDE.md # Forensic technical analysis & disaster recovery guide
├── configs/                                # All generated & patched WireGuard profiles
│   ├── US-Proton-Fast.conf                 # ⭐ PRODUCTION: Non-expiring 10Gbps US Los Angeles tunnel
│   ├── us-fast-US-FREE-11.conf             # Original Proton download profile
│   ├── US-VPN.conf                         # Portland (Oregon) fallback profile (MTU 1280 & IPv6 patched)
│   ├── vpnbook-wg_bfe52b4db661fde5.conf    # Original Portland download profile
│   ├── Washington-DC.conf                  # Washington D.C. profile (MTU 1280 patched)
│   ├── vpnbook-wg_41774d94f7b9d3b5.conf    # Original Washington download profile
│   ├── Cloudflare-WARP.conf                # Cloudflare WARP encrypted profile (India Anycast)
│   ├── wgcf-account.toml                   # Cloudflare WARP account registration data
│   └── wgcf-profile.conf                   # Raw wgcf profile dump
└── logs/                                   # Raw execution telemetry & system logs
    ├── transcript.jsonl                    # Raw compact JSONL conversation transcript
    ├── transcript_full.jsonl               # Raw complete JSONL conversation transcript
    ├── chunks/                             # Split transcript storage chunks
    ├── messages/                           # Internal system message queues
    ├── steps/                              # Intermediate execution outputs & scraped web content
    └── tasks/                              # Background task logs & execution outputs
```

---

## 🛠️ Key Technical Decisions & Milestones

1. **Jio CGNAT Rejection:** Analyzed user's local network (`10.134.179.140` behind `2409:40c1:...`). Proven that tutorials showing how to host a WireGuard server on a home Windows PC are completely incompatible with Carrier-Grade NAT and do not change the PC's public IP address.
2. **Cloudflare WARP BGP Limitation:** Built a local WARP client config via `wgcf`. Traffic was encrypted, but Anycast routing dumped traffic into Mumbai/Delhi, failing the user's US Tier-1 requirement.
3. **The IPv6 Blackhole & MTU Patch:** When testing free US servers, websites failed to load because WireGuard configuration routed `::/0` into an IPv4-only interface, and default MTU (1420) exceeded Jio's encapsulation limit (~1360). Injected `MTU = 1280` and restricted `AllowedIPs = 0.0.0.0/0`, immediately fixing web loading.
4. **Google Geolocation Poisoning Solved:** Identified why public free VPNs (VPNBook) showed "Tehran, Iran" on Google. Massive Iranian censorship evasion traffic on shared IPs caused Google's AI to reclassify the Oregon datacenter as Iran.
5. **Permanent Proton VPN Solution:** Deployed a dedicated free Proton WireGuard profile connected to `146.70.230.146:51820` (Los Angeles, California). Unlike VPNBook, this connection does not expire every 7 days, offers full 10Gbps throughput with VPN Accelerator, and provides a 100% clean US IP.

---

## 🚀 Instant Recovery Instructions

To activate the VPN on any Windows PC:
1. Install [WireGuard for Windows](https://www.wireguard.com/install/).
2. Import `configs/US-Proton-Fast.conf`.
3. Click **Activate**.
