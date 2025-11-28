## 1. Discovery & Setup
- [x] 1.1 Introduce runtime config for the Data Fusion Hub API base URL and auth secret (default to `http://localhost:8000`).
- [x] 1.2 Create a shared Nitro fetch helper that forwards headers, handles pagination params, and normalizes API errors.

## 2. Data Domains Endpoints
- [x] 2.1 Implement `GET /api/datadomains` to paginate results via the upstream `/datadomains/` route.
- [x] 2.2 Implement `POST /api/datadomains` forwarder with request validation and 201 propagation.
- [x] 2.3 Implement `GET|PUT|DELETE /api/datadomains/:id` proxying the single-resource actions.

## 3. Data Connectors Endpoints
- [x] 3.1 Implement `GET /api/dataconnectors` pagination proxy.
- [x] 3.2 Implement `POST /api/dataconnectors` create proxy.
- [x] 3.3 Implement `GET|PUT|DELETE /api/dataconnectors/:id` handlers.

## 4. Data Objects Endpoints
- [x] 4.1 Implement `GET /api/data-objects` collection proxy.
- [x] 4.2 Implement `POST /api/data-objects` create proxy.
- [x] 4.3 Implement `GET|PUT|DELETE /api/data-objects/:id` handlers.
- [x] 4.4 Implement `POST /api/data-objects/bulk` bulk create handler, including validation on array payload shape.

## 5. User & Role Management
- [x] 5.1 Implement `POST /api/users/login` and `POST /api/auth/login` proxies that return upstream token payloads verbatim.
- [x] 5.2 Implement `POST /api/users/create`, `GET /api/users`, and `GET|PUT|DELETE /api/users/:id` routes.
- [x] 5.3 Implement `GET|POST /api/roles` and `GET|PUT|DELETE /api/roles/:id` proxies.
- [x] 5.4 Implement `PUT /api/roles/:roleId/approver-roles`, `GET /api/roles/:roleId/approver-roles`, and `DELETE /api/roles/:roleId/approver-roles/:approverRoleId` routes.
- [x] 5.5 Implement `POST|GET /api/user-role-requests`, `GET /api/user-role-requests/:requestId`, and approval/deny `PUT` routes.

## 6. Validation & Observability
- [x] 6.1 Mirror upstream HTTP status codes and parse FastAPI validation errors into JSON responses.
- [x] 6.2 Add server-side logging for non-2xx responses to aid troubleshooting.

## 7. Quality Gates
- [x] 7.1 Update or add API client composables to consume the new routes where mock data was previously used.
- [x] 7.2 Run `pnpm lint` and `pnpm typecheck`.
- [ ] 7.3 Produce manual test notes covering happy/validation/error paths for each resource.
