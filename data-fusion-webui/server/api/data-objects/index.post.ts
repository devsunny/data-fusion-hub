import type { H3Event } from 'h3'
import { createError, readBody } from 'h3'

type DataObjectPayload = {
    name?: string
    type?: string
    data_domain_id?: string
    description?: string | null
}

export default defineEventHandler(async (event: H3Event) => {
    const body = await readBody<DataObjectPayload | null>(event)

    if (!body || typeof body !== 'object' || typeof body.name !== 'string' || !body.name.trim() || typeof body.type !== 'string' || !body.type.trim() || typeof body.data_domain_id !== 'string' || !body.data_domain_id.trim()) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: {
                message: 'name, type, and data_domain_id are required'
            }
        })
    }

    return await callPlatformApi(event, '/data-objects/', {
        method: 'POST',
        body
    })
})
