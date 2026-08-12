# Skill: UI/UX Pro Max (Premium SaaS Layouts)

This skill contains instructions and rules for building premium, modern, and accessible SaaS user interfaces. Use this skill when modifying dashboards, layouts, buttons, grids, typography, or animation properties.

---

## 1. Typography & Hierarchy (Sora + Inter)
*   **Headings**: Always use the **Sora** font (`var(--font-sora)`) for major page titles, metric numbers, and section headers. Combine with slight negative letter-spacing (`tracking-[-0.03em]`) for a clean, editorial look.
*   **Data & Tables**: Always retain **Inter** or a readable sans-serif for dense data tables, sidebar links, lists, and forms. This ensures readability for users of all ages.

## 2. Color Palette & Dark Mode Contrast
*   **Backgrounds**: Dark mode backgrounds must be near-black (`#0A0A0B`), allowing accents to stand out.
*   **Surfaces**: Elevated dashboard cards and panels should use **Graphite** (`#1F2328` / `bg-surface-secondary`).
*   **Accents**: Use **Scarlet** (`#FF102A`) for primary actions, active states, and focus states. Use **Deep Red** (`#89001E`) for hover transitions and subtle card border glows.
*   **NO Hardcoded Dark Text**: Inside cards or dark panels, never use absolute dark text classes (like `text-slate-900` or `text-neutral-950`) without a dark-mode alternative token.

## 3. Symmetrical Grid Layouts
*   **items-stretch**: Avoid using `items-start` on twin columns or dashboard rows. Always use `items-stretch` so that adjacent cards automatically expand to identical heights.
*   **Safe-Area Bounding (Overscroll Control)**: 
    *   To prevent PWAs from triggering the browser's native "pull-to-refresh" glitch, lock the outer layout (`h-screen overflow-hidden`).
    *   Restrict scrolling to inner panels or lists using `overflow-y-auto` and fixed container heights (e.g., `h-[520px]`).

## 4. Navigation & Active States
*   **Active Pills**: Selection tab pills or active sidebar navigation links must stand out. Active state should use `bg-[var(--brand)] text-white` (or a high-contrast accent color) to avoid white-on-white text readability bugs in dark mode.
*   **Touch Targets**: Mobile buttons and tab triggers must be at least **44x44px** to ensure accessibility under coarse pointers.
