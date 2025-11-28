import type { H3Event } from 'h3'
import { createError, getRouterParam, setResponseStatus } from 'h3'

export default defineEventHandler(async (event: H3Event) => {
    const roleId = getRouterParam(event, 'role_id')
    const approverRoleId = getRouterParam(event, 'approver_role_id')

    if (!roleId || !approverRoleId) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'role_id and approver_role_id are required' }
        })
    }

    await callPlatformApi(event, `/roles/${roleId}/approver-roles/${approverRoleId}`, {
        method: 'DELETE',
        responseType: 'text'
    })

    setResponseStatus(event, 204)
    return null
})
