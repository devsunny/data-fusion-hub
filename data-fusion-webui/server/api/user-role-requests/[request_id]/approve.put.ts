import type { H3Event } from 'h3'
import { createError, getRouterParam, readBody } from 'h3'

type RequestUpdatePayload = {
    status?: string
    reason?: string | null
}

export default defineEventHandler(async (event: H3Event) => {
    const requestId = getRouterParam(event, 'request_id')

    if (!requestId) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'request_id is required' }
        })
    }

    const body = await readBody<RequestUpdatePayload | null>(event)

    if (!body || typeof body !== 'object' || typeof body.status !== 'string' || !body.status.trim()) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'status is required' }
        })
    }

    return await callPlatformApi(event, `/user-role-requests/${requestId}/approve`, {
        method: 'PUT',
        body
    })
})
