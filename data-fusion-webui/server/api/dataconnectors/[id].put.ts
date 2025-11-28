import type { H3Event } from 'h3'
import { createError, getRouterParam, readBody } from 'h3'

type DataConnectorUpdatePayload = {
    name?: string | null
    description?: string | null
    type?: string | null
    configuration?: Record<string, unknown> | null
    authentication?: Record<string, unknown> | null
}

export default defineEventHandler(async (event: H3Event) => {
    const id = getRouterParam(event, 'id')

    if (!id) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'id is required' }
        })
    }

    const body = await readBody<DataConnectorUpdatePayload | null>(event)

    if (!body || typeof body !== 'object') {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'payload is required' }
        })
    }

    return await callPlatformApi(event, `/dataconnectors/${id}`, {
        method: 'PUT',
        body
    })
})
