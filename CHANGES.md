### Code Refactoring Log

### Overview
This document details all the meaningful changes I made during my 3-hour refactor of the legacy user management API, focusing on security, code quality, and maintainability within the assignment constraints.

---

## Issues Identified & Prioritization

Before any changes, I carefully reviewed the codebase and noted the following, in priority order:

1. **SQL Injection vulnerabilities** — All DB access was via direct string formatting!
2. **Plaintext password storage** — Obvious security risk.
3. **No input validation** — Could allow invalid or harmful data.
4. **Mix of response formats and error handling** — Inconsistent, hard to maintain.
5. **Database connection not properly managed** — Can cause app instability.
6. **Monolithic structure** — Business logic and route handling fully mixed together.

Given the brief (3 hours, no new features!), I decided to:
- **Prioritize fixing security** (SQLi, password storage) and stability first,
- **Improve validation and error messages** for API users,
- **Refactor for clarity** (separating concerns using a `user_service.py`).

---

## Concrete Changes

### Critical Security & Stability

- **Parameterised all database queries**  
  (*Why:* Avoid SQL injection, one of OWASP’s top risks.)

- **Implemented bcrypt password hashing on new/sign-up and login**  
  (*Why:* Safeguards user credentials, industry standard.)

- **Added input validation for user and password data**  
  (*Why:* Prevents corrupted/malicious input. Error messages clarify missing/invalid data.)

- **Turned off Flask debug mode by default**  
  (*Why:* Avoids leaking stacktraces or sensitive info in prod.)

- **Ensured all DB connections are closed after use**  
  (*Why:* Reliability and resource management.)

### Code Structure & Organization

- **Moved all CRUD logic into a `user_service.py` “service” layer**  
  (*Why:* Cleaner routes, more maintainable, passes single responsibility test.)

- **All API endpoints now return clear JSON with consistent status and message fields**  
  (*Why:* Makes API consumption and debugging much easier—no more plain strings or silent fails.)

- **Added a simple validation helper and improved test coverage for key cases**
  (*Why:* Keeps checks transparent, discourages silent errors.)

### Testing

- **Added/updated tests (`test_app.py`)** to cover:
  - SQL injection risk
  - Password requirements
  - Login using hashed passwords
  - Direct service-layer invocation

---

## Trade-offs & What’s Left (Given Time Constraints)

- Left out advanced authentication, rate limiting, and full schema validation (stayed within “no new features” and kept it 3-hour realistic).
- Did not convert to ORM, add migrations, or introduce background jobs.
- Kept error handling straightforward for clarity/review.

---

## “If I Had More Time” List

- Add JWT/modern authentication and user roles
- Use Marshmallow or Pydantic for input schemas
- More robust logging & monitoring
- Swagger/API documentation
- Production-like config management and Dockerfile

---

## AI Usage Disclosure

- **Tools:** ChatGPT (OpenAI GPT-4)
- **For:** Advice on safe query patterns, bcrypt integration, and service-layer organization.  
  Rejected advice on JWT/session implementation and ORM conversion (not allowed in specs).
- **All code reviewed and adapted** to this project’s needs with human editing and testing.
