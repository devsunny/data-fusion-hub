import type { H3Event } from 'h3'
import { createError, readBody } from 'h3'

type DataFieldPayload = {
    name?: string
    type?: string
}

type DataObjectBulkPayload = {
    data_domain_id?: string
    data_objects?: Array<{
        name?: string
        type?: string
        data_domain_id?: string
        data_fields?: DataFieldPayload[]
    }>
}

export default defineEventHandler(async (event: H3Event) => {
    const body = await readBody<DataObjectBulkPayload | null>(event)

    if (!body || typeof body !== 'object' || typeof body.data_domain_id !== 'string' || !body.data_domain_id.trim() || !Array.isArray(body.data_objects) || body.data_objects.length === 0) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'data_domain_id and at least one data object are required' }
        })
    }

    for (const [index, dataObject] of body.data_objects.entries()) {
        if (!dataObject || typeof dataObject !== 'object') {
            throw createError({
                statusCode: 400,
                statusMessage: 'Bad Request',
                data: { message: `data_objects[${index}] must be an object` }
            })
        }

        if (typeof dataObject.name !== 'string' || !dataObject.name.trim() || typeof dataObject.type !== 'string' || !dataObject.type.trim()) {
            throw createError({
                statusCode: 400,
                statusMessage: 'Bad Request',
                data: { message: `data_objects[${index}] requires name and type` }
            })
        }

        if (!Array.isArray(dataObject.data_fields) || dataObject.data_fields.length === 0) {
            throw createError({
                statusCode: 400,
                statusMessage: 'Bad Request',
                data: { message: `data_objects[${index}] requires at least one data field` }
            })
        }

        for (const [fieldIndex, field] of dataObject.data_fields.entries()) {
            if (!field || typeof field !== 'object' || typeof field.name !== 'string' || !field.name.trim() || typeof field.type !== 'string' || !field.type.trim()) {
                throw createError({
                    statusCode: 400,
                    statusMessage: 'Bad Request',
                    data: { message: `data_objects[${index}].data_fields[${fieldIndex}] requires name and type` }
                })
            }
        }
    }

    return await callPlatformApi(event, '/data-objects/bulk', {
        method: 'POST',
        body
    })
})
