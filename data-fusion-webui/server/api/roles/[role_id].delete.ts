import type { H3Event } from 'h3'
import { createError, getRouterParam, setResponseStatus } from 'h3'

export default defineEventHandler(async (event: H3Event) => {
    const roleId = getRouterParam(event, 'role_id')

    if (!roleId) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'role_id is required' }
        })
    }

    await callPlatformApi(event, `/roles/${roleId}`, {
        method: 'DELETE',
        responseType: 'text'
    })

    setResponseStatus(event, 204)
    return null
})
