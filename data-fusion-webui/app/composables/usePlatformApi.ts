import type {
    DataDomain,
    DataDomainCreate,
    DataDomainUpdate,
    DataConnector,
    DataConnectorCreate,
    DataConnectorUpdate,
    DataObject,
    DataObjectCreate,
    DataObjectUpdate,
    DataObjectBulkCreate,
    DataObjectBulkResponse,
    PaginatedResponse,
    PlatformUser,
    PlatformUserCreate,
    PlatformUserUpdate,
    Role,
    RoleCreate,
    RoleUpdate,
    RoleApproverRelationship,
    TokenResponse,
    UserRoleRequest,
    UserRoleRequestCreate,
    UserRoleRequestUpdate
} from '~/types/platform'

interface PaginationQuery {
    page?: number
    size?: number
}

interface RolePaginationQuery {
    skip?: number
    limit?: number
}

export function usePlatformApi() {
    const request = useRequestFetch()

    return {
        // Data Domains
        listDataDomains: (query?: PaginationQuery) =>
            request<PaginatedResponse<DataDomain>>('/api/datadomains', { query }),
        createDataDomain: (payload: DataDomainCreate) =>
            request<DataDomain>('/api/datadomains', { method: 'POST', body: payload }),
        getDataDomain: (id: string) => request<DataDomain>(`/api/datadomains/${id}`),
        updateDataDomain: (id: string, payload: DataDomainUpdate) =>
            request<DataDomain>(`/api/datadomains/${id}`, { method: 'PUT', body: payload }),
        deleteDataDomain: (id: string) => request<undefined>(`/api/datadomains/${id}`, { method: 'DELETE' }),

        // Data Connectors
        listDataConnectors: (query?: PaginationQuery) =>
            request<PaginatedResponse<DataConnector>>('/api/dataconnectors', { query }),
        createDataConnector: (payload: DataConnectorCreate) =>
            request<DataConnector>('/api/dataconnectors', { method: 'POST', body: payload }),
        getDataConnector: (id: string) => request<DataConnector>(`/api/dataconnectors/${id}`),
        updateDataConnector: (id: string, payload: DataConnectorUpdate) =>
            request<DataConnector>(`/api/dataconnectors/${id}`, { method: 'PUT', body: payload }),
        deleteDataConnector: (id: string) =>
            request<undefined>(`/api/dataconnectors/${id}`, { method: 'DELETE' }),

        // Data Objects
        listDataObjects: () => request<DataObject[]>('/api/data-objects'),
        createDataObject: (payload: DataObjectCreate) =>
            request<DataObject>('/api/data-objects', { method: 'POST', body: payload }),
        getDataObject: (id: string) => request<DataObject>(`/api/data-objects/${id}`),
        updateDataObject: (id: string, payload: DataObjectUpdate) =>
            request<DataObject>(`/api/data-objects/${id}`, { method: 'PUT', body: payload }),
        deleteDataObject: (id: string) =>
            request<undefined>(`/api/data-objects/${id}`, { method: 'DELETE' }),
        bulkCreateDataObjects: (payload: DataObjectBulkCreate) =>
            request<DataObjectBulkResponse[]>('/api/data-objects/bulk', { method: 'POST', body: payload }),

        // Authentication & Users
        loginUser: (payload: { email: string; password: string }) =>
            request<TokenResponse>('/api/users/login', { method: 'POST', body: payload }),
        loginViaAuth: (payload: { email: string; password: string }) =>
            request<TokenResponse>('/api/auth/login', { method: 'POST', body: payload }),
        createUser: (payload: PlatformUserCreate) =>
            request<PlatformUser>('/api/users/create', { method: 'POST', body: payload }),
        listUsers: () => request<PlatformUser[]>('/api/users'),
        getUser: (id: string) => request<PlatformUser>(`/api/users/${id}`),
        updateUser: (id: string, payload: PlatformUserUpdate) =>
            request<PlatformUser>(`/api/users/${id}`, { method: 'PUT', body: payload }),
        deleteUser: (id: string) => request<undefined>(`/api/users/${id}`, { method: 'DELETE' }),

        // Roles
        listRoles: (query?: RolePaginationQuery) => request<Role[]>('/api/roles', { query }),
        createRole: (payload: RoleCreate) =>
            request<Role>('/api/roles', { method: 'POST', body: payload }),
        getRole: (id: string) => request<Role>(`/api/roles/${id}`),
        updateRole: (id: string, payload: RoleUpdate) =>
            request<Role>(`/api/roles/${id}`, { method: 'PUT', body: payload }),
        deleteRole: (id: string) => request<undefined>(`/api/roles/${id}`, { method: 'DELETE' }),

        // Role approver relationships
        assignApproverRoles: (roleId: string, approverRoleIds: string[]) =>
            request<RoleApproverRelationship[]>(`/api/roles/${roleId}/approver-roles`, {
                method: 'PUT',
                body: approverRoleIds
            }),
        listApproverRoles: (roleId: string) =>
            request<RoleApproverRelationship[]>(`/api/roles/${roleId}/approver-roles`),
        removeApproverRole: (roleId: string, approverRoleId: string) =>
            request<undefined>(`/api/roles/${roleId}/approver-roles/${approverRoleId}`, { method: 'DELETE' }),

        // User role requests
        createUserRoleRequest: (payload: UserRoleRequestCreate) =>
            request<UserRoleRequest>('/api/user-role-requests', { method: 'POST', body: payload }),
        listUserRoleRequests: (userId: string) =>
            request<UserRoleRequest[]>(`/api/user-role-requests`, { query: { user_id: userId } }),
        getUserRoleRequest: (requestId: string) =>
            request<UserRoleRequest>(`/api/user-role-requests/${requestId}`),
        updateUserRoleRequest: (requestId: string, payload: UserRoleRequestUpdate, action: 'approve' | 'deny') =>
            request(`/api/user-role-requests/${requestId}/${action}`, { method: 'PUT', body: payload })
    }
}
