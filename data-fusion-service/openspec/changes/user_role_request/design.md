# User Role Request - Design Document

## Overview

This document outlines the design for implementing a user role request system that allows users to request membership in additional roles beyond their default "public" role. The system implements an approval workflow where requests must be approved by designated approver roles before being granted, and includes administrative functionality to assign approver roles.

## Architecture Approach

### Data Models
1. **UserRoleRequest**: Tracks individual role requests with status and metadata
2. **UserRoleRequestStatus**: Enum for request states (pending, approved, denied)  
3. **RoleApproverRelationship**: Defines which roles can approve requests for other roles
4. **UserRoles**: Relationship table to track user-role assignments

### Workflow Logic
1. Users submit role requests through the API with justification
2. System validates that:
   - Requested role is not "public" (default role)
   - User doesn't already have the requested role  
   - Justification is provided for the request
3. For each approver role associated with the target role:
   - Check if at least one member of that approver role exists in the system  
4. If all required approver roles approve, assign the role to the user
5. If any approver role denies, reject the request
6. After successful persistence, send notification to ActiveMQ topic

### Database Schema Changes
- `user_role_requests` table for tracking requests with justification field
- `role_approver_relationships` table for defining approval hierarchies
- Updated database initialization to include new table models

## Key Design Decisions

1. **Default Role**: All users automatically belong to "public" role without requiring approval
2. **Approval Hierarchy**: Each role can have zero or more approver roles that must approve requests  
3. **Owner Role as Approver**: If no specific approver roles are defined, the owner role becomes the approver
4. **Atomic Operations**: Approval process is atomic - either all approvals succeed or request fails completely
5. **Role-based Approvers**: Approvers are roles (not individual users), with at least one member of each approver role needed for approval
6. **Justification Required**: All requests must include a justification explaining the need for the role
7. **Optional Reasons**: Approvals and denials can optionally include reasons for audit purposes

## Integration Design

### ActiveMQ Notification System
- After successful database persistence of user role request, system shall publish JSON event to ActiveMQ topic
- Topic name: "system integration topic" 
- Event type: "user_role_request"
- Payload includes: request ID (UUID) and all user request details

## Administrative Functionality

### Role Approver Assignment
The system SHALL provide administrative capabilities to assign approver roles to existing roles.

#### Endpoint:
`PUT /roles/{role_id}/approver-roles`

#### Description:
This endpoint allows administrators to specify which roles can approve requests for a given role. The request body should contain an array of approver role IDs.

### Database Relationships
- `role_approver_relationships` table connects roles to their approver roles
- Each row represents a relationship between a target role and its approver roles

## Approval Reason Handling

The system SHALL support optional reason fields for approval and denial actions:

1. **Approval Reasons**: When approving a request, approvers may optionally provide a reason
2. **Denial Reasons**: When denying a request, approvers may optionally provide a reason  
3. **Storage**: Reasons are stored with the request and made available in request details
4. **Audit Trail**: Reasons contribute to audit trail for compliance purposes

## Security Considerations

1. Only authenticated users can submit requests
2. Only designated approver roles can approve/deny requests  
3. Request status changes require proper authorization checks
4. Role assignments are logged for audit purposes
5. Approver role assignment requires administrative privileges

## API Design Principles

1. Clear separation between request submission and approval operations
2. Comprehensive error handling with descriptive messages
3. Consistent response formats across all endpoints
4. Proper HTTP status codes for different scenarios

## Usage Examples

### Creating a Role Request
```bash
curl -X POST "http://localhost:8000/user-role-requests" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-123",
    "role_id": "role-456", 
    "justification": "Need admin access for project management"
  }'
```

### Approving a Role Request
```bash
curl -X PUT "http://localhost:8000/user-role-requests/req-789/approve" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "approved",
    "reason": "Manager approved access request"
  }'
```

### Assigning Approver Roles
```bash
curl -X PUT "http://localhost:8000/roles/role-456/approver-roles" \
  -H "Content-Type: application/json" \
  -d '["role-111", "role-222"]'
```

## Approval Workflow Process

1. **Request Submission**: User submits role request with justification
2. **Validation**: System validates that:
   - Role is not "public"
   - User and target role exist  
   - Justification is provided
3. **Approval Processing**: 
   - Request waits for approver roles to review
   - Approvers can optionally provide reasons
4. **Outcome**:
   - Approved: Request status changes to "approved" 
   - Denied: Request status changes to "denied"
5. **Role Assignment**: Upon approval, user is assigned the requested role (implementation detail)

## Future Enhancements

- Integration with ActiveMQ for system notifications  
- Enhanced approval workflow with multi-step processes
- Email notifications for request status changes
- Role hierarchy inheritance capabilities