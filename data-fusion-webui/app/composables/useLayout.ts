import type { Ref } from 'vue'

export interface NavItem {
  label: string
  icon: string
  path: string
  children?: NavItem[]
}

export const useLayout = () => {
  // State
  const isSidebarCollapsed: Ref<boolean> = ref(false)
  const isMobile: Ref<boolean> = ref(false)
  const isMobileMenuOpen: Ref<boolean> = ref(false)

  // Actions
  const toggleSidebar = () => {
    isSidebarCollapsed.value = !isSidebarCollapsed.value
  }

  const toggleMobileMenu = () => {
    isMobileMenuOpen.value = !isMobileMenuOpen.value
  }

  const closeMobileMenu = () => {
    isMobileMenuOpen.value = false
  }

  // Initialize responsive behavior
  const initResponsive = () => {
    const checkMobile = () => {
      isMobile.value = window.innerWidth < 768
      if (!isMobile.value) {
        isMobileMenuOpen.value = false
      }
    }

    checkMobile()
    window.addEventListener('resize', checkMobile)

    onUnmounted(() => {
      window.removeEventListener('resize', checkMobile)
    })
  }

  // Navigation items
  const navigationItems: NavItem[] = [
    {
      label: 'Dashboard',
      icon: 'i-heroicons-home',
      path: '/'
    },
    {
      label: 'Data Sources',
      icon: 'i-heroicons-circle-stack',
      path: '/sources'
    },
    {
      label: 'Fusion Pipelines',
      icon: 'i-heroicons-arrow-path',
      path: '/fusion'
    },
    {
      label: 'Analytics',
      icon: 'i-heroicons-chart-bar',
      path: '/analytics'
    },
    {
      label: 'Settings',
      icon: 'i-heroicons-cog-6-tooth',
      path: '/settings'
    }
  ]

  return {
    // State
    isSidebarCollapsed: readonly(isSidebarCollapsed),
    isMobile: readonly(isMobile),
    isMobileMenuOpen: readonly(isMobileMenuOpen),
    
    // Actions
    toggleSidebar,
    toggleMobileMenu,
    closeMobileMenu,
    initResponsive,
    
    // Data
    navigationItems
  }
}
