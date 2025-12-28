# Password & Authentication Policy

**Company:** wwktm
**Location:** Kathmandu, Nepal
**Version:** 1.0
**Effective Date:** 2025-06-18
**Owner:** IT & Security

**Purpose**
Standardize password and authentication requirements to reduce the risk of unauthorized access to systems supporting our e‑commerce operations.

**Password Requirements**
Passwords must be at least 12 characters, avoid common words and reused credentials, and prefer passphrases. Password managers are encouraged for employees. Credential sharing is prohibited. Password rotation is required upon compromise or high‑risk exposure rather than arbitrary intervals.

**Storage and Transmission**
Passwords must never be stored in plaintext. Use modern password hashing (e.g., bcrypt/Argon2/PBKDF2 with strong parameters). Authentication traffic must be protected with TLS 1.2+ and modern cipher suites. Rate limiting and lockouts guard against brute force attacks.

**Additional Controls**
Enable MFA, risk‑based authentication, and session management controls (idle timeouts, re‑authentication for sensitive actions). API keys and secrets must be scoped, rotated, and stored in secure vaults; hard‑coding in code or configuration repositories is prohibited.

**Compliance and Review**
Audits and spot checks validate adherence. Violations may result in disciplinary actions and incident response.
