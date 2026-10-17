---
name: workflow-new-screen
description: Build or redesign a UI screen using the project design system: inspect system and Figma, design, implement, screenshot, compare, fix. Use when asked to design, redesign, or build a page, dashboard, or screen.
---

# workflow-new-screen

Announce "Using workflow-new-screen to <purpose>". The impeccable skill governs craft; the project design system wins on tokens and components.

## Flow
1. Read the project design-system skill or doc. List tokens and existing components to reuse.
2. If Figma is authorized, read the relevant frames and variables (figma-use, figma-design-to-code). If not, say so and work from the design system.
3. Define states up front: loading, empty, error, permission denied, mobile.
4. Implement with existing components. Add a component only when none fits.
5. Run qa-loop: screenshot desktop and mobile, compare with the design.
6. Fix and re-check the failing items.
7. Optional: push the live UI back to Figma with figma-generate-design for review.

## Stop
When all states exist and the screenshot matches the intended design.
