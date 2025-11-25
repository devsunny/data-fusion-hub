<template>
  <div>
    <UiContentCard title="Analytics" subtitle="Data insights and visualizations">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Data Quality Metrics -->
        <UiContentCard title="Data Quality Score" :subtitle="`Overall: ${overallQuality}%`">
          <div class="space-y-4">
            <div
              v-for="metric in qualityMetrics"
              :key="metric.name"
            >
              <div class="flex justify-between mb-1">
                <span class="text-sm font-medium text-gray-700">{{ metric.name }}</span>
                <span class="text-sm text-gray-600">{{ metric.score }}%</span>
              </div>
              <UProgress :value="metric.score" :color="getProgressColor(metric.score)" />
            </div>
          </div>
        </UiContentCard>

        <!-- Processing Stats -->
        <UiContentCard title="Processing Statistics">
          <div class="grid grid-cols-2 gap-4">
            <div class="text-center p-4 bg-gray-50 rounded-lg">
              <div class="text-2xl font-bold text-blue-600">{{ processingStats.recordsProcessed }}</div>
              <div class="text-sm text-gray-600">Records Processed</div>
            </div>
            <div class="text-center p-4 bg-gray-50 rounded-lg">
              <div class="text-2xl font-bold text-green-600">{{ processingStats.successRate }}%</div>
              <div class="text-sm text-gray-600">Success Rate</div>
            </div>
            <div class="text-center p-4 bg-gray-50 rounded-lg">
              <div class="text-2xl font-bold text-yellow-600">{{ processingStats.avgProcessingTime }}s</div>
              <div class="text-sm text-gray-600">Avg Processing Time</div>
            </div>
            <div class="text-center p-4 bg-gray-50 rounded-lg">
              <div class="text-2xl font-bold text-purple-600">{{ processingStats.activeJobs }}</div>
              <div class="text-sm text-gray-600">Active Jobs</div>
            </div>
          </div>
        </UiContentCard>

        <!-- Recent Errors -->
        <UiContentCard title="Recent Errors" subtitle="Last 24 hours">
          <div class="space-y-3">
            <div
              v-for="error in recentErrors"
              :key="error.id"
              class="flex items-start space-x-3 p-3 bg-red-50 rounded-lg"
            >
              <UIcon name="i-heroicons-exclamation-circle" class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
              <div class="flex-1">
                <p class="text-sm font-medium text-red-800">{{ error.message }}</p>
                <p class="text-xs text-red-600">{{ error.source }} • {{ error.time }}</p>
              </div>
            </div>
          </div>
        </UiContentCard>

        <!-- Data Volume Trends -->
        <UiContentCard title="Data Volume Trends">
          <div class="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
            <div class="text-center">
              <UIcon name="i-heroicons-chart-bar" class="w-12 h-12 text-gray-400 mx-auto mb-2" />
              <p class="text-sm text-gray-600">Chart visualization will be implemented</p>
              <p class="text-xs text-gray-500">Using a chart library in future iteration</p>
            </div>
          </div>
        </UiContentCard>
      </div>
    </UiContentCard>
  </div>
</template>

<script setup lang="ts">
// Set page meta
definePageMeta({
  title: 'Analytics',
  subtitle: 'Data insights and visualizations'
})

const overallQuality = 87

const qualityMetrics = [
  { name: 'Completeness', score: 92 },
  { name: 'Accuracy', score: 85 },
  { name: 'Consistency', score: 88 },
  { name: 'Timeliness', score: 90 }
]

const processingStats = {
  recordsProcessed: '2.4M',
  successRate: 96.5,
  avgProcessingTime: 2.3,
  activeJobs: 12
}

const recentErrors = [
  {
    id: 1,
    message: 'Connection timeout to PostgreSQL server',
    source: 'PostgreSQL Production',
    time: '2 hours ago'
  },
  {
    id: 2,
    message: 'Invalid data format in CSV file',
    source: 'CSV Import Pipeline',
    time: '5 hours ago'
  },
  {
    id: 3,
    message: 'API rate limit exceeded',
    source: 'Sales API',
    time: '8 hours ago'
  }
]

const getProgressColor = (score: number) => {
  if (score >= 90) return 'green'
  if (score >= 70) return 'yellow'
  return 'red'
}
</script>
