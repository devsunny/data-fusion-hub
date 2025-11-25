<template>
  <div
    class="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow duration-200"
  >
    <div class="p-5">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <div
            class="flex items-center justify-center h-12 w-12 rounded-md"
            :class="iconColorClass"
          >
            <UIcon :name="icon" class="w-6 h-6 text-white" />
          </div>
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">
              {{ title }}
            </dt>
            <dd class="text-lg font-semibold text-gray-900">
              {{ value }}
            </dd>
          </dl>
        </div>
      </div>
    </div>
    <div v-if="change !== undefined" class="bg-gray-50 px-5 py-3">
      <div class="text-sm">
        <span
          class="font-medium"
          :class="change >= 0 ? 'text-green-600' : 'text-red-600'"
        >
          {{ change >= 0 ? '↑' : '↓' }} {{ Math.abs(change) }}%
        </span>
        <span class="text-gray-600 ml-1">from last period</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  value: string | number
  icon: string
  color?: 'primary' | 'success' | 'warning' | 'danger'
  change?: number
}

const props = withDefaults(defineProps<Props>(), {
  color: 'primary'
})

const iconColorClass = computed(() => {
  const colorMap = {
    primary: 'bg-blue-500',
    success: 'bg-green-500',
    warning: 'bg-yellow-500',
    danger: 'bg-red-500'
  }
  return colorMap[props.color]
})
</script>
