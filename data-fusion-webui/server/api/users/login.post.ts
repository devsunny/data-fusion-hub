import type { H3Event } from 'h3'
import { createError, readBody } from 'h3'

type LoginPayload = {
    email?: string
    password?: string
}

export default defineEventHandler(async (event: H3Event) => {
    const body = await readBody<LoginPayload | null>(event)

    if (!body || typeof body !== 'object' || typeof body.email !== 'string' || !body.email.trim() || typeof body.password !== 'string' || !body.password.trim()) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'email and password are required' }
        })
    }

    return await callPlatformApi(event, '/users/login', {
        method: 'POST',
        body
    })
})
