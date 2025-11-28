## ADDED Requirements
### Requirement: Proxy Data Domain Collection
The Nuxt server SHALL expose `GET /api/datadomains` and `POST /api/datadomains` endpoints that forward requests to the platform service (`/datadomains/`), including pagination query params (`page`, `size`) and authentication context.

#### Scenario: List Data Domains
- **WHEN** a client calls `GET /api/datadomains` with optional `page` and `size`
- **THEN** the server SHALL fetch `GET {platformBaseUrl}/datadomains/?page={page}&size={size}`
- **AND** return the upstream JSON body and HTTP status unchanged.

#### Scenario: Create Data Domain
- **WHEN** a client sends a valid JSON payload to `POST /api/datadomains`
- **THEN** the server SHALL forward the body to `POST {platformBaseUrl}/datadomains/`
- **AND** respond with the upstream 201 body or validation error payload without mutation.

### Requirement: Proxy Data Domain Resource
The Nuxt server SHALL expose `GET`, `PUT`, and `DELETE` operations at `/api/datadomains/:id` that forward to the corresponding platform service resource URL and relay status codes and payloads verbatim.

#### Scenario: Retrieve Data Domain
- **WHEN** a client issues `GET /api/datadomains/{id}`
- **THEN** the server SHALL call `GET {platformBaseUrl}/datadomains/{id}`
- **AND** return the upstream JSON body or error response as-is.

#### Scenario: Update Data Domain
- **WHEN** a client sends a JSON body to `PUT /api/datadomains/{id}`
- **THEN** the server SHALL forward the body to `PUT {platformBaseUrl}/datadomains/{id}`
- **AND** mirror the upstream HTTP status and body.

#### Scenario: Delete Data Domain
- **WHEN** a client issues `DELETE /api/datadomains/{id}`
- **THEN** the server SHALL call `DELETE {platformBaseUrl}/datadomains/{id}`
- **AND** propagate the upstream 204 success or validation error without modification.
