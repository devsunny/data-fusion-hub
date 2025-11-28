## ADDED Requirements
### Requirement: Proxy Data Object Collection
The Nuxt server SHALL expose `GET /api/data-objects` and `POST /api/data-objects` routes that forward payloads to `{platformBaseUrl}/data-objects/`, ensuring the response body and status codes match the upstream service exactly.

#### Scenario: List Data Objects
- **WHEN** a client calls `GET /api/data-objects`
- **THEN** the server SHALL call `GET {platformBaseUrl}/data-objects/`
- **AND** return the array response or error from the upstream API without modification.

#### Scenario: Create Data Object
- **WHEN** a client sends a valid JSON payload to `POST /api/data-objects`
- **THEN** the server SHALL forward the payload to `POST {platformBaseUrl}/data-objects/`
- **AND** propagate the upstream success or validation failure intact.

### Requirement: Proxy Data Object Resource
The Nuxt server SHALL expose `GET`, `PUT`, and `DELETE` operations at `/api/data-objects/:id` that proxy to `{platformBaseUrl}/data-objects/{id}` while mirroring upstream status codes, headers, and bodies.

#### Scenario: Retrieve Data Object
- **WHEN** a client issues `GET /api/data-objects/{id}`
- **THEN** the server SHALL request `GET {platformBaseUrl}/data-objects/{id}`
- **AND** respond with the same JSON payload or error status.

#### Scenario: Update Data Object
- **WHEN** a client submits `PUT /api/data-objects/{id}` with JSON content
- **THEN** the server SHALL forward to `PUT {platformBaseUrl}/data-objects/{id}`
- **AND** mirror the upstream success or validation error response.

#### Scenario: Delete Data Object
- **WHEN** a client calls `DELETE /api/data-objects/{id}`
- **THEN** the server SHALL call `DELETE {platformBaseUrl}/data-objects/{id}`
- **AND** surface the upstream HTTP status and JSON body (if any) unchanged.

### Requirement: Proxy Data Object Bulk Create
The Nuxt server SHALL expose `POST /api/data-objects/bulk` that forwards bulk payloads to `{platformBaseUrl}/data-objects/bulk` and relays the upstream array response or validation errors verbatim.

#### Scenario: Bulk Create Data Objects
- **WHEN** a client posts a bulk payload to `/api/data-objects/bulk`
- **THEN** the server SHALL request `POST {platformBaseUrl}/data-objects/bulk`
- **AND** respond with the upstream array of created objects or validation errors without alteration.
