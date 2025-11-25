# Project Specification

## Overview

**Project Name:** Data Fusion WebUI  
**Framework:** Nuxt 3 (Vue 3)  
**Language:** TypeScript  
**Package Manager:** npm  
**Purpose:** A modern web application for data fusion and visualization

**Current Status:** 🟡 Initial Setup - Basic Nuxt 3 scaffold with minimal code

## Tech Stack

### Core Framework
- **Nuxt 3.20.1** - Full-stack Vue.js framework with SSR/SSG capabilities
- **Vue 3.5.25** - Progressive JavaScript framework with Composition API
- **TypeScript 5.9.3** - Type-safe JavaScript development
- **Vue Router 4.6.3** - Client-side routing (integrated with Nuxt)
- **Nitro** - High-performance server engine (built into Nuxt)

### UI & Styling
- **@nuxt/ui 4.2.1** - Official Nuxt UI component library with Tailwind CSS
- **@nuxt/image 2.0.0** - Image optimization and responsive images
- **@unhead/vue 2.0.19** - Document head manager for meta tags and SEO
- **Tailwind CSS** - Utility-first CSS framework (via @nuxt/ui)

### Development & Quality
- **ESLint 9.39.1** - Code linting with Nuxt-specific rules (@nuxt/eslint 1.10.0)
- **@nuxt/hints 1.0.0-alpha.2** - Development hints and best practices
- **TypeScript** - Static type checking and IDE support
- **Vue DevTools** - Browser devtools integration (enabled in nuxt.config)

### Testing & Utilities
- **@nuxt/test-utils 3.20.1** - Testing utilities for Nuxt applications
- **@nuxt/scripts 0.13.0** - Script management and optimization
- **Vitest** - Testing framework (available via Nuxt)

## Architecture

### Current Directory Structure
```
data-fusion-webui/
├── app/                    # Vue application code (MINIMAL - only app.vue exists)
│   ├── app.vue            # Root Vue component (basic template with NuxtWelcome)
│   ├── components/        # Reusable Vue components (EMPTY - needs to be created)
│   ├── pages/             # File-system based routing (EMPTY - needs to be created)
│   ├── layouts/           # Page layouts (EMPTY - needs to be created)
│   ├── composables/       # Vue Composition API functions (EMPTY - needs to be created)
│   ├── assets/            # Static assets (EMPTY - needs to be created)
│   └── utils/             # Client-side utilities (EMPTY - needs to be created)
├── server/                # Nitro server API (MINIMAL - only tsconfig.json exists)
│   ├── api/               # API endpoints (EMPTY - needs to be created)
│   ├── middleware/        # Server middleware (EMPTY - needs to be created)
│   ├── utils/             # Server utilities (EMPTY - needs to be created)
│   └── types/             # Server-side TypeScript types (EMPTY - needs to be created)
├── public/                # Static files served at root (EMPTY)
├── nuxt.config.ts         # Nuxt configuration (minimal setup)
├── package.json           # Dependencies and scripts
├── tsconfig.json          # TypeScript configuration
└── openspec/              # OpenSpec documentation
    ├── project.md         # This file
    ├── AGENTS.md          # OpenSpec instructions
    ├── specs/             # Capability specifications (EMPTY)
    └── changes/           # Change proposals (EMPTY except for archive)
```

### Key Features Available
- **Server-Side Rendering (SSR)** - Improved SEO and initial load performance
- **File-system Routing** - Automatic route generation from pages directory
- **API Routes** - Server-side endpoints using Nitro server
- **Auto-imports** - Components and composables automatically imported
- **Hot Module Replacement (HMR)** - Fast development with instant updates
- **TypeScript** - Full type safety throughout the stack
- **Nuxt DevTools** - Enhanced development experience

### Planned Architecture for Data Fusion
```
app/
├── components/
│   ├── data/                # Data display components
│   │   ├── DataTable.vue
│   │   ├── DataChart.vue
│   │   └── DataCard.vue
│   ├── fusion/              # Fusion-specific components
│   │   ├── FusionPipeline.vue
│   │   ├── SourceSelector.vue
│   │   └── ResultViewer.vue
│   └── common/              # Shared components
│       ├── Header.vue
│       ├── Sidebar.vue
│       └── LoadingSpinner.vue
├── pages/
│   ├── index.vue            # Dashboard/home page
│   ├── sources/             # Data source management
│   │   ├── index.vue
│   │   └── [id].vue
│   ├── fusion/              # Fusion pipelines
│   │   ├── index.vue
│   │   ├── create.vue
│   │   └── [id].vue
│   └── settings/            # Application settings
│       └── index.vue
├── composables/
│   ├── useDataSources.ts    # Data source management
│   ├── useFusionPipelines.ts # Fusion pipeline logic
│   └── useWebSocket.ts      # Real-time updates
├── utils/
│   ├── formatters.ts        # Data formatting utilities
│   └── validators.ts        # Input validation
└── types/
    ├── data.ts              # Data type definitions
    └── fusion.ts            # Fusion-specific types

server/
├── api/
│   ├── sources/             # Data source endpoints
│   │   ├── index.get.ts
│   │   └── index.post.ts
│   ├── fusion/              # Fusion pipeline endpoints
│   │   ├── index.get.ts
│   │   ├── index.post.ts
│   │   └── [id].get.ts
│   └── ws/                  # WebSocket endpoints
│       └── index.ts
├── utils/
│   ├── dataFusion.ts        # Fusion algorithms
│   └── dataValidation.ts    # Data validation logic
└── types/
    └── api.ts               # API type definitions
```

