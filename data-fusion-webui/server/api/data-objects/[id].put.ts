import type { H3Event } from 'h3'
import { createError, getRouterParam, readBody } from 'h3'

type DataObjectUpdatePayload = {
    name?: string | null
    description?: string | null
    type?: string | null
    data_domain_id?: string | null
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

    const body = await readBody<DataObjectUpdatePayload | null>(event)

    if (!body || typeof body !== 'object') {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'payload is required' }
        })
    }

    return await callPlatformApi(event, `/data-objects/${id}`, {
        method: 'PUT',
        body
    })
})
