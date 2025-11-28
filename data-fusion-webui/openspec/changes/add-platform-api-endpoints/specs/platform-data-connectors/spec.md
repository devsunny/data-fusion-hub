## ADDED Requirements
### Requirement: Proxy Data Connector Collection
The Nuxt server SHALL expose `GET /api/dataconnectors` and `POST /api/dataconnectors` endpoints that forward requests to `{platformBaseUrl}/dataconnectors/`, preserving pagination query parameters and returning upstream responses verbatim.

#### Scenario: List Data Connectors
- **WHEN** a client calls `GET /api/dataconnectors`
- **THEN** the server SHALL issue `GET {platformBaseUrl}/dataconnectors/`
- **AND** reply with the same HTTP status code and JSON payload as the upstream service.

#### Scenario: Create Data Connector
- **WHEN** a client sends a valid JSON payload to `POST /api/dataconnectors`
- **THEN** the server SHALL forward the payload to `POST {platformBaseUrl}/dataconnectors/`
- **AND** surface the upstream 201 response or validation error as-is.

### Requirement: Proxy Data Connector Resource
The Nuxt server SHALL expose `GET`, `PUT`, and `DELETE` routes at `/api/dataconnectors/:id` that proxy to `{platformBaseUrl}/dataconnectors/{id}` and do not mutate response bodies or status codes.

#### Scenario: Retrieve Data Connector
- **WHEN** a client requests `GET /api/dataconnectors/{id}`
- **THEN** the server SHALL request `GET {platformBaseUrl}/dataconnectors/{id}`
- **AND** return the upstream payload or error without alteration.

#### Scenario: Update Data Connector
- **WHEN** a client submits `PUT /api/dataconnectors/{id}` with JSON content
- **THEN** the server SHALL forward the body to `PUT {platformBaseUrl}/dataconnectors/{id}`
- **AND** mirror the upstream HTTP status and JSON response.

#### Scenario: Delete Data Connector
- **WHEN** a client calls `DELETE /api/dataconnectors/{id}`
- **THEN** the server SHALL call `DELETE {platformBaseUrl}/dataconnectors/{id}`
- **AND** propagate the upstream 204 success or error payload unmodified.
