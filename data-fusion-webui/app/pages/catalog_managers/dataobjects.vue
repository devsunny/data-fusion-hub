<script setup lang="ts">
import type { DataObject } from '~/types/platform'

const { listDataObjects } = usePlatformApi()

const { data: objects, status, error, refresh } = await useAsyncData<DataObject[]>(
  'catalog-data-objects',
  () => listDataObjects(),
  { default: () => [] }
)

const search = ref('')

const filteredObjects = computed(() => {
  const term = search.value.trim()
  const data = objects.value ?? []

  if (!term) {
    return data
  }

  const matcher = new RegExp(term, 'i')

  return data.filter((object) => {
    return matcher.test(object.name) || matcher.test(object.type) || matcher.test(object.description ?? '') || matcher.test(object.data_domain_id)
  })
})

const total = computed(() => (objects.value ?? []).length)

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

const handleRefreshObjects = async (_event?: MouseEvent) => {
  await refresh()
}
</script>

<template>
  <div class="space-y-4">
    <UPageCard
      title="Data Objects"
      description="Objects registered within the Data Fusion Hub."
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
            placeholder="Search data objects"
            class="w-full sm:max-w-md"
          />

          <UButton
            icon="i-lucide-refresh-cw"
            color="neutral"
            variant="soft"
            :loading="status === 'pending'"
            @click="handleRefreshObjects"
          >
            Refresh
          </UButton>
        </div>
      </template>

      <div
        v-if="status === 'pending'"
        class="p-4 text-sm text-muted"
      >
        Loading data objects…
      </div>

      <div
        v-else-if="error"
        class="p-4 text-sm text-error space-y-2"
      >
        <p>Unable to load data objects from the platform API.</p>
        <UButton
          icon="i-lucide-refresh-cw"
          color="error"
          variant="subtle"
          size="sm"
          @click="handleRefreshObjects"
        >
          Try again
        </UButton>
      </div>

      <div
        v-else-if="!filteredObjects.length"
        class="p-4 text-sm text-muted"
      >
        No data objects match your search.
      </div>

      <ul
        v-else
        class="divide-y divide-default"
      >
        <li
          v-for="object in filteredObjects"
          :key="object.id"
          class="p-4 sm:p-6 space-y-2"
        >
          <div class="flex flex-wrap items-center justify-between gap-2">
            <h3 class="text-base font-semibold text-highlighted">
              {{ object.name }}
            </h3>
            <UBadge
              color="primary"
              variant="soft"
            >
              {{ object.type }}
            </UBadge>
          </div>
          <p class="text-sm text-muted">
            {{ object.description || 'No description provided.' }}
          </p>
          <p class="text-xs text-muted">
            Domain ID: {{ object.data_domain_id }}
          </p>
          <p class="text-xs text-muted">
            Updated {{ formatTimestamp(object.updated_at) }} · Created {{ formatTimestamp(object.created_at) }}
          </p>
        </li>
      </ul>
    </UPageCard>
  </div>
</template>
