<script setup lang="ts">
import type { Member } from '~/types'
import type { PlatformUser } from '~/types/platform'
import { platformUserToMember } from '~/utils'

const { listUsers } = usePlatformApi()

const { data: platformUsers, status, error } = await useAsyncData<PlatformUser[]>(
  'settings-platform-users',
  () => listUsers(),
  { default: () => [] }
)

const q = ref('')

const members = computed<Member[]>(() => {
  return (platformUsers.value ?? []).map(platformUserToMember)
})

const filteredMembers = computed(() => {
  const query = q.value.trim()
  if (!query) {
    return members.value
  }

  const matcher = new RegExp(query, 'i')

  return members.value.filter((member) => matcher.test(member.name) || matcher.test(member.username))
})
</script>

<template>
  <div>
    <UPageCard
      title="Members"
      description="Invite new members by email address."
      variant="naked"
      orientation="horizontal"
      class="mb-4"
    >
      <UButton
        label="Invite people"
        color="neutral"
        class="w-fit lg:ms-auto"
      />
    </UPageCard>

    <UPageCard variant="subtle" :ui="{ container: 'p-0 sm:p-0 gap-y-0', wrapper: 'items-stretch', header: 'p-4 mb-0 border-b border-default' }">
      <template #header>
        <UInput
          v-model="q"
          icon="i-lucide-search"
          placeholder="Search members"
          autofocus
          class="w-full"
        />
      </template>

      <div
        v-if="status === 'pending'"
        class="p-4 text-sm text-muted"
      >
        Loading members…
      </div>
      <div
        v-else-if="error"
        class="p-4 text-sm text-error"
      >
        Unable to load members from the platform API.
      </div>
      <SettingsMembersList
        v-else
        :members="filteredMembers"
      />
    </UPageCard>
  </div>
</template>
