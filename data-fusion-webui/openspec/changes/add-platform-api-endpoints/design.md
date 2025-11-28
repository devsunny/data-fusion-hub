## Context
The Nuxt dashboard currently reads from mock Nitro endpoints. The Data Fusion Hub platform exposes a FastAPI service (documented at `http://localhost:8000/openapi.json`) that delivers the authoritative CRUD surface. We need to proxy that service through the Nuxt server layer so the SPA interacts with a single origin and we can later enforce UI-specific policies (auth cookies, rate limiting, telemetry).

## Goals / Non-Goals
- Goals:
  - Provide 1:1 proxy coverage for every REST operation listed in the provided OpenAPI document.
  - Support pagination, bulk creation, and role approval workflows with minimal transformation of payloads.
  - Keep proxy behavior declarative and testable, isolating base URL and auth configuration.
- Non-Goals:
  - Implement the upstream FastAPI service itself.
  - Add advanced caching or retry/backoff beyond simple pass-through.
  - Introduce UI rewrites; frontend consumption updates stay minimal.

## Decisions
- Decision: Use a shared `callPlatformApi` helper wrapping `ofetch` so all routes inherit auth headers, timeout, and error handling. This keeps route handlers small and makes logging consistent.
- Decision: Store the platform base URL and optional API key in `runtimeConfig` (`public.platformApiBaseUrl`, `platformApiKey`). When absent, default to `http://localhost:8000` for local dev.
- Decision: Let upstream HTTP status codes pass through, only transforming 5xx into JSON bodies if the platform returns empty responses.
- Decision: Validate required params at the edge using Zod schemas derived from the OpenAPI contract to catch developer errors earlier than the upstream service.

## Risks / Trade-offs
- Upstream downtime will now break dashboard functionality; mitigate with clear error messaging and logging.
- Maintaining parity with the OpenAPI spec requires diligence; future spec changes need corresponding OpenSpec updates and regression tests.
- Without caching, high-volume list requests hit the upstream service directly; acceptable for now given modest load expectations.

## Migration Plan
1. Land proxy helpers and runtime config.
2. Replace each mock route with a proxy implementation, keeping route paths stable for the UI.
3. Update composables/pages to consume new data shapes (identical to spec) and test flows locally.
4. Coordinate deployment so environment variables (`PLATFORM_API_BASE_URL`, `PLATFORM_API_KEY`) are set in each environment.

## Open Questions
- Do we need to handle JWT storage/refresh on behalf of the frontend, or will the UI store access tokens directly?
- Should we add request/response schema validation against the OpenAPI document (e.g., using `zod-openapi`) to detect regressions automatically?
