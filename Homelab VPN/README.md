# 🚀 Project 04 – Homelab VPN Using WireGuard on AWS EC2

## 📌 Project Information

| Item               | Details                                      |
| ------------------ | -------------------------------------------- |
| **Project Name**   | Homelab VPN Using WireGuard on AWS EC2       |
| **Project Status** | ✅ Completed                                 |
| **Difficulty**     | ⭐⭐⭐ Intermediate                          |
| **Estimated Time** | *120 Minutes*                                |
| **Date Completed** | *28 Aug 2026*                             |
| **AWS Region**     | *us-east-1 – N. Virginia*                    |

---

# 📖 Project Overview

This project extends the foundation from Project 01 by implementing a secure, encrypted VPN tunnel between a remote client and a home Proxmox lab environment using WireGuard running on an AWS EC2 instance.

The objective was to create a private, segmented network architecture that allows secure remote access to homelab services (Jellyfin, Sonarr, FTP, qBittorrent) while maintaining strict security boundaries between different user roles (Root vs. Standard).

Rather than exposing services directly to the internet, this solution leverages WireGuard's efficiency and simplicity to create a zero-trust architecture with fine-grained access control at the firewall level.

---

# 🎯 Project Objective

Successfully deploy a WireGuard VPN gateway on AWS EC2, configure bidirectional encrypted tunneling between AWS and a home Proxmox WireGuard LXC container, implement role-based firewall policies for different clients, and enable secure remote access to homelab services with proper network segmentation.

---

# 🛠 AWS Services Used

| AWS Service      | Purpose                                           |
| ---------------- | ------------------------------------------------- |
| Amazon EC2       | WireGuard VPN Gateway (Compute)                   |
| Elastic IP       | Static Public IP for VPN Endpoint                 |
| Security Group   | Virtual Stateful Firewall (UDP 51820 only)        |
| Amazon VPC       | Network where the EC2 instance is deployed        |
| Internet Gateway | Allows internet connectivity for VPN endpoint     |

---

# 🧠 Skills Practiced

* AWS Management Console
* Amazon EC2 Configuration
* Elastic IP Association
* Security Groups & NACLs
* WireGuard VPN Configuration
* Linux Networking
* IP Forwarding & Routing
* NAT/MASQUERADE Rules
* iptables/Firewall Configuration
* Proxmox LXC Networking
* VPN Peer Management
* Zero-Trust Security Architecture
* Network Segmentation

---

# 🏗 Architecture

```text
                     Internet
                         │
                         │
                 Elastic IP (Public)
                         │
                 Internet Gateway
                         │
                  Amazon VPC
                         │
                  Public Subnet
                         │
                 Security Group
                 (UDP 51820 only)
                         │
           Amazon EC2 Instance (WireGuard Hub)
                  wg0: 10.200.0.1/24
                         │
                  WireGuard Tunnel
                  (Encrypted UDP)
                         │
                    Home Network
                         │
                    Home Router
                 192.168.1.1/24
                         │
         ┌────────────────┼────────────────┐
         │                │                │
    Proxmox WG LXC    Jellyfin        qBittorrent
    192.168.1.60      192.168.1.150   192.168.1.150
    10.200.0.2/24     
         │
    ┌────┴────┐
 Root      Standard
10.200.0.10 10.200.0.20
Full LAN    Service-only
```

---

# 🔧 Configuration Details

## Operating System

**AWS EC2:** Amazon Linux (with WireGuard, iptables, net-tools)

**WG LXC:** Debian 12 (with WireGuard, iptables, net-tools)

---

## Instance Type

t3.micro *(Free Tier Eligible)*

---

## Public Endpoint

Elastic IP: `<ELASTIC_IP>`

---

## VPN Network

10.200.0.0/24 (separate from home LAN 192.168.1.0/24)

---

## WireGuard Addressing

| Component | Address |
|---|---|
| EC2 wg0 | 10.200.0.1/24 |
| WG LXC wg0 | 10.200.0.2/24 |
| Root client | 10.200.0.10/32 |
| Standard client | 10.200.0.20/32 |

---

## Home Network Addressing

| Component | Address |
|---|---|
| Home Router | 192.168.1.1 |
| WG LXC eth0 | 192.168.1.60 |
| Jellyfin | 192.168.1.150 |
| FTP | 192.168.1.151 |
| Sonarr | 192.168.1.152 |
| qBittorrent | 192.168.1.150 |

