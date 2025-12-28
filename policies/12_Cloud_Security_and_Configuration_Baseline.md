# Cloud Security & Configuration Baseline Policy

**Company:** wwktm
**Location:** Kathmandu, Nepal
**Version:** 1.0
**Effective Date:** 2025-08-07
**Owner:** Cloud Engineering & Security

**Purpose**
Define secure configuration baselines and operational practices for cloud services hosting our e‑commerce platform to prevent misconfigurations and reduce risk.

**Baselines**
No public buckets for sensitive data; enforce least‑privilege security groups; separate IAM roles for admin, service, and CI/CD; enable logging (cloud audit logs, object access logs); encrypt storage and databases at rest; require TLS for all endpoints.

**Posture Management**
Use Cloud Security Posture Management (CSPM) for continuous checks. Critical misconfigurations trigger automated remediation or immediate tickets. Infrastructure as code ensures repeatable, reviewable changes.

**Secrets & Keys**
Manage keys in KMS, rotate regularly, restrict access, log key operations, and avoid hard‑coding secrets. Use versioned parameter stores and enforce least privilege.

**Resilience & Cost Controls**
Implement backups, disaster recovery patterns, autoscaling, and budget alerts. Tag resources for ownership and lifecycle management. Regular reviews align architecture with business goals and security controls.
