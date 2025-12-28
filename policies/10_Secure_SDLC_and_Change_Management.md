# Secure SDLC & Change Management Policy

**Company:** wwktm
**Location:** Kathmandu, Nepal
**Version:** 1.0
**Effective Date:** 2025-02-28
**Owner:** Engineering & Security

**Purpose**
Integrate security controls into the software development lifecycle (SDLC) and govern changes to production systems to reduce risk and improve reliability of our e‑commerce platform.

**Lifecycle Stages**
Requirements (include security and privacy), threat modeling, secure design review, secure coding practices, peer code review, automated testing (SAST/DAST), QA/UAT, controlled deployment, and post‑release monitoring. Security sign‑off is required for high‑risk features.

**Change Control**
All production changes require tickets, documented impact, approvals, and rollback plans. Releases are versioned, and release notes are published. Emergency changes are permitted with expedited approvals and post‑implementation review.

**Standards and Tooling**
Follow OWASP Top 10 guidance, use dependency scanning and supply chain security checks, protect secrets, and enforce CI/CD gates. Infrastructure as code (IaC) changes undergo the same rigor. Observability and logging must be in place before release.

**Continuous Improvement**
Defects and incidents feed back into requirements and design. Training keeps developers current on secure practices. Metrics include defect escape rate, review coverage, and control effectiveness.
