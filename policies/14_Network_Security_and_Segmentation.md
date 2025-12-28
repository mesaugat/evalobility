# Network Security & Segmentation Policy

**Company:** wwktm
**Location:** Kathmandu, Nepal
**Version:** 1.0
**Effective Date:** 2024-09-19
**Owner:** Infrastructure & Security

**Purpose**
Establish controls to protect networked systems that support our e‑commerce operations, reduce attack surface, and prevent lateral movement.

**Architecture**
Define zones: Public (web frontends), DMZ (reverse proxies/WAF), Application, Data, and Admin. Segmentation and firewall rules enforce least privilege. VPN is required for administrative access. Egress filtering prevents unauthorized data exfiltration.

**Controls**
Deploy WAF, IDS/IPS, DDoS protections, and secure DNS. Apply secure routing, hardened device configurations, and patching. Monitor network flows and configuration changes, with alerting for anomalies and policy violations.

**Remote Connectivity**
Strong authentication, encryption, and endpoint checks for remote access. Third‑party connections are documented and controlled via gateways. Regular reviews ensure alignment with evolving threats.

**Testing and Maintenance**
Perform periodic penetration tests, configuration audits, and tabletop exercises for network incidents. Findings are tracked to closure.
