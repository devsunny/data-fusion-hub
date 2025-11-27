# Project Context

## Purpose
Data Fusion Hub Web UI delivers the operational dashboard for the Data Fusion platform. It provides a Nuxt-powered admin experience for monitoring high-level KPIs, browsing recent activity, and managing core entities such as customers, inbox conversations, notifications, and team members. The near-term goal is to keep the template production-ready while we progressively replace mocked data with live backend integrations.

## Tech Stack
- Nuxt 4 (Vue 3 + Vite bundler, SSR/ISR capable)
- TypeScript-first single file components using `<script setup>`
- `@nuxt/ui` design system with Tailwind CSS theme tokens defined in `app/assets/css/main.css`
- `@vueuse/nuxt` for composables, shortcuts, and shared state
- `@unovis/vue` + `@unovis/ts` for charting and data visualizations
- `date-fns` and `zod` for date utilities and runtime validation when needed
- PNPM 10 as the package manager; Nuxt requires Node.js 18 or newer for local dev and deployments

## Project Conventions

### Code Style
- Compose views with `<script setup lang="ts">` and the Vue Composition API; keep props and emits typed via `~/types` definitions.
- Follow the Nuxt ESLint preset (`@nuxt/eslint`) with project overrides: allow multiple root nodes, limit Vue attributes to three per line, enforce 1TBS brace style, and disallow dangling commas.
- Group feature-specific components under `app/components/<feature>` and colocate domain-specific dialogs or modals with their feature.
- Prefer composables (`app/composables/`) for cross-page state (for example `useDashboard` handles keyboard shortcuts and shared UI flags).
- Keep styling declarative through `@nuxt/ui` utility classes and the centralized theme tokens in `app/assets/css/main.css` rather than ad-hoc CSS.

### Architecture Patterns
- Adopt the Nuxt `app/` directory structure: file-based routing in `app/pages`, global layout scaffolding in `app/layouts`, and configuration via `app/app.config.ts`.
- Expose lightweight server endpoints under `server/api` that currently return in-memory fixtures; UI code accesses them through `useAsyncData` to smooth the eventual transition to real services.
- Split components that depend on browser-only APIs into `.client.vue` counterparts (for example `HomeChart.client.vue`) so that SSR can fall back to skeleton placeholders defined in matching `.server.vue` files.
- Encapsulate shared UI state and macro-interactions (like the notifications slide-over) inside composables built with `createSharedComposable` to keep pages declarative.
- Keep utility logic centralized in `app/utils` and strongly type data contracts inside `app/types` to minimize duplication.

### Testing Strategy
- Required local quality gates: `pnpm lint` (ESLint) and `pnpm typecheck` (Vue TSC) must pass before opening or merging pull requests.
- No automated unit or end-to-end suites are wired up yet; perform manual smoke testing across the Home, Customers, Inbox, and Settings views before shipping.
- Document reproduction steps for bugs and backfill automated coverage (likely with Vitest + Playwright) as we integrate real APIs.

### Git Workflow
- Work on short-lived feature branches named with a verb-led prefix (for example `feat/sbadmin_layout`) branched from the default trunk (`main`).
- Open pull requests for review rather than pushing directly to `main`; include links to relevant OpenSpec changes when applicable.
- Keep commits focused and descriptive; Conventional Commit prefixes (`feat:`, `fix:`, etc.) are encouraged but not enforced.
- Before pushing, run `pnpm lint` and `pnpm typecheck` to catch regressions early and avoid breaking the shared branch.

## Domain Context
- The dashboard surfaces operational insights for Data Fusion Hub: revenue snapshots, inbox triage, customer subscription health, and team administration workflows.
- Current data is mocked within the repo (`server/api/*.ts`) to enable rapid UI iteration; downstream work will swap these handlers for real service integrations while preserving the same shape.
- Navigation shortcuts (for example `g-h`, `g-i`, `g-c`, `g-s`) are part of the UX contract and should continue to work as routes evolve.

## Important Constraints
- Maintain compatibility with Nuxt 4’s expectations (Node 18+, ESM modules, Nitro serverless targets) when introducing dependencies or build tooling.
- Keep the design aligned with the Nuxt UI theme palette (green primary, zinc neutrals) configured in `app/app.config.ts` and `app/assets/css/main.css` to protect brand consistency.
- API routes under `/api/**` currently enable CORS; future backend integrations must respect cross-origin access for external tooling and should remain stateless to stay deployable on edge runtimes.
- Prefer lightweight front-end only solutions unless the change explicitly requires backend logic—backend services are owned by a separate repository.

## External Dependencies
- `@nuxt/ui` component library (and its Tailwind theme) provides the design system primitives; breaking changes there require coordinated updates.
- `@vueuse/nuxt` supplies composables relied upon for shortcuts, shared state, and reactivity utilities.
- `@unovis/vue` + `@unovis/ts` render the dashboard charts; upgrades may require adjusting chart configuration objects.
- Static imagery uses `https://i.pravatar.cc` for avatar placeholders—replace with internal media service before production roll-out.
- No production backend is wired in yet; planned integrations will consume Data Fusion Hub APIs exposed by the core platform services.
