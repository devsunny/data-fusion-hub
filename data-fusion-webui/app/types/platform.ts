export interface PaginationMetadata {
    page: number
    size: number
    total: number
    pages: number
}

export interface PaginatedResponse<T> {
    data: T[]
    pagination: PaginationMetadata
}

export interface DataDomain {
    id: string
    name: string
    description?: string | null
    created_at: string
    updated_at: string
}

export interface DataDomainCreate {
    name: string
    description?: string | null
}

export interface DataDomainUpdate {
    name?: string | null
    description?: string | null
}

export interface DataConnector {
    id: string
    name: string
    description?: string | null
    type: string
    configuration: Record<string, unknown>
    authentication?: Record<string, unknown> | null
    created_at: string
    updated_at: string
}

export interface DataConnectorCreate {
    name: string
    description?: string | null
    type: string
    configuration: Record<string, unknown>
    authentication?: Record<string, unknown> | null
}

export interface DataConnectorUpdate {
    name?: string | null
    description?: string | null
    type?: string | null
    configuration?: Record<string, unknown> | null
    authentication?: Record<string, unknown> | null
}

export interface DataObject {
    id: string
    name: string
    description?: string | null
    type: string
    data_domain_id: string
    created_at: string
    updated_at: string
}

export interface DataObjectCreate {
    name: string
    description?: string | null
    type: string
    data_domain_id: string
}

export interface DataObjectUpdate {
    name?: string | null
    description?: string | null
    type?: string | null
    data_domain_id?: string | null
}

export interface DataFieldCreate {
    name: string
    description?: string | null
    type: string
    is_required?: boolean
    ansi_data_type?: string | null
    display_name?: string | null
    max_char_length?: number | null
    min_char_length?: number | null
    numerical_precision?: number | null
    numerical_scale?: number | null
}

export interface DataObjectBulkCreateItem extends DataObjectCreate {
    data_fields: DataFieldCreate[]
}

export interface DataObjectBulkCreate {
    data_domain_id: string
    data_objects: DataObjectBulkCreateItem[]
}

export interface DataObjectBulkResponse extends DataObject {
    data_fields: DataFieldCreate[]
}

export interface TokenResponse {
    access_token: string
    token_type?: string
}

export interface PlatformUser {
    id: string
    email: string
    first_name: string
    middle_name?: string | null
    last_name: string
    created_at: string
    updated_at: string
    created_by?: string | null
    updated_by?: string | null
}

export interface PlatformUserCreate {
    email: string
    first_name: string
    last_name: string
    password?: string | null
    middle_name?: string | null
}

export type PlatformUserUpdate = PlatformUserCreate

export interface Role {
    id: string
    name: string
    description?: string | null
    created_by: string
    updated_by: string
    created_at: string
    updated_at: string
}

export interface RoleCreate {
    name: string
    description?: string | null
}

export interface RoleUpdate {
    name?: string | null
    description?: string | null
}

export interface RoleApproverRelationship {
    id: string
    role_id: string
    approver_role_id: string
    created_at: string
    updated_at: string
}

export interface UserRoleRequest {
    id: string
    user_id: string
    role_id: string
    justification: string
    reason?: string | null
    status: string
    created_at: string
    updated_at: string
}

export interface UserRoleRequestCreate {
    user_id: string
    role_id: string
    justification: string
    reason?: string | null
}

export interface UserRoleRequestUpdate {
    status: string
    reason?: string | null
}
