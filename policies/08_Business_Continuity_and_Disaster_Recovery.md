# Business Continuity & Disaster Recovery (BC/DR) Policy

**Company:** wwktm
**Location:** Kathmandu, Nepal
**Version:** 1.0
**Effective Date:** 2024-08-22
**Owner:** Operations & Security

**Purpose**
Ensure resilience of critical e‑commerce services against disruptions, including infrastructure failures, cyber incidents, natural disasters, and vendor outages, and define recovery objectives and testing.

**RTO/RPO Targets**
Core commerce platform: RTO ≤ 4 hours, RPO ≤ 1 hour.
Payments: RTO ≤ 2 hours, RPO ≤ 15 minutes.
Customer support systems: RTO ≤ 8 hours, RPO ≤ 4 hours.

**Strategies**
Use multi‑AZ/cloud redundancy, automated backups, replication, and failover. Maintain clear runbooks and contact lists. Prioritize restoration by business impact. Coordinate with logistics and payment partners for continuity. Alternative communication channels must be prepared in case of primary platform failure.

**Exercises and Maintenance**
Conduct semi‑annual failover tests and quarterly backup restore tests. Review vendor SLAs and capacity plans annually. Post‑test reports capture issues, remediation owners, and due dates. Update plans after organizational or architectural changes.

**Governance**
BC/DR plans are approved by leadership and tested regularly. Deviations require documented risk acceptance. Lessons learned feed back into architecture and process improvements.
