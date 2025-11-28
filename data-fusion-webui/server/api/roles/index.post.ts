import type { H3Event } from 'h3'
import { createError, readBody } from 'h3'

type RoleCreatePayload = {
    name?: string
    description?: string | null
}

export default defineEventHandler(async (event: H3Event) => {
    const body = await readBody<RoleCreatePayload | null>(event)

    if (!body || typeof body !== 'object' || typeof body.name !== 'string' || !body.name.trim()) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'name is required' }
        })
    }

    return await callPlatformApi(event, '/roles/', {
        method: 'POST',
        body
    })
})