## Development Conventions

### Code Style & Standards
- **TypeScript** - All code must be written in TypeScript (strict mode)
- **ESLint** - Follow configured ESLint rules (@nuxt/eslint)
- **Vue 3 Composition API** - Use Composition API exclusively (no Options API)
- **Script Setup** - Always use `<script setup lang="ts">` for Vue components
- **Type Imports** - Use `import type` for TypeScript types
- **File Naming** - Use kebab-case for files (except Vue components)

### Component Structure
```vue
<template>
  <div class="component-name">
    <!-- Use Nuxt UI components -->
    <UButton 
      :label="buttonText"
      @click="handleClick"
    />
  </div>
</template>

<script setup lang="ts">
// Type imports first
import type { ButtonProps } from '@nuxt/ui'

// Vue imports
import { ref, computed } from 'vue'

// Composable imports
import { useDataSources } from '~/composables/useDataSources'

// Props interface
interface Props {
  buttonText: string
  disabled?: boolean
}

// Props definition
const props = withDefaults(defineProps<Props>(), {
  disabled: false
})

// Emits definition
const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

// Composables
const { sources, loading } = useDataSources()

// State
const count = ref(0)

// Computed
const isActive = computed(() => count.value > 0)

// Methods
const handleClick = (event: MouseEvent) => {
  emit('click', event)
  count.value++
}

// Lifecycle
onMounted(() => {
  console.log('Component mounted')
})
</script>

<style scoped>
/* Use Tailwind CSS classes primarily */
.component-name {
  @apply p-4 m-2;
}
</style>
```

### Composables Pattern
```typescript
// composables/useDataSources.ts
import type { DataSource } from '~/types/data'

export const useDataSources = () => {
  // State
  const sources = ref<DataSource[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Actions
  const fetchSources = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await $fetch<DataSource[]>('/api/sources')
      sources.value = response
    } catch (err) {
      error.value = 'Failed to fetch data sources'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  const addSource = async (source: Omit<DataSource, 'id'>) => {
    // Implementation
  }

  // Lifecycle
  onMounted(() => {
    fetchSources()
  })

  // Return
  return {
    sources: readonly(sources),
    loading: readonly(loading),
    error: readonly(error),
    fetchSources,
    addSource
  }
}
```

### API Route Pattern
```typescript
// server/api/sources/index.get.ts
import type { DataSource } from '~/server/types/api'

export default defineEventHandler(async (event): Promise<DataSource[]> => {
  try {
    // Verify authentication if needed
    // await requireAuth(event)
    
    // Fetch data from database or external API
    const sources = await fetchDataSources()
    
    return sources
  } catch (error) {
    throw createError({
      statusCode: 500,
      statusMessage: 'Failed to fetch data sources',
      cause: error
    })
  }
})
```

### Naming Conventions
- **Vue Components:** PascalCase with .vue extension (e.g., `DataTable.vue`)
- **Composables:** camelCase with 'use' prefix (e.g., `useDataFusion.ts`)
- **Pages:** kebab-case with .vue extension (e.g., `data-sources.vue`)
- **API Routes:** kebab-case with method suffix (e.g., `sources.get.ts`, `create.post.ts`)
- **Types/Interfaces:** PascalCase (e.g., `FusionData.ts`, `DataSource.interface.ts`)
- **Regular TS/JS Files:** kebab-case (e.g., `data-formatters.ts`)
- **Constants:** UPPER_SNAKE_CASE (e.g., `API_BASE_URL`)

### Git Workflow
- **Main Branch:** `main` (protected)
- **Feature Branches:** `feature/description` or `issue-123-description`
- **OpenSpec Changes:** `openspec/[change-id]`
- **Pull Requests:** Required for all merges to main
- **Commit Messages:** Follow conventional commits format
  - `feat: add data source selector component`
  - `fix: resolve websocket connection issue`
  - `docs: update API documentation`
  - `refactor: simplify fusion pipeline logic`

### TypeScript Configuration
- **Strict Mode:** Enabled
- **No Implicit Any:** Enabled
- **Strict Null Checks:** Enabled
- **ES Module Interop:** Enabled
- **Target:** ESNext
- **Module Resolution:** Bundler

## Key Dependencies

