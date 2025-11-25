<template>
  <footer class="bg-white border-t border-gray-200 py-4">
    <div class="px-4 sm:px-6 lg:px-8">
      <div class="text-center">
        <p class="text-sm text-gray-500">
          © {{ currentYear }} Data Fusion Hub. All rights reserved.
        </p>
        <p class="text-xs text-gray-400 mt-1">
          Built with Nuxt 3 and TypeScript
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const currentYear = computed(() => new Date().getFullYear())
</script>
