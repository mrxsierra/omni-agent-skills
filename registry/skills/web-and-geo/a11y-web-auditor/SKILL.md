---
name: a11y-web-auditor
description: Audits web applications for accessibility compliance (WCAG 2.1), responsive layout behavior, semantic markup, and Core Web Vitals performance.
---

# 🌐 A11y Web Auditor

The **A11y Web Auditor** evaluates web applications for accessibility compliance, semantic structure, responsive layout stability, and Core Web Vitals performance.

## 1. Inputs & Context Required
- **Target Application:** Local HTML/CSS/JS files, component templates, or running local development server URL.
- **Accessibility Standard:** Target compliance tier (e.g. WCAG 2.1 Level AA).
- **Target Viewports:** Breakpoint specifications (e.g. mobile 375px, tablet 768px, desktop 1440px).

## 2. Step-by-Step Procedure
1. **Semantic HTML & ARIA Audit:** Check for landmarks (`<main>`, `<nav>`, `<header>`), correct heading hierarchy (`h1` through `h6`), alt text for non-decorative images, and appropriate ARIA attributes.
2. **Keyboard Navigation & Focus Trapping:** Verify all interactive elements are reachable via keyboard (`Tab`, `Shift+Tab`, `Enter`, `Space`) with visible `:focus-visible` styling.
3. **Contrast Ratio Verification:** Measure text-to-background contrast ratios against WCAG AA standards (minimum 4.5:1 for body text, 3:1 for large text and UI components).
4. **Responsive Layout & Overflow Check:** Inspect layout behavior across breakpoints to detect horizontal scroll overflow, overlapping text, or touch targets smaller than 44x44px.
5. **Core Web Vitals Assessment:** Audit asset loading, font swap configurations, and image dimension definitions to avoid Cumulative Layout Shift (CLS) and high Largest Contentful Paint (LCP).

## 3. Expected Outputs & Artifacts
- **Accessibility & UX Audit Report:** Structured summary identifying violations, affected elements/selectors, and actionable code fixes.
- **Remediation Code Snippets:** Corrective markup or CSS snippets addressing discovered defects.

## 4. Constraints & Tool Neutrality
- **Non-Destructive Audit:** Report findings and provide recommended fixes without unilaterally modifying production markup during review.
- **Tool Neutral:** Usable alongside Chrome DevTools, axe-core, Pa11y, Lighthouse, or manual code review.
