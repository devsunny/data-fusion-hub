import type { H3Event } from 'h3'
import { createError, readBody } from 'h3'

type DataConnectorPayload = {
    name?: string
    type?: string
    configuration?: Record<string, unknown>
    authentication?: Record<string, unknown> | null
}

export default defineEventHandler(async (event: H3Event) => {
    const body = await readBody<DataConnectorPayload | null>(event)

    if (!body || typeof body !== 'object' || typeof body.name !== 'string' || !body.name.trim() || typeof body.type !== 'string' || !body.type.trim() || typeof body.configuration !== 'object' || body.configuration === null) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: {
                message: 'name, type, and configuration are required'
            }
        })
    }

    return await callPlatformApi(event, '/dataconnectors/', {
        method: 'POST',
        body
    })
})
