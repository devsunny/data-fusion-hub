<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Top Navigation -->
    <LayoutTopNav />

    <!-- Sidebar -->
    <LayoutSidebar />

    <!-- Mobile menu overlay -->
    <div
      v-if="isMobileMenuOpen && isMobile"
      @click="closeMobileMenu"
      class="fixed inset-0 bg-black bg-opacity-50 z-30 lg:hidden"
    />

    <!-- Main Content Area -->
    <main
      :class="[
        'transition-all duration-300 pt-16',
        isMobile ? 'ml-0' : (isSidebarCollapsed ? 'ml-16' : 'ml-64')
      ]"
    >
      <div class="p-4 sm:p-6 lg:p-8">
        <!-- Page Header -->
        <div class="mb-6">
          <h1 class="text-2xl font-semibold text-gray-900">
            {{ pageTitle }}
          </h1>
          <p v-if="pageSubtitle" class="mt-1 text-sm text-gray-600">
            {{ pageSubtitle }}
          </p>
        </div>

        <!-- Page Content -->
        <slot />
      </div>

      <!-- Footer -->
      <LayoutFooter />
    </main>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const { isSidebarCollapsed, isMobile, isMobileMenuOpen, closeMobileMenu, initResponsive } = useLayout()

// Initialize responsive behavior
onMounted(() => {
  initResponsive()
})

// Page title from route meta or use a default
const pageTitle = computed(() => {
  return route.meta.title || 'Dashboard'
})

const pageSubtitle = computed(() => {
  return route.meta.subtitle || ''
})
</script>

<style scoped>
/* Ensure smooth transitions for layout changes */
main {
  min-height: calc(100vh - 4rem); /* Account for top nav */
}
</style>
