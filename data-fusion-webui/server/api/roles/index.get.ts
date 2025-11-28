import type { H3Event } from 'h3'
import { createError, getQuery } from 'h3'

type ListParams = {
    skip?: string
    limit?: string
}

export default defineEventHandler(async (event: H3Event) => {
    const { skip, limit } = getQuery<ListParams>(event)

    const parsedSkip = skip !== undefined ? Number.parseInt(skip, 10) : undefined
    const parsedLimit = limit !== undefined ? Number.parseInt(limit, 10) : undefined

    if ((skip && Number.isNaN(parsedSkip)) || (limit && Number.isNaN(parsedLimit))) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'skip and limit must be integers' }
        })
    }

    const query = {
        skip: parsedSkip,
        limit: parsedLimit
    }

    return await callPlatformApi(event, '/roles/', { query })
})
