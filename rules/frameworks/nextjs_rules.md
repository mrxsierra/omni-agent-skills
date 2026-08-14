---
trigger: model_decision
description: Next.js, React, TypeScript, and Web Development Coding Standards & Rules.
---

# ⚛️ Next.js, React & Web Development Standards

These rules apply when writing, editing, or auditing Next.js applications, React components, and TypeScript frontend code.

## 1. Next.js App Router & Architecture
- **Server Components by Default:** Keep components as React Server Components (`RSC`) by default. Use `'use client'` only when state, event handlers, or browser APIs are required.
- **Dynamic Imports:** Use dynamic imports (`next/dynamic`) or `React.lazy()` for heavy client side components to maintain optimal LCP and INP Core Web Vitals.
- **Metadata & SEO:** Include descriptive page title tags, meta descriptions, and OpenGraph headers for every page.

## 2. Design System & CSS (Vanilla CSS / HSL Tokens)
- **Fluid Layouts:** Components and containers must be fluidly responsive across all breakpoints (mobile, tablet, desktop).
- **Design Tokens:** Use curated HSL color palettes and CSS variables for background, text, and accent colors.
