import type { H3Event } from 'h3'
import { createError, getQuery } from 'h3'

type ListParams = {
    page?: string
    size?: string
}

export default defineEventHandler(async (event: H3Event) => {
    const { page, size } = getQuery<ListParams>(event)

    const parsedPage = page !== undefined ? Number.parseInt(page, 10) : undefined
    const parsedSize = size !== undefined ? Number.parseInt(size, 10) : undefined

    if ((page && Number.isNaN(parsedPage)) || (size && Number.isNaN(parsedSize))) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'page and size must be integers' }
        })
    }

    const query = {
        page: parsedPage,
        size: parsedSize
    }

    return await callPlatformApi(event, '/datadomains/', { query })
})