---

## Security Group Rules

| Type                   | Protocol | Port  | Source       |
| ---------------------- | -------- | ----- | ------------ |
| WireGuard              | UDP      | 51820 | 0.0.0.0/0    |
| All other inbound      | -        | -     | DENY         |

---

## Root Access Policy

```
Root (10.200.0.10) -> WG LXC -> 192.168.1.0/24 ALLOW (Full LAN Access)
```

---

## Standard Access Policy

```
Standard (10.200.0.20) -> Jellyfin (192.168.1.150:8096)      ALLOW
Standard (10.200.0.20) -> FTP (192.168.1.151:21)             ALLOW
Standard (10.200.0.20) -> qBittorrent (192.168.1.150:8080)   ALLOW
Standard (10.200.0.20) -> All other addresses                DENY
```

---

# 🚀 Deployment Process

The following high-level steps were performed:

## AWS EC2 Setup
1. Launched t3.micro EC2 instance with Amazon Linux 2
2. Associated Elastic IP for static public endpoint
3. Configured Security Group (UDP 51820 only)
4. Enabled IP forwarding on EC2

## WireGuard Configuration on EC2
5. Installed WireGuard on EC2
6. Generated EC2 WireGuard key pair
7. Created `/etc/wireguard/wg0.conf` with peer configurations
8. Enabled and started WireGuard service
9. Verified tunnel initialization

## Home Lab Setup
10. Deployed Proxmox LXC container with WireGuard
11. Configured LXC with dual networking (eth0 + wg0)
12. Generated LXC WireGuard key pair
13. Configured LXC `/etc/wireguard/wg0.conf` with EC2 as peer
14. Enabled IP forwarding on LXC
15. Configured SNAT/MASQUERADE rules on LXC eth0

## Firewall & Access Control
16. Implemented iptables FORWARD rules on LXC
17. Created Root policy (full 192.168.1.0/24 access)
18. Created Standard policy (explicit service allowlist)
19. Set default FORWARD policy to DROP
20. Tested connectivity matrix

## Client Configuration
21. Generated Root client key pair
22. Generated Standard client key pair
23. Created Root client config with AllowedIPs = 10.200.0.0/24, 192.168.1.0/24
24. Created Standard client config with AllowedIPs = 10.200.0.0/24, 192.168.1.150/32, 192.168.1.151/32, 192.168.1.153/32
25. Tested client connections from external network

---

# ⚠ Challenges Encountered

## Challenge 1: Return Traffic Not Reaching Home Devices

**Symptom:** Packets from VPN clients reached home services (e.g., Jellyfin), but responses were not returning to clients.

**Cause:** Home devices have default gateway pointing to 192.168.1.1, but the router does not support or have a static route. When Jellyfin tried to reply to 10.200.0.10, the home router didn't know how to reach the VPN network.

**Resolution:** Implemented SNAT/MASQUERADE on the WG LXC so that packets leaving toward home LAN get source IP rewritten to 192.168.1.60. This makes services believe they're communicating with a normal LAN device. Return traffic targets 192.168.1.60 (the LXC), which then reverses the NAT translation back to the original VPN client IP before sending through the tunnel.

```bash
iptables -t nat -A POSTROUTING -s 10.200.0.0/24 -d 192.168.1.0/24 -o eth0 -j MASQUERADE
```

---

## Challenge 2: Standard Client Receiving No Traffic

**Symptom:** Standard client could send traffic to services, but service responses weren't reaching the client.

**Cause:** iptables FORWARD rules were not configured with `ESTABLISHED,RELATED` stateful tracking, so return packets were hitting the default DROP policy.

**Resolution:** Added a generic stateful ESTABLISHED/RELATED rule early in the FORWARD chain:

```bash
iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
```

This allows all return traffic for connections that were previously authorized.

---

# 📚 Key Concepts Learned

During this project I learned:

