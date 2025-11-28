import type { H3Event } from 'h3'
import { createError, getRequestHeader } from 'h3'
import { ofetch, type FetchError, type FetchOptions, type ResponseType } from 'ofetch'

export type PlatformApiOptions = Omit<Partial<FetchOptions<ResponseType>>, 'baseURL' | 'query'> & {
    query?: Record<string, string | number | boolean | null | undefined>
}

export async function callPlatformApi<T = unknown>(event: H3Event, path: string, options: PlatformApiOptions = {}): Promise<T> {
    const runtimeConfig = useRuntimeConfig()
    const headers = new Headers(options.headers ?? {})

    const authHeader = getRequestHeader(event, 'authorization')
    if (authHeader && !headers.has('authorization')) {
        headers.set('authorization', authHeader)
    }

    if (runtimeConfig.platformApiKey && !headers.has('x-api-key')) {
        headers.set('x-api-key', runtimeConfig.platformApiKey as string)
    }

    const { query: rawQuery, ...restOptions } = options
    const query = rawQuery ? normalizeQuery(rawQuery) : undefined

    try {
        const fetchOptions = {
            ...(restOptions as FetchOptions<ResponseType>),
            baseURL: runtimeConfig.platformApiBaseUrl as string,
            headers,
            query,
            retry: false
        } as FetchOptions<ResponseType>

        const result = await ofetch(path, fetchOptions)

        return result as T
    } catch (error: unknown) {
        if (isFetchError(error)) {
            const statusCode = error.response?.status ?? 500
            const statusMessage = error.response?.statusText
            const data = error.data ?? {
                message: 'Platform API request failed'
            }

            if (statusCode >= 400) {
                logPlatformApiError({
                    statusCode,
                    statusMessage,
                    path,
                    body: (restOptions as FetchOptions<ResponseType>).body,
                    query,
                    data
                })
            }

            throw createError({
                statusCode,
                statusMessage,
                data
            })
        }

        throw error
    }
}

function normalizeQuery(query: Record<string, string | number | boolean | null | undefined>) {
    const params: Record<string, string> = {}

    for (const [key, value] of Object.entries(query)) {
        if (value === undefined || value === null || value === '') {
            continue
        }

        params[key] = typeof value === 'string' ? value : String(value)
    }

    return params
}

function isFetchError(error: unknown): error is FetchError<unknown> {
    return Boolean(error) && typeof error === 'object' && 'response' in (error as Record<string, unknown>)
}

function logPlatformApiError(details: Record<string, unknown>): void {
    if (process.env.NODE_ENV === 'test') {
        return
    }

    console.error('Platform API error', details)
}
