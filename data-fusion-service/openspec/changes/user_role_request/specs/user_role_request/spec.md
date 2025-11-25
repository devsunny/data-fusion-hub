# User Role Request Service

## ADDED Requirements

### Requirement: UserRoleRequest Model
The system SHALL provide a data model for tracking user requests for additional roles, including status and metadata about the request.

#### Scenario:
When a user wants to join a specific role and submits a request through the API, a `UserRoleRequest` object shall be created with status "pending".

#### Scenario:
When a user submits a role request for the "public" role, the system shall reject the request with error code 400.

### Requirement: Approval Workflow  
The system SHALL implement an approval workflow where requests require approval from designated approver roles before being granted.

#### Scenario:
When a role has defined approver roles and a user requests membership in that role, the system shall check if at least one member of each approver role approves the request.

#### Scenario:
When a role has no defined approver roles and a user requests membership in that role, the system shall use the owner role of the target role as the approver role.

### Requirement: Request Status Management
The system SHALL manage the lifecycle of role requests through different status states.

#### Scenario:
When an authorized approver from a required approver role approves a valid role request, the system shall update the request status to "approved" and assign the role.

#### Scenario:
When an authorized approver from a required approver role denies a valid role request, the system shall update the request status to "denied".

### Requirement: User Role Assignment
The system SHALL automatically assign roles to users upon successful approval of their requests.

#### Scenario:
When a request is approved by all required approver roles and the approval process completes, the system shall grant membership in the requested role to the user.

### Requirement: System Notification Integration
The system SHALL send a notification to a "system integration topic" in ActiveMQ when a user role request is persisted to the database.

#### Scenario:
When a user submits a role request that is successfully persisted to the database, the system shall publish a JSON payload event with type "user_role_request" to an ActiveMQ system integration topic.

#### Scenario:
The published JSON payload shall include the request ID (UUID) and all user request details.

### Requirement: Justification for Requests
The system SHALL require users to provide justification when submitting role requests.

#### Scenario:
When a user submits a role request through the API, they must provide a justification field explaining why they need the requested role.

#### Scenario:
If a user does not provide justification when submitting a request, the system shall reject the request with error code 400.

### Requirement: Approver Reason Field
The system SHALL allow approvers to optionally provide a reason when approving or denying role requests.

#### Scenario:
When an approver approves a role request through the API, they may optionally include a reason field in their request body.

#### Scenario:
When an approver denies a role request through the API, they may optionally include a reason field in their request body.

#### Scenario:
If a reason is provided during approval or denial, it shall be stored with the request and made available in request details.

## MODIFIED Requirements

### Requirement: Existing Role Model Enhancement  
The system SHALL extend existing role models to include information about which roles can approve requests for this role.

#### Scenario:
When extending existing role models with approval relationships, each role shall be able to specify zero or more other roles that can approve requests for it.

### Requirement: User Model Extension 
The system SHALL provide enhanced user information that includes all current roles the user belongs to.

#### Scenario:
When retrieving user information, the system shall return all roles the user belongs to including "public".

## REMOVED Requirements

None