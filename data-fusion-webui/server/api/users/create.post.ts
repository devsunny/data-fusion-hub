import type { H3Event } from 'h3'
import { createError, readBody } from 'h3'

type UserCreatePayload = {
    email?: string
    first_name?: string
    last_name?: string
    password?: string | null
    middle_name?: string | null
}

export default defineEventHandler(async (event: H3Event) => {
    const body = await readBody<UserCreatePayload | null>(event)

    if (!body || typeof body !== 'object' || typeof body.email !== 'string' || !body.email.trim() || typeof body.first_name !== 'string' || !body.first_name.trim() || typeof body.last_name !== 'string' || !body.last_name.trim()) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'email, first_name, and last_name are required' }
        })
    }

    return await callPlatformApi(event, '/users/create', {
        method: 'POST',
        body
    })
})
