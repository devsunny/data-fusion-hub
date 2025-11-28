# Change: Implement Data Fusion Hub REST API surface in Nuxt server

## Why
The dashboard currently serves mocked data from static handlers under `server/api`. To connect the UI to live platform services and enable CRUD operations, the Nuxt application needs REST endpoints that mirror the official Data Fusion Hub API contract published at `http://localhost:8000/openapi.json`.

## What Changes
- Add Nuxt server routes that proxy every documented resource in the OpenAPI schema (data domains, data connectors, data objects, user management, authentication, and role approvals).
- Apply consistent pagination, validation, and error handling aligned with the upstream FastAPI service (HTTP 4xx/5xx pass-through, typed responses).
- Centralize configuration for the base service URL and authentication so frontend and server code share the same integration settings.
- Update OpenSpec capabilities to define the required request/response flows, authorization expectations, and bulk operation semantics for the dashboard backend.

## Impact
- Affected specs: `platform-data-domains`, `platform-data-connectors`, `platform-data-objects`, `platform-user-management` (new capabilities).
- Affected code: `server/api/**` (replacement of mock handlers), potential new composables for API client configuration, runtime config (`nuxt.config.ts`, `.env` usage).
