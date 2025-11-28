<script setup lang="ts">
import type { DataConnector, PaginatedResponse } from '~/types/platform'

const { listDataConnectors } = usePlatformApi()

const emptyResponse = (): PaginatedResponse<DataConnector> => ({
  data: [],
  pagination: {
    page: 1,
    size: 0,
    total: 0,
    pages: 0
  }
})

const { data: response, status, error, refresh } = await useAsyncData<PaginatedResponse<DataConnector>>(
  'catalog-data-connectors',
  () => listDataConnectors({ page: 1, size: 50 }),
  { default: emptyResponse }
)

const search = ref('')

const connectors = computed<DataConnector[]>(() => response.value?.data ?? [])

const handleRefreshConnectors = async (_event?: MouseEvent) => {
  await refresh()
}

const filteredConnectors = computed(() => {
  const term = search.value.trim()
  if (!term) {
    return connectors.value
  }

  const matcher = new RegExp(term, 'i')
  return connectors.value.filter((connector) => {
    return matcher.test(connector.name) || matcher.test(connector.type) || matcher.test(connector.description ?? '')
  })
})

const total = computed(() => response.value?.pagination.total ?? connectors.value.length)

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
      title="Data Connectors"
      description="Connectors configured in the Data Fusion Hub platform."
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
            placeholder="Search data connectors"
            class="w-full sm:max-w-md"
          />

          <UButton
            icon="i-lucide-refresh-cw"
            color="neutral"
            variant="soft"
            :loading="status === 'pending'"
            @click="handleRefreshConnectors"
          >
            Refresh
          </UButton>
        </div>
      </template>

      <div
        v-if="status === 'pending'"
        class="p-4 text-sm text-muted"
      >
        Loading data connectors…
      </div>

      <div
        v-else-if="error"
        class="p-4 text-sm text-error space-y-2"
      >
        <p>Unable to load data connectors from the platform API.</p>
        <UButton
          icon="i-lucide-refresh-cw"
          color="error"
          variant="subtle"
          size="sm"
          @click="handleRefreshConnectors"
        >
          Try again
        </UButton>
      </div>

      <div
        v-else-if="!filteredConnectors.length"
        class="p-4 text-sm text-muted"
      >
        No data connectors match your search.
      </div>

      <ul
        v-else
        class="divide-y divide-default"
      >
        <li
          v-for="connector in filteredConnectors"
          :key="connector.id"
          class="p-4 sm:p-6 space-y-2"
        >
          <div class="flex flex-wrap items-center justify-between gap-2">
            <h3 class="text-base font-semibold text-highlighted">
              {{ connector.name }}
            </h3>
            <UBadge
              color="primary"
              variant="soft"
            >
              {{ connector.type }}
            </UBadge>
          </div>
          <p class="text-sm text-muted">
            {{ connector.description || 'No description provided.' }}
          </p>
          <p class="text-xs text-muted">
            Updated {{ formatTimestamp(connector.updated_at) }} · Created {{ formatTimestamp(connector.created_at) }}
          </p>
        </li>
      </ul>
    </UPageCard>
  </div>
</template>
