<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { PlatformUser } from '~/types/platform'

const { listUsers } = usePlatformApi()

const { data: users, status, error, refresh } = await useAsyncData<PlatformUser[]>(
  'platform-users',
  () => listUsers(),
  { default: () => [] }
)

const search = ref('')

const total = computed(() => (users.value ?? []).length)

const handleRefreshUsers = async (_event?: MouseEvent) => {
  await refresh()
}

function formatName(user: PlatformUser): string {
  return [user.first_name, user.last_name].filter(Boolean).join(' ').trim() || user.email
}

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

const filteredUsers = computed<PlatformUser[]>(() => {
  const term = search.value.trim()
  const data = users.value ?? []

  if (!term) {
    return data
  }

  const matcher = new RegExp(term, 'i')

  return data.filter((user) => matcher.test(user.email) || matcher.test(formatName(user)))
})

const columns: TableColumn<PlatformUser>[] = [
  {
    accessorKey: 'id',
    header: 'ID',
    cell: ({ row }) => String(row.getValue('id'))
  },
  {
    accessorKey: 'first_name',
    header: 'Name',
    cell: ({ row }) => formatName(row.original)
  },
  {
    accessorKey: 'email',
    header: 'Email'
  },
  {
    accessorKey: 'created_at',
    header: 'Created',
    cell: ({ row }) => formatTimestamp(row.original.created_at)
  },
  {
    accessorKey: 'updated_at',
    header: 'Updated',
    cell: ({ row }) => formatTimestamp(row.original.updated_at)
  }
]
</script>

<template>
  <UDashboardPanel id="users">
    <template #header>
      <UDashboardNavbar title="Users">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
          <UButton
            icon="i-lucide-refresh-cw"
            color="neutral"
            variant="ghost"
            :loading="status === 'pending'"
            @click="handleRefreshUsers"
          >
            Refresh
          </UButton>
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <div class="flex flex-wrap items-center justify-between gap-2 mb-4">
        <UInput
          v-model="search"
          class="w-full sm:max-w-lg"
          icon="i-lucide-search"
          placeholder="Search by name or email"
        />

        <UBadge
          color="neutral"
          variant="subtle"
          :label="`${filteredUsers.length} / ${total} users`"
        />
      </div>

      <div
        v-if="error"
        class="mb-4 rounded-lg border border-error/40 bg-error/10 p-4 text-sm text-error space-y-2"
      >
        <p>Unable to load users from the platform API.</p>
        <UButton
          icon="i-lucide-refresh-cw"
          color="error"
          variant="subtle"
          size="sm"
          @click="handleRefreshUsers"
        >
          Try again
        </UButton>
      </div>

      <UTable
        :data="filteredUsers"
        :columns="columns"
        :loading="status === 'pending'"
        class="shrink-0"
        :ui="{
          base: 'table-fixed border-separate border-spacing-0',
          thead: '[&>tr]:bg-elevated/50 [&>tr]:after:content-none',
          tbody: '[&>tr]:last:[&>td]:border-b-0',
          th: 'py-2 first:rounded-l-lg last:rounded-r-lg border-y border-default first:border-l last:border-r',
          td: 'border-b border-default'
        }"
      />

      <div
        v-if="status === 'success' && !filteredUsers.length"
        class="mt-4 text-sm text-muted"
      >
        No users match your search.
      </div>
    </template>
  </UDashboardPanel>
</template>
