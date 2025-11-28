import type { H3Event } from 'h3'
import { createError, getRouterParam, readBody } from 'h3'

type UserUpdatePayload = {
    email?: string
    first_name?: string
    last_name?: string
    password?: string | null
    middle_name?: string | null
}

export default defineEventHandler(async (event: H3Event) => {
    const userId = getRouterParam(event, 'user_id')

    if (!userId) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'user_id is required' }
        })
    }

    const body = await readBody<UserUpdatePayload | null>(event)

    if (!body || typeof body !== 'object') {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'payload is required' }
        })
    }

    return await callPlatformApi(event, `/users/${userId}`, {
        method: 'PUT',
        body
    })
})
