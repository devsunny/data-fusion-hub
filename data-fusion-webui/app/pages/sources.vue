<template>
  <div>
    <UiContentCard title="Data Sources" subtitle="Manage your data connections">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="source in sources"
          :key="source.id"
          class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
        >
          <div class="flex items-start justify-between mb-3">
            <UIcon :name="source.icon" class="w-8 h-8 text-blue-500" />
            <UBadge
              :color="source.status === 'connected' ? 'green' : 'red'"
              variant="subtle"
              size="sm"
            >
              {{ source.status }}
            </UBadge>
          </div>
          <h3 class="font-medium text-gray-900 mb-1">{{ source.name }}</h3>
          <p class="text-sm text-gray-600 mb-2">{{ source.type }}</p>
          <p class="text-xs text-gray-500">{{ source.description }}</p>
        </div>
      </div>
      
      <template #footer>
        <UButton color="primary" @click="showAddSource = true">
          Add Data Source
        </UButton>
      </template>
    </UiContentCard>

    <!-- Add Source Modal -->
    <UModal v-model="showAddSource">
      <UiContentCard title="Add New Data Source">
        <UForm :state="newSource" @submit="addSource">
          <UFormGroup label="Name" name="name" class="mb-4">
            <UInput v-model="newSource.name" placeholder="Enter source name" />
          </UFormGroup>
          <UFormGroup label="Type" name="type" class="mb-4">
            <USelect
              v-model="newSource.type"
              :options="['Database', 'API', 'File', 'Cloud Storage']"
            />
          </UFormGroup>
          <UFormGroup label="Connection String" name="connection" class="mb-4">
            <UInput v-model="newSource.connection" placeholder="Enter connection details" />
          </UFormGroup>
          <div class="flex justify-end space-x-3">
            <UButton color="gray" @click="showAddSource = false">Cancel</UButton>
            <UButton type="submit" color="primary">Add Source</UButton>
          </div>
        </UForm>
      </UiContentCard>
    </UModal>
  </div>
</template>

<script setup lang="ts">
// Set page meta
definePageMeta({
  title: 'Data Sources',
  subtitle: 'Manage your data connections'
})

const showAddSource = ref(false)

const newSource = ref({
  name: '',
  type: 'Database',
  connection: ''
})

const sources = ref([
  {
    id: 1,
    name: 'PostgreSQL Production',
    type: 'PostgreSQL',
    status: 'connected',
    icon: 'i-heroicons-circle-stack',
    description: 'Main production database'
  },
  {
    id: 2,
    name: 'Sales API',
    type: 'REST API',
    status: 'connected',
    icon: 'i-heroicons-cloud',
    description: 'External sales data API'
  },
  {
    id: 3,
    name: 'Customer CSV Dump',
    type: 'File',
    status: 'error',
    icon: 'i-heroicons-document',
    description: 'Weekly customer data export'
  },
  {
    id: 4,
    name: 'AWS S3 Bucket',
    type: 'Cloud Storage',
    status: 'connected',
    icon: 'i-heroicons-server',
    description: 'Raw data storage'
  }
])

const addSource = () => {
  sources.value.push({
    id: sources.value.length + 1,
    name: newSource.value.name,
    type: newSource.value.type,
    status: 'connected',
    icon: 'i-heroicons-circle-stack',
    description: 'Newly added data source'
  })
  showAddSource.value = false
  newSource.value = { name: '', type: 'Database', connection: '' }
}
</script>
