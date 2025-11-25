<template>
  <nav class="bg-white border-b border-gray-200 fixed z-50 w-full top-0">
    <div class="px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Left side: Logo and mobile menu button -->
        <div class="flex items-center">
          <!-- Mobile menu button -->
          <button
            v-if="isMobile"
            @click="toggleMobileMenu"
            class="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
          >
            <span class="sr-only">Open sidebar</span>
            <UIcon name="i-heroicons-bars-3" class="w-6 h-6" />
          </button>

          <!-- Logo/Brand -->
          <div class="flex items-center ml-4 md:ml-0">
            <h1 class="text-xl font-semibold text-gray-900">
              Data Fusion Hub
            </h1>
          </div>
        </div>

        <!-- Right side: User menu -->
        <div class="flex items-center space-x-4">
          <!-- Notifications -->
          <button class="p-2 rounded-full text-gray-600 hover:text-gray-900 hover:bg-gray-100">
            <UIcon name="i-heroicons-bell" class="w-5 h-5" />
          </button>

          <!-- User menu -->
          <UDropdown
            :items="userMenuItems"
            :popper="{ placement: 'bottom-end' }"
          >
            <UButton
              color="white"
              variant="ghost"
              class="flex items-center space-x-2"
            >
              <UAvatar
                src="https://ui-avatars.com/api/?name=Admin+User"
                alt="User Avatar"
                size="sm"
              />
              <span class="hidden md:inline text-sm font-medium text-gray-700">
                Admin User
              </span>
              <UIcon name="i-heroicons-chevron-down" class="w-4 h-4" />
            </UButton>
          </UDropdown>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
const { isMobile, toggleMobileMenu } = useLayout()

const userMenuItems = [
  [{
    label: 'Profile',
    icon: 'i-heroicons-user',
    to: '/profile'
  }, {
    label: 'Settings',
    icon: 'i-heroicons-cog-6-tooth',
    to: '/settings'
  }],
  [{
    label: 'Sign out',
    icon: 'i-heroicons-arrow-right-on-rectangle',
    to: '/logout'
  }]
]
</script>
