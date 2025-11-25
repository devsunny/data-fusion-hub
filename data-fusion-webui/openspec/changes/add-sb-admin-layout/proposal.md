# Change: Add SB Admin Dashboard Layout

## Why
The project currently has only a basic Nuxt welcome page. We need a professional admin dashboard layout to provide a solid foundation for the data fusion web UI. SB Admin is a proven, responsive dashboard template that provides common admin interface patterns including navigation, content areas, and responsive behavior.

## What Changes
- **ADD** responsive dashboard layout with top navigation bar
- **ADD** collapsible sidebar navigation with menu items
- **ADD** main content area with proper spacing and containers
- **ADD** footer component
- **ADD** common dashboard UI components (stats cards, content cards)
- **ADD** responsive breakpoints for mobile, tablet, and desktop views
- **ADD** layout state management for sidebar collapse/expand

## Impact
- **Affected specs:** layout, navigation, ui-components
- **Affected code:** New layout components, pages, composables
- **New dependencies:** None (uses existing @nuxt/ui and Tailwind CSS)
- **Breaking changes:** None - this is additive
