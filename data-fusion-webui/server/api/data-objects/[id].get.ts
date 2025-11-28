import type { H3Event } from 'h3'
import { createError, getRouterParam } from 'h3'

export default defineEventHandler(async (event: H3Event) => {
    const id = getRouterParam(event, 'id')

    if (!id) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'id is required' }
        })
    }

    return await callPlatformApi(event, `/data-objects/${id}`)
})
