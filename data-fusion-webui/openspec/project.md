# Project Context

## Purpose
Data Fusion WebUI is a modern web application built with Nuxt 4 that provides an intuitive interface for data integration, transformation, and fusion operations. The project aims to create a user-friendly web interface for managing data pipelines, visualizing data flows, and orchestrating data fusion processes.

## Tech Stack

### Core Framework
- **Nuxt 4** (^4.2.1) - Vue 3 meta-framework for full-stack web development
- **Vue 3** (^3.5.25) - Progressive JavaScript framework for building UI
- **Vue Router** (^4.6.3) - Official router for Vue.js
- **TypeScript** (^5.9.3) - Typed superset of JavaScript

### UI & Styling
- **@nuxt/ui** (^4.2.1) - UI component library for Nuxt
- **@nuxt/image** (^2.0.0) - Image optimization and handling

### Code Quality & Testing
- **ESLint** (^9.39.1) - Pluggable JavaScript linter
- **@nuxt/eslint** (^1.10.0) - Nuxt-specific ESLint configuration
- **@nuxt/test-utils** (^3.20.1) - Testing utilities for Nuxt applications
- **@nuxt/hints** (^1.0.0-alpha.2) - Development hints and best practices

### Development Tools
- **Nuxt DevTools** - Enabled for development debugging and inspection
- **TypeScript Configuration** - Project references for client/server/shared types

## Project Conventions

### Code Style
- **TypeScript First**: All new code should be written in TypeScript with proper type definitions
- **Vue 3 Composition API**: Prefer Composition API over Options API for new components
- **File Naming**: Use kebab-case for files (e.g., `data-processor.ts`, `user-card.vue`)
- **Component Naming**: PascalCase for Vue components, kebab-case in templates
- **Indentation**: 2 spaces for all files
- **Semicolons**: Required
- **Quotes**: Single quotes for strings

### Architecture Patterns

#### Directory Structure
```
app/                      # Nuxt 4 app directory
├── components/           # Vue components (auto-imported)
├── composables/          # Vue composables (auto-imported)
├── layouts/              # Layout components
├── pages/                # Page components (file-based routing)
├── plugins/              # Nuxt plugins
├── server/               # Server-side code (API proxy, auth middleware)
│   ├── api/              # API proxy endpoints for backend service
│   ├── middleware/       # Server middleware (auth, logging)
│   └── utils/            # Server utilities
├── utils/                # Client-side utilities
└── app.vue               # Root component
```

#### Component Architecture
- **Single Responsibility**: Each component should have one clear purpose
- **Props/Emits**: Explicitly define props and emits with TypeScript interfaces
- **Composables**: Extract reusable logic into composables in `app/composables/`
- **Store Management**: Use Pinia (to be added) for state management

#### API Integration Pattern
- **Backend Service**: RESTful API at `http://localhost:8000` (production URL TBD)
- **OpenAPI Documentation**: Available at `http://localhost:8000/openapi.json`
- **API Client**: Generate TypeScript client from OpenAPI spec for type-safe API calls
- **Proxy Pattern**: Use Nuxt server API routes to proxy requests to backend service
- **Authentication**: JWT-based auth with token storage and refresh logic
- **Error Handling**: Consistent error handling with appropriate HTTP status codes

### Testing Strategy
- **Unit Tests**: Test composables and utility functions
- **Component Tests**: Test Vue components in isolation
- **E2E Tests**: Test critical user flows (to be implemented)
- **Type Testing**: Leverage TypeScript for compile-time type checking
- **API Mocking**: Mock backend API responses for frontend testing

### Git Workflow
- **Main Branch**: `main` (protected)
- **Feature Branches**: `feature/description` or `issue-123-description`
- **Commit Convention**: Conventional Commits (feat:, fix:, docs:, style:, refactor:, test:, chore:)
- **Pull Requests**: Required for all changes to main branch
- **Code Review**: All PRs require at least one review

## Domain Context

### Data Fusion Concepts
- **Data Sources**: Various input sources (databases, APIs, files)
- **Transformations**: Data cleaning, mapping, and transformation operations
- **Fusion Rules**: Logic for combining data from multiple sources
- **Pipelines**: Sequences of operations for data processing
- **Schedules**: Time-based or event-based pipeline execution

### User Roles
- **Data Engineers**: Create and manage data pipelines
- **Data Analysts**: Monitor data quality and pipeline performance
- **Administrators**: Manage users, permissions, and system configuration

## Important Constraints

### Technical Constraints
- **Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
- **Performance**: Initial page load should be under 3 seconds on 3G
- **Accessibility**: WCAG 2.1 AA compliance
- **Security**: All API endpoints must implement proper authentication/authorization
- **Backend Dependency**: Frontend requires backend service to be running on localhost:8000 during development

### Development Constraints
- **Type Safety**: No `any` types without explicit justification
- **Documentation**: All public functions and components must have JSDoc comments
- **Dependencies**: Minimize external dependencies, prefer Nuxt/Vue ecosystem
- **API Contract**: Frontend must stay in sync with backend OpenAPI specification

## External Dependencies

### Backend Service
- **RESTful API**: Backend service providing data fusion operations
- **OpenAPI/Swagger**: API documentation available at `/openapi.json`
- **Base URL**: `http://localhost:8000` (development), production URL TBD
- **Authentication**: JWT token-based authentication
- **Technology**: Python-based backend (FastAPI/Flask/Django - TBD)

### Development Infrastructure
- **Package Management**: npm
- **Version Control**: GitHub
- **CI/CD**: GitHub Actions
- **Hosting**: TBD (likely Vercel, Netlify, or AWS for frontend)
- **Backend Hosting**: TBD (separate from frontend hosting)

## Development Commands

```bash
# Install dependencies
npm install

# Development server (frontend only)
npm run dev

# Development with backend (run in separate terminal)
# Backend must be running on http://localhost:8000

# Build for production
npm run build

# Preview production build
npm run preview

# Generate static site
npm run generate
```

## Backend Integration

### Local Development Setup
1. Start backend service on `http://localhost:8000`
2. Verify OpenAPI documentation at `http://localhost:8000/openapi.json`
3. Start frontend development server with `npm run dev`
4. Frontend will proxy API requests to backend service

### API Client Generation
- Generate TypeScript client from OpenAPI spec for type-safe API integration
- Store generated client in `app/lib/api-client/` or similar location
- Regenerate client when backend OpenAPI spec changes

### Environment Configuration
- Development: `http://localhost:8000`
- Staging: TBD
- Production: TBD

## Future Considerations

### Planned Features
- Real-time data pipeline monitoring
- Visual workflow builder
- Data quality metrics dashboard
- Role-based access control
- Audit logging
- Export/import pipeline configurations

### Scalability
- Modular architecture to support plugin system
- Microservices-ready design for backend separation
- Support for horizontal scaling of data processing
- CDN integration for static assets
