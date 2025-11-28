import type { H3Event } from 'h3'
import { createError, getQuery } from 'h3'

type QueryParams = {
    user_id?: string
}

export default defineEventHandler(async (event: H3Event) => {
    const { user_id: userId } = getQuery<QueryParams>(event)

    if (!userId || typeof userId !== 'string' || !userId.trim()) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'user_id query parameter is required' }
        })
    }

    return await callPlatformApi(event, '/user-role-requests/', {
        query: { user_id: userId }
    })
})
