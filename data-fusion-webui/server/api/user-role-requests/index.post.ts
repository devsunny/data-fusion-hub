import type { H3Event } from 'h3'
import { createError, readBody } from 'h3'

type UserRoleRequestCreatePayload = {
    user_id?: string
    role_id?: string
    justification?: string
    reason?: string | null
}

export default defineEventHandler(async (event: H3Event) => {
    const body = await readBody<UserRoleRequestCreatePayload | null>(event)

    if (!body || typeof body !== 'object' || typeof body.user_id !== 'string' || !body.user_id.trim() || typeof body.role_id !== 'string' || !body.role_id.trim() || typeof body.justification !== 'string' || !body.justification.trim()) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'user_id, role_id, and justification are required' }
        })
    }

    return await callPlatformApi(event, '/user-role-requests/', {
        method: 'POST',
        body
    })
})
