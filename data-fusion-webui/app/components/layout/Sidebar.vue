<template>
  <aside
    :class="[
      'fixed left-0 top-16 h-full bg-white border-r border-gray-200 transition-all duration-300 z-40',
      isMobile ? 'w-64' : (isSidebarCollapsed ? 'w-16' : 'w-64')
    ]"
  >
    <!-- Sidebar content -->
    <div class="flex flex-col h-full">
      <!-- Navigation menu -->
      <nav class="flex-1 px-2 py-4 space-y-1">
        <NuxtLink
          v-for="item in navigationItems"
          :key="item.path"
          :to="item.path"
          @click="handleNavClick"
          class="flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors"
          :class="[
            isActiveRoute(item.path)
              ? 'bg-blue-50 text-blue-600'
              : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
          ]"
        >
          <UIcon
            :name="item.icon"
            class="w-5 h-5 flex-shrink-0"
            :class="isSidebarCollapsed && !isMobile ? 'mx-auto' : 'mr-3'"
          />
          <span
            v-if="!isSidebarCollapsed || isMobile"
            class="transition-opacity duration-300"
          >
            {{ item.label }}
          </span>
        </NuxtLink>
      </nav>

      <!-- Sidebar footer (collapse button) -->
      <div
        v-if="!isMobile"
        class="p-4 border-t border-gray-200"
      >
        <button
          @click="toggleSidebar"
          class="flex items-center justify-center w-full px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md"
        >
          <UIcon
            :name="isSidebarCollapsed ? 'i-heroicons-chevron-right' : 'i-heroicons-chevron-left'"
            class="w-5 h-5"
          />
          <span
            v-if="!isSidebarCollapsed"
            class="ml-3"
          >
            Collapse
          </span>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
const {
  isSidebarCollapsed,
  isMobile,
  navigationItems,
  toggleSidebar,
  closeMobileMenu
} = useLayout()

const route = useRoute()

const isActiveRoute = (path: string) => {
  return route.path === path
}

const handleNavClick = () => {
  if (isMobile.value) {
    closeMobileMenu()
  }
}
</script>
