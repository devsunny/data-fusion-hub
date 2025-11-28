import type { H3Event } from 'h3'
import { createError, getRouterParam, readBody } from 'h3'

type AssignPayload = string[]

export default defineEventHandler(async (event: H3Event) => {
    const roleId = getRouterParam(event, 'role_id')

    if (!roleId) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'role_id is required' }
        })
    }

    const body = await readBody<AssignPayload | null>(event)

    if (!Array.isArray(body) || body.length === 0 || body.some(item => typeof item !== 'string' || !item.trim())) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Bad Request',
            data: { message: 'approver role ids must be a non-empty array of strings' }
        })
    }

    return await callPlatformApi(event, `/roles/${roleId}/approver-roles/`, {
        method: 'PUT',
        body
    })
})