* WireGuard architecture and cryptographic design
* The role of `AllowedIPs` as both a cryptographic peer selector and routing selector
* NAT/MASQUERADE and why it's necessary for returning traffic in this topology
* SNAT vs. standard NAT and when each is appropriate
* iptables FORWARD chain policies and stateful connection tracking
* Zero-trust network architecture and explicit service allowlists
* Why `AllowedIPs` on clients provides defense-in-depth but is not a security boundary
* The difference between a routing-only VPN and a firewalled VPN gateway
* Persistent keepalives and their role in NAT traversal
* IP forwarding and how to verify it's enabled (`sysctl net.ipv4.ip_forward`)
* How WireGuard peers form bidirectional tunnels even from behind NAT
* Security group policies vs. firewall rules vs. client-side AllowedIPs

---

# 💡 Lessons Learned

### What went well?

The separation of concerns between EC2 (public endpoint + basic routing) and the WG LXC (firewalling + NAT + home network access) proved to be a clean and maintainable design. Once SNAT was implemented, the home router remained completely unaware of the VPN, which is elegant for a network that doesn't support static routing.

The use of `AllowedIPs` on clients for defense-in-depth, combined with firewall rules on the LXC, created a strong security posture where both layers had to be compromised for an unauthorized access.

---

### What challenged me?

Understanding that NAT was necessary took debugging effort — initially I assumed routing tables alone would be sufficient. The concept that home devices needed to see the WG LXC as the source, not the actual VPN client, required rethinking how packets flow through the network.

Distinguishing between `AllowedIPs` (a routing/crypto mechanism) and firewall rules (the actual security boundary) was a key mental shift.

---

### What did I discover myself?

I realized that a standard `/etc/wireguard/wg-quick.conf` might not persist firewall rules across reboots if using ad-hoc `iptables` commands. Planning to migrate to `nftables` with `systemd` for durability and better auditability is the next step.

I also discovered that the home ISP connection doesn't need to expose WireGuard directly — the AWS EC2 Elastic IP becomes the public endpoint, which is a privacy win and reduces attack surface on the home router.

---

# 🔄 Future Improvements

Possible enhancements include:

* Migrate firewall rules from `iptables` to persistent `nftables` with `systemd` unit files
* Implement DNS forwarding (Pi-hole/AdGuard Home) for FQDN access instead of raw IPs
* Add audit logging for Standard client access attempts
* Create additional client roles (e.g., "Admin" for remote management)
* Implement dynamic client provisioning via a management script
* Set up Grafana/Prometheus monitoring for VPN tunnel statistics
* Add rate limiting on firewall rules to prevent brute-force attempts
* Implement VPN certificate rotation automation
* Create a secondary EC2 instance for high availability
* Document emergency revocation procedures for compromised client keys

---

# 📚 References

* WireGuard Official Documentation (https://www.wireguard.com/)
* Proxmox VE Networking Documentation
* Linux iptables/netfilter Documentation
* Linux Kernel IP Forwarding & Routing

---

# 📝 Personal Reflection

### What went well?

The overall architecture is sound and proven to work reliably. The separation between EC2 (stateless public endpoint) and the LXC (stateful firewall + routing) creates a clean security model. Elastic IP provides a stable endpoint, and WireGuard's performance is excellent even on t3.micro.

---

### What challenged me?

Initially underestimating the complexity of NAT and return traffic flow. Also, debugging which layer (Security Group, iptables, AllowedIPs, routing) was responsible for each behavior required methodical testing. It took days to configure the LXC, including redoing and recreating a new EC2 and LXC instance at times, and even then some issues persisted.

---

### What is my next project?

* Deploy a Flask application on EC2 with Nginx and HTTPS

* Add S3 and RDS to the application (storage + database)

* Implement monitoring (CloudWatch), IAM policies, and security hardening

* Convert manual infrastructure to Terraform

* Build a hybrid cloud project (AWS + Proxmox homelab) with Terraform

> **Note:** These projects represent the current plan and are subject to change during the process as new learning opportunities and challenges emerge during the implementation phase.

---

# ✅ Project Summary

This project successfully implemented a production-ready VPN gateway using WireGuard on AWS EC2, enabling secure and segmented remote access to homelab services without exposing the home ISP connection or individual services to the internet.

By completing this project, I gained deep understanding of network architecture, cryptographic VPN design, and security policy enforcement. The zero-trust approach with role-based access control and defense-in-depth demonstrates professional-grade infrastructure thinking.

This documentation serves as a comprehensive reference for the VPN deployment, a guide for future enhancements, and a portfolio artifact demonstrating advanced cloud networking and security architecture skills.
