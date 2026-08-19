---
name: db-migration-helper
description: Strict rules for database schema migrations, seed scripts, and tenant isolation: non-destructive nullable-first migrations, handwritten enum/type conversions, mandatory factoryId/organizationId scoping, Row-Level Security policies, deriving tenant context from the session never the client payload, and consistent hashing across entry points. Use when editing schema.prisma, SQL migrations, seed scripts, or server-side authorization checks.
---

# Skill: DB Migration & Tenancy Hardening

This skill contains strict rules and instructions for writing database schema migrations, seeding scripts, and enforcing Row-Level Security (RLS) or tenant isolation. Use this skill when modifying `schema.prisma`, SQL migrations, seed scripts, or server-side authorization checks.

---

## 1. Defensive Database Migrations
*   **Non-Destructive Changes**: Never drop a column or rename a table if it contains active data. Introduce new columns as **nullable** (`?`) or with sensible defaults.
*   **BOM/Status Migrations**: When converting a strict column (like a non-null enum) to nullable or a different type, write a handwritten migration that keeps existing records in their legacy state (e.g. mapping to `OFF` explicitly) instead of mass-resetting to null.

## 2. Multi-Tenant Isolation & RLS
*   **Always Scope by Tenant**: Every query or mutation on workspace data (Orders, Inspections, Checklists, Inventory, Invoices) **must** be scoped by `factoryId` or `organizationId`.
*   **RLS Policies**: For database tables storing tenant-sensitive data (e.g. `OrderDraft`, `Fitment`, `Agreement`), always generate and deploy Row-Level Security (RLS) policies.
*   **Derive from Auth**: Never trust a `factoryId` or `organizationId` passed directly from the client payload. Derive the tenant context strictly from the authenticated session (session token or authenticated API key).

## 3. Seed & Script Integrity
*   **No Code Duplication**: Avoid duplicating helper logic (like password/PIN hashing or role creation) between server actions, seed scripts, and database migrations.
*   **Salt Checks**: Ensure PIN hashing methods (`hashPin`) use a consistent salt strategy across all entry points to prevent login mismatches.
