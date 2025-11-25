# User Role Request Service

## Overview

This change introduces a comprehensive user role request service that allows users to request membership in additional roles beyond their default "public" role. The system implements an approval workflow where requests must be approved by designated approver roles before being granted, and includes administrative functionality to assign approver roles to existing roles.

## Change ID
`user_role_request`

## Summary
Users can submit requests for additional roles with justification, which require approval from designated approver roles before being granted. All users automatically belong to the "public" default role without requiring approval. Each role has associated approver roles that must approve requests for that role. After successful persistence, system sends notifications to ActiveMQ. Administrators can assign one or more roles as approvers to any existing role.

## Key Features
1. Users can request membership in non-public roles with justification
2. Requests require approval by one member of each required approver role  
3. Default "public" role is automatically assigned to all users
4. Role hierarchy with owner/approver relationships
5. Approval workflow with status tracking
6. ActiveMQ notification system for integration events
7. Administrative endpoint to assign approver roles to existing roles
8. Optional reason fields for approval and denial actions

## API Endpoints

### User Role Request Operations
- **POST** `/user-role-requests` - Submit new role requests with justification
- **GET** `/user-role-requests` - List user's own requests  
- **GET** `/user-role-requests/{id}` - Get specific request details
- **PUT** `/user-role-requests/{id}/approve` - Approve a request (with optional reason)
- **PUT** `/user-role-requests/{id}/deny` - Deny a request (with optional reason)

### Role Approver Management  
- **PUT** `/roles/{role_id}/approver-roles` - Assign approver roles to existing role
- **GET** `/roles/{role_id}/approver-roles` - Get approver roles for a specific role

## Data Models

### UserRoleRequestDB
Tracks individual role requests with status and metadata including:
- User ID (UUID of requesting user)
- Role ID (UUID of requested role)  
- Justification (reason for request)
- Reason (optional reason for approval/denial)
- Status (pending, approved, denied)

### RoleApproverRelationshipDB
Defines which roles can approve requests for other roles including:
- Role ID (target role to be approved)
- Approver Role ID (role that can approve requests for target role)

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
5. **Role Assignment**: Upon approval, user is assigned the requested role

## Security Considerations
- All endpoints require proper authentication
- Only designated approver roles can approve/deny requests  
- Audit trail maintained through created_at/updated_at timestamps
- Reason fields contribute to compliance audit requirements

## Integration Features
- ActiveMQ notifications for system integration (ready upon database persistence)
- JSON payload with request ID and details
- Event type: "user_role_request"

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

## Dependencies
- Existing user and role models
- Authentication system (not specified in this change)
- ActiveMQ integration capability

## Future Enhancements
- Integration with ActiveMQ for system notifications  
- Enhanced approval workflow with multi-step processes
- Email notifications for request status changes
- Role hierarchy inheritance capabilities