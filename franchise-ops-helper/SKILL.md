---
name: franchise-ops-helper
description: Architecture patterns for a multi-outlet Franchise Operating System: franchisor-HQ vs franchisee-outlet isolation, white-labeled tenant lookups, SOP validation gates, photo audit engines, franchise health scoring, approved-vendor procurement and price-leakage detection. Use when modifying outlet configuration, command center dashboards, audit engines, SOP checklists, or outlet provisioning.
---

# Skill: Franchise Operations OS (Multi-Outlet Management)

This skill provides guidelines and patterns for implementing features in a Franchise Operating System (Franchise OS). Use it when modifying outlet configurations, command center dashboards, audit engines, SOP checklists, or provisioning processes.

---

## 1. Multi-Tenant vs. Hierarchy Architecture
*   **The Model**: The architecture must separate:
    *   **Franchisor HQ**: Can view all outlets, read aggregated sales data, configure master SOP libraries, and push audit templates.
    *   **Franchisee Outlet**: Isolated workspace where users see only their local sales, local attendance, and assign tasks.
*   **White-Labeling**: Never hardcode client or brand names. Look up references dynamically using the tenant's `factory.name`.

## 2. SOP & Audit Engine
*   **SOP Validation Gates**: Force opening/closing sequences. For example, a store status cannot change to "OPEN" until the opening checklist (cleaning, attendance, device checks) is fully submitted.
*   **Photo Audits**: Audit submissions must support photo uploads (e.g., visual merchandising verification) with structured violation tags and corrective actions.
*   **Franchise Health Score**: Compile a numeric rating (0-100) per outlet based on:
    *   SOP compliance (checklists submitted on time).
    *   Audit/Inspection scores.
    *   Sales targets achieved.
    *   Customer/Incident complaints resolved.

## 3. Procurement & Price Auditing
*   **Approved Vendors**: Maintain a central registry of HQ-approved suppliers and price sheets.
*   **Leakage Detection**: Flag transactions if an outlet records purchases of supplies at rates above the HQ approved vendor agreement list (e.g., buying milk at 15% above approved rate).

## 4. Expansion & Automated Provisioning
*   **One-Click Launch**: Creating a new outlet must be fully automated:
    *   Generate a new workspace, default store manager account, and assign system roles.
    *   Seed the store with HQ's global SOP templates, audit checklists, and approved supplier catalogs in one database transaction.
