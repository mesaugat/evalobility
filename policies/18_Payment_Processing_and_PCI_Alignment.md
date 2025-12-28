# Payment Processing & PCI Alignment Policy

**Company:** wwktm
**Location:** Kathmandu, Nepal
**Version:** 1.0
**Effective Date:** 2025-11-20
**Owner:** Finance & Security

**Purpose**
Define secure payment processing practices for our e‑commerce platform, aligning with PCI‑DSS principles while minimizing exposure to cardholder data.

**Model and Controls**
Prefer SAQ‑A models (redirect or iFrame) where card data is processed by certified gateways. Do not store or transmit full PAN/CVV. Use tokenization for subsequent charges and refunds. Implement strong authentication, idempotency for payment actions, and logging of all payment events with privacy safeguards.

**Fraud Prevention**
Apply velocity checks, address verification, device fingerprinting (where lawful), and manual review queues for high‑risk transactions. Collaborate with gateways on risk signals. Refunds and payouts require step‑up authentication and dual approvals.

**Compliance and Records**
Maintain accurate invoices, reconcile transactions, and document exceptions. Conduct periodic reviews of gateway configurations and permissions. Train staff handling financial operations on security and privacy expectations.

**Incident Handling**
Payment incidents follow IR procedures, including containment, customer notifications if necessary, and coordination with processors.
