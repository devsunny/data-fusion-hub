## ADDED Requirements
### Requirement: Proxy Authentication Endpoints
The Nuxt server SHALL expose `POST /api/users/login` and `POST /api/auth/login` endpoints that forward credential payloads to `{platformBaseUrl}/users/login` and `{platformBaseUrl}/auth/login` respectively, returning the upstream token response without mutation.

#### Scenario: Login For Access Token
- **WHEN** a client posts credentials to `/api/users/login`
- **THEN** the server SHALL forward the payload to `POST {platformBaseUrl}/users/login`
- **AND** reply with the upstream `Token` JSON or validation error.

#### Scenario: Alternate Auth Login
- **WHEN** a client posts credentials to `/api/auth/login`
- **THEN** the server SHALL call `POST {platformBaseUrl}/auth/login`
- **AND** mirror the upstream response status and body.

### Requirement: Proxy User Management
The Nuxt server SHALL expose `POST /api/users/create`, `GET /api/users`, and `GET|PUT|DELETE /api/users/:id` routes that proxy to the matching upstream user endpoints while preserving payloads and status codes.

#### Scenario: Create User
- **WHEN** a client sends user data to `POST /api/users/create`
- **THEN** the server SHALL forward to `POST {platformBaseUrl}/users/create`
- **AND** return the created user JSON or validation errors unchanged.

#### Scenario: List Users
- **WHEN** a client calls `GET /api/users`
- **THEN** the server SHALL request `GET {platformBaseUrl}/users/`
- **AND** return the upstream array payload intact.

#### Scenario: Update User
- **WHEN** a client performs `PUT /api/users/{user_id}`
- **THEN** the server SHALL forward the body to `PUT {platformBaseUrl}/users/{user_id}`
- **AND** surface the upstream success or error response without alteration.

#### Scenario: Delete User
- **WHEN** a client issues `DELETE /api/users/{user_id}`
- **THEN** the server SHALL call `DELETE {platformBaseUrl}/users/{user_id}`
- **AND** propagate the upstream 204 or error payload verbatim.

### Requirement: Proxy Roles and Approver Relationships
The Nuxt server SHALL expose role CRUD routes (`GET|POST /api/roles`, `GET|PUT|DELETE /api/roles/:roleId`) and approver relationship routes (`PUT /api/roles/:roleId/approver-roles`, `GET /api/roles/:roleId/approver-roles`, `DELETE /api/roles/:roleId/approver-roles/:approverRoleId`) that mirror the upstream API behaviors.

#### Scenario: Manage Roles
- **WHEN** a client performs CRUD operations on `/api/roles`
- **THEN** the server SHALL call the corresponding `{platformBaseUrl}/roles/` endpoints
- **AND** return upstream JSON or errors without modification.

#### Scenario: Manage Approver Roles
- **WHEN** a client assigns or removes approver roles via `/api/roles/{roleId}/approver-roles`
- **THEN** the server SHALL forward to the matching upstream endpoint
- **AND** mirror the response body and status codes.

### Requirement: Proxy User Role Requests
The Nuxt server SHALL expose `POST /api/user-role-requests`, `GET /api/user-role-requests`, `GET /api/user-role-requests/:requestId`, and approval/denial routes at `/api/user-role-requests/:requestId/(approve|deny)` that forward to the upstream service and relay responses verbatim.

#### Scenario: Submit Role Request
- **WHEN** a client posts to `/api/user-role-requests`
- **THEN** the server SHALL forward to `POST {platformBaseUrl}/user-role-requests/`
- **AND** respond with the upstream JSON payload or error.

#### Scenario: Review Role Request
- **WHEN** a client invokes approval or denial routes on `/api/user-role-requests/{requestId}`
- **THEN** the server SHALL forward to the corresponding `{platformBaseUrl}/user-role-requests/{requestId}/{action}` endpoint
- **AND** return the upstream success or error response unchanged.
