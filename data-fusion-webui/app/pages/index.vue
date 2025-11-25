<template>
  <div>
    <!-- Stats Cards Grid -->
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
      <UiStatsCard
        title="Total Data Sources"
        :value="12"
        icon="i-heroicons-circle-stack"
        color="primary"
        :change="12"
      />
      <UiStatsCard
        title="Active Pipelines"
        :value="8"
        icon="i-heroicons-arrow-path"
        color="success"
        :change="8"
      />
      <UiStatsCard
        title="Data Objects"
        :value="1,247"
        icon="i-heroicons-table-cells"
        color="warning"
        :change="-3"
      />
      <UiStatsCard
        title="System Health"
        value="98%"
        icon="i-heroicons-heart"
        color="danger"
        :change="2"
      />
    </div>

    <!-- Content Cards -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Recent Activity -->
      <UiContentCard title="Recent Activity" subtitle="Latest data fusion operations">
        <ul class="divide-y divide-gray-200">
          <li
            v-for="activity in recentActivity"
            :key="activity.id"
            class="py-4 flex items-center space-x-3"
          >
            <UIcon
              :name="activity.icon"
              class="w-5 h-5 flex-shrink-0"
              :class="activity.color"
            />
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">
                {{ activity.description }}
              </p>
              <p class="text-xs text-gray-500">
                {{ activity.time }}
              </p>
            </div>
          </li>
        </ul>
        
        <template #footer>
          <UButton
            color="primary"
            variant="ghost"
            size="sm"
            to="/activity"
          >
            View all activity
          </UButton>
        </template>
      </UiContentCard>

      <!-- Data Sources Overview -->
      <UiContentCard title="Data Sources" subtitle="Connected data sources status">
        <div class="space-y-4">
          <div
            v-for="source in dataSources"
            :key="source.id"
            class="flex items-center justify-between"
          >
            <div class="flex items-center space-x-3">
              <UIcon
                :name="source.icon"
                class="w-5 h-5 text-gray-600"
              />
              <div>
                <p class="text-sm font-medium text-gray-900">
                  {{ source.name }}
                </p>
                <p class="text-xs text-gray-500">
                  {{ source.type }}
                </p>
              </div>
            </div>
            <UBadge
              :color="source.status === 'connected' ? 'green' : 'red'"
              variant="subtle"
              size="sm"
            >
              {{ source.status }}
            </UBadge>
          </div>
        </div>
        
        <template #footer>
          <UButton
            color="primary"
            variant="ghost"
            size="sm"
            to="/sources"
          >
            Manage sources
          </UButton>
        </template>
      </UiContentCard>
    </div>
  </div>
</template>

<script setup lang="ts">
// Set page meta
definePageMeta({
  title: 'Dashboard',
  subtitle: 'Welcome to Data Fusion Hub'
})

// Sample data for dashboard
const recentActivity = [
  {
    id: 1,
    description: 'Data pipeline "Sales ETL" completed successfully',
    time: '2 minutes ago',
    icon: 'i-heroicons-check-circle',
    color: 'text-green-500'
  },
  {
    id: 2,
    description: 'New data source "PostgreSQL Prod" added',
    time: '15 minutes ago',
    icon: 'i-heroicons-plus-circle',
    color: 'text-blue-500'
  },
  {
    id: 3,
    description: 'Data quality check detected 3 anomalies',
    time: '1 hour ago',
    icon: 'i-heroicons-exclamation-triangle',
    color: 'text-yellow-500'
  },
  {
    id: 4,
    description: 'Scheduled fusion job started',
    time: '2 hours ago',
    icon: 'i-heroicons-play-circle',
    color: 'text-gray-500'
  }
]

const dataSources = [
  {
    id: 1,
    name: 'PostgreSQL Production',
    type: 'Database',
    status: 'connected',
    icon: 'i-heroicons-circle-stack'
  },
  {
    id: 2,
    name: 'Sales API',
    type: 'REST API',
    status: 'connected',
    icon: 'i-heroicons-cloud'
  },
  {
    id: 3,
    name: 'Legacy CSV Files',
    type: 'File System',
    status: 'error',
    icon: 'i-heroicons-document'
  }
]
</script>
