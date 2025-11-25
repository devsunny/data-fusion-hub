<template>
  <div>
    <UiContentCard title="Fusion Pipelines" subtitle="Manage data transformation workflows">
      <div class="mb-6">
        <UButton color="primary" @click="showCreatePipeline = true">
          Create Pipeline
        </UButton>
      </div>
      
      <div class="space-y-4">
        <div
          v-for="pipeline in pipelines"
          :key="pipeline.id"
          class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
        >
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center space-x-3">
              <UIcon name="i-heroicons-arrow-path" class="w-6 h-6 text-blue-500" />
              <div>
                <h3 class="font-medium text-gray-900">{{ pipeline.name }}</h3>
                <p class="text-sm text-gray-600">{{ pipeline.description }}</p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <UBadge
                :color="pipeline.status === 'running' ? 'green' : pipeline.status === 'paused' ? 'yellow' : 'gray'"
                variant="subtle"
              >
                {{ pipeline.status }}
              </UBadge>
              <UButton
                :color="pipeline.status === 'running' ? 'red' : 'green'"
                size="sm"
                variant="soft"
                @click="togglePipeline(pipeline)"
              >
                {{ pipeline.status === 'running' ? 'Stop' : 'Start' }}
              </UButton>
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span class="text-gray-500">Source:</span>
              <span class="ml-1 font-medium">{{ pipeline.source }}</span>
            </div>
            <div>
              <span class="text-gray-500">Target:</span>
              <span class="ml-1 font-medium">{{ pipeline.target }}</span>
            </div>
            <div>
              <span class="text-gray-500">Last Run:</span>
              <span class="ml-1 font-medium">{{ pipeline.lastRun }}</span>
            </div>
          </div>
        </div>
      </div>
    </UiContentCard>

    <!-- Create Pipeline Modal -->
    <UModal v-model="showCreatePipeline">
      <UiContentCard title="Create New Pipeline">
        <UForm :state="newPipeline" @submit="createPipeline">
          <UFormGroup label="Pipeline Name" name="name" class="mb-4">
            <UInput v-model="newPipeline.name" placeholder="Enter pipeline name" />
          </UFormGroup>
          <UFormGroup label="Description" name="description" class="mb-4">
            <UTextarea v-model="newPipeline.description" placeholder="Enter description" />
          </UFormGroup>
          <UFormGroup label="Source" name="source" class="mb-4">
            <USelect
              v-model="newPipeline.source"
              :options="['PostgreSQL Production', 'Sales API', 'AWS S3 Bucket']"
            />
          </UFormGroup>
          <UFormGroup label="Target" name="target" class="mb-4">
            <USelect
              v-model="newPipeline.target"
              :options="['Data Warehouse', 'Analytics DB', 'Export']"
            />
          </UFormGroup>
          <div class="flex justify-end space-x-3">
            <UButton color="gray" @click="showCreatePipeline = false">Cancel</UButton>
            <UButton type="submit" color="primary">Create Pipeline</UButton>
          </div>
        </UForm>
      </UiContentCard>
    </UModal>
  </div>
</template>

<script setup lang="ts">
// Set page meta
definePageMeta({
  title: 'Fusion Pipelines',
  subtitle: 'Manage data transformation workflows'
})

const showCreatePipeline = ref(false)

const newPipeline = ref({
  name: '',
  description: '',
  source: 'PostgreSQL Production',
  target: 'Data Warehouse'
})

const pipelines = ref([
  {
    id: 1,
    name: 'Sales Data ETL',
    description: 'Extract and transform daily sales data',
    status: 'running',
    source: 'Sales API',
    target: 'Data Warehouse',
    lastRun: '2 minutes ago'
  },
  {
    id: 2,
    name: 'Customer Data Sync',
    description: 'Sync customer data from PostgreSQL to Analytics DB',
    status: 'paused',
    source: 'PostgreSQL Production',
    target: 'Analytics DB',
    lastRun: '1 hour ago'
  },
  {
    id: 3,
    name: 'CSV Import Pipeline',
    description: 'Import and process CSV files from S3',
    status: 'stopped',
    source: 'AWS S3 Bucket',
    target: 'Export',
    lastRun: '3 days ago'
  }
])

const togglePipeline = (pipeline: any) => {
  if (pipeline.status === 'running') {
    pipeline.status = 'paused'
  } else {
    pipeline.status = 'running'
  }
}

const createPipeline = () => {
  pipelines.value.push({
    id: pipelines.value.length + 1,
    name: newPipeline.value.name,
    description: newPipeline.value.description,
    status: 'paused',
    source: newPipeline.value.source,
    target: newPipeline.value.target,
    lastRun: 'Not yet run'
  })
  showCreatePipeline.value = false
  newPipeline.value = {
    name: '',
    description: '',
    source: 'PostgreSQL Production',
    target: 'Data Warehouse'
  }
}
</script>
