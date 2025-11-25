<template>
  <div class="bg-white shadow rounded-lg overflow-hidden">
    <!-- Card Header -->
    <div v-if="title || $slots.header" class="px-6 py-4 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <div>
          <h3 v-if="title" class="text-lg font-medium text-gray-900">
            {{ title }}
          </h3>
          <p v-if="subtitle" class="mt-1 text-sm text-gray-600">
            {{ subtitle }}
          </p>
        </div>
        <slot name="header-actions" />
      </div>
    </div>

    <!-- Card Body -->
    <div class="px-6 py-4">
      <slot />
    </div>

    <!-- Card Footer -->
    <div v-if="$slots.footer" class="px-6 py-4 bg-gray-50 border-t border-gray-200">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title?: string
  subtitle?: string
}

defineProps<Props>()
</script>
