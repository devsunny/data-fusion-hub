import type { H3Event } from 'h3'
import { createError, getRouterParam } from 'h3'

export default defineEventHandler(async (event: H3Event) => {
    const requestId = getRouterParam(event, 'request_id')

    if (!requestId) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'request_id is required' }
        })
    }

    return await callPlatformApi(event, `/user-role-requests/${requestId}`)
})
