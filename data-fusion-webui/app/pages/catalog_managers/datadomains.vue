<script setup lang="ts">
import type { DataDomain, PaginatedResponse } from '~/types/platform'

const { listDataDomains } = usePlatformApi()

const emptyResponse = (): PaginatedResponse<DataDomain> => ({
  data: [],
  pagination: {
    page: 1,
    size: 0,
    total: 0,
    pages: 0
  }
})

const { data: response, status, error, refresh } = await useAsyncData<PaginatedResponse<DataDomain>>(
  'catalog-data-domains',
  () => listDataDomains({ page: 1, size: 50 }),
  { default: emptyResponse }
)

const search = ref('')

const domains = computed<DataDomain[]>(() => response.value?.data ?? [])

const handleRefreshDomains = async (_event?: MouseEvent) => {
  await refresh()
}

const filteredDomains = computed(() => {
  const term = search.value.trim()
  if (!term) {
    return domains.value
  }

  const matcher = new RegExp(term, 'i')
  return domains.value.filter((domain) => matcher.test(domain.name) || matcher.test(domain.description ?? ''))
})

const total = computed(() => response.value?.pagination.total ?? domains.value.length)

function formatTimestamp(value?: string | null): string {
  if (!value) {
    return '—'
  }

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return value
  }

  return date.toLocaleString()
}
</script>

<template>
  <div class="space-y-4">
    <UPageCard
      title="Data Domains"
      description="Domains sourced from the Data Fusion Hub platform."
      variant="naked"
      orientation="horizontal"
      class="mb-2"
    >
      <UBadge
        color="neutral"
        variant="subtle"
        :label="`${total} total`"
        class="ms-auto"
      />
    </UPageCard>

    <UPageCard variant="subtle" :ui="{ container: 'p-0 sm:p-0 gap-y-0', wrapper: 'items-stretch', header: 'p-4 mb-0 border-b border-default' }">
      <template #header>
        <div class="flex flex-col gap-2 w-full sm:flex-row sm:items-center sm:justify-between">
          <UInput
            v-model="search"
            icon="i-lucide-search"
            placeholder="Search data domains"
            class="w-full sm:max-w-md"
          />

          <UButton
            icon="i-lucide-refresh-cw"
            color="neutral"
            variant="soft"
            :loading="status === 'pending'"
            @click="handleRefreshDomains"
          >
            Refresh
          </UButton>
        </div>
      </template>

      <div
        v-if="status === 'pending'"
        class="p-4 text-sm text-muted"
      >
        Loading data domains…
      </div>

      <div
        v-else-if="error"
        class="p-4 text-sm text-error space-y-2"
      >
        <p>Unable to load data domains from the platform API.</p>
        <UButton
          icon="i-lucide-refresh-cw"
          color="error"
          variant="subtle"
          size="sm"
          @click="handleRefreshDomains"
        >
          Try again
        </UButton>
      </div>

      <div
        v-else-if="!filteredDomains.length"
        class="p-4 text-sm text-muted"
      >
        No data domains match your search.
      </div>

      <ul
        v-else
        class="divide-y divide-default"
      >
        <li
          v-for="domain in filteredDomains"
          :key="domain.id"
          class="p-4 sm:p-6"
        >
          <div class="flex flex-wrap items-center justify-between gap-2">
            <h3 class="text-base font-semibold text-highlighted">
              {{ domain.name }}
            </h3>
            <span class="text-xs text-muted">
              Updated {{ formatTimestamp(domain.updated_at) }}
            </span>
          </div>
          <p class="mt-2 text-sm text-muted">
            {{ domain.description || 'No description provided.' }}
          </p>
        </li>
      </ul>
    </UPageCard>
  </div>
</template>
