import type { H3Event } from 'h3'
import { createError, getRouterParam, readBody } from 'h3'

type RoleUpdatePayload = {
    name?: string | null
    description?: string | null
}

export default defineEventHandler(async (event: H3Event) => {
    const roleId = getRouterParam(event, 'role_id')

    if (!roleId) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'role_id is required' }
        })
    }

    const body = await readBody<RoleUpdatePayload | null>(event)

    if (!body || typeof body !== 'object') {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'payload is required' }
        })
    }

    return await callPlatformApi(event, `/roles/${roleId}`, {
        method: 'PUT',
        body
    })
})
