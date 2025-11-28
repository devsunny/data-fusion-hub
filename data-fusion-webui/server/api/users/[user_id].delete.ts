import type { H3Event } from 'h3'
import { createError, getRouterParam, setResponseStatus } from 'h3'

export default defineEventHandler(async (event: H3Event) => {
    const userId = getRouterParam(event, 'user_id')

    if (!userId) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'user_id is required' }
        })
    }

    await callPlatformApi(event, `/users/${userId}`, {
        method: 'DELETE',
        responseType: 'text'
    })

    setResponseStatus(event, 204)
    return null
})