### Production Dependencies
- `nuxt` ^3.20.1 - Core framework
- `vue` ^3.5.25 - Vue.js
- `vue-router` ^4.6.3 - Routing
- `@nuxt/ui` ^4.2.1 - UI components (Tailwind CSS based)
- `@nuxt/image` ^2.0.0 - Image optimization
- `@unhead/vue` ^2.0.19 - Head management
- `typescript` ^5.9.3 - TypeScript language

### Development Dependencies
- `@nuxt/eslint` ^1.10.0 - ESLint integration
- `@nuxt/hints` ^1.0.0-alpha.2 - Development hints
- `@nuxt/scripts` ^0.13.0 - Script management
- `@nuxt/test-utils` ^3.20.1 - Testing utilities
- `eslint` ^9.39.1 - Linting

## Available Scripts

```bash
# Development
npm run dev          # Start development server on http://localhost:3000
npm run postinstall  # Prepare Nuxt (runs automatically after npm install)

# Production
npm run build        # Build for production
npm run preview      # Preview production build locally
npm run generate     # Generate static site (SSG)
```

## Configuration Files

### nuxt.config.ts
```typescript
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: [
    '@nuxt/eslint',
    '@nuxt/hints',
    '@nuxt/image',
    '@nuxt/scripts',
    '@nuxt/test-utils',
    '@nuxt/ui'
  ]
})
```

### tsconfig.json
- Extends Nuxt's TypeScript configuration
- Includes server and app directories
- Strict mode enabled

## Environment Variables

Create `.env` file for local development:
```bash
# API Configuration
NUXT_PUBLIC_API_BASE=http://localhost:3000/api

# Feature Flags
NUXT_PUBLIC_ENABLE_ANALYTICS=false
NUXT_PUBLIC_ENABLE_WEBSOCKETS=true

# External Services (when needed)
# NUXT_PUBLIC_DATA_SERVICE_URL=https://api.example.com
```

## Development Setup

### Prerequisites
- Node.js 18+ or 20+
- npm 9+

### Initial Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Open browser to http://localhost:3000
```

### Adding New Features
1. Check `openspec/specs/` for existing capabilities
2. Create change proposal in `openspec/changes/[change-id]/`
3. Follow OpenSpec workflow (see openspec/AGENTS.md)
4. Implement using established conventions
5. Test thoroughly before merging

## Future Considerations

### Planned Features
- **Data Source Management** - Connect to various data sources (APIs, databases, files)
- **Data Fusion Engine** - Merge and transform data from multiple sources
- **Real-time Updates** - WebSocket integration for live data
- **Data Visualization** - Charts, graphs, and interactive dashboards
- **Export/Import** - Data export in various formats (CSV, JSON, Excel)
- **User Authentication** - Secure access to data and features
- **Pipeline Builder** - Visual interface for creating fusion pipelines
- **Scheduling** - Automated data fusion jobs

### Performance Goals
- **Initial Load:** < 3 seconds
- **Time to Interactive:** < 5 seconds
- **API Response:** < 200ms for simple queries
- **Bundle Size:** < 500KB initial JS
- **Core Web Vitals:** All in "Good" range

### Scaling Considerations
- Support for large datasets (100k+ rows)
- Efficient WebSocket connections for real-time updates
- Caching strategies for frequently accessed data
- Progressive loading for large result sets

## Deployment

### Supported Platforms
- **Node.js Servers:** Traditional SSR deployment
- **Static Hosting:** SSG for static sites (Netlify, Vercel, etc.)
- **Serverless:** Edge functions and serverless platforms
- **Containers:** Docker deployment ready

### Environment-Specific Configurations
```bash
# Production
NODE_ENV=production
NUXT_PUBLIC_API_BASE=https://api.production.com

# Staging
NODE_ENV=production
NUXT_PUBLIC_API_BASE=https://api.staging.com

# Development
NODE_ENV=development
NUXT_PUBLIC_API_BASE=http://localhost:3000/api
```

## Testing Strategy

### Unit Tests
- Test composables and utilities in isolation
- Use Vitest for fast execution
- Mock external dependencies

### Component Tests
- Test Vue components with @nuxt/test-utils
- Test user interactions and props
- Verify event emissions

### Integration Tests
- Test API endpoints
- Test full user flows
- Use test database when needed

### E2E Tests
- Test critical user journeys
- Use Playwright or Cypress
- Run against staging environment

## Documentation Standards

### Code Documentation
- Use JSDoc comments for complex functions
- Document component props and emits
- Include usage examples in component comments

### API Documentation
- Document all API endpoints
- Include request/response examples
- Document error cases

### OpenSpec Documentation
- Follow OpenSpec conventions strictly
- Keep specs focused and testable
- Include clear scenarios for each requirement

## Security Considerations

### API Security
- Validate all input data
- Implement authentication/authorization
- Use rate limiting
- Sanitize user inputs

### Data Protection
- Encrypt sensitive data
- Use HTTPS in production
- Implement proper CORS policies
- Secure WebSocket connections

### Frontend Security
- Prevent XSS attacks
- Sanitize user-generated content
- Use Content Security Policy
- Validate file uploads
