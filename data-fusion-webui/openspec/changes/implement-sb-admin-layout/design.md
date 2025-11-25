# Design: SB Admin Dashboard Layout with Night Mode Toggle

## Overview
This design adapts SB Admin dashboard patterns to our Nuxt 4 + Tailwind CSS stack, implementing a responsive admin interface with light/dark theme switching.

## Design Decisions

### 1. Layout Structure
**SB Admin Pattern Adaptation**
- Sidebar navigation (collapsible on desktop, slide-out on mobile)
- Top navigation bar with user controls and theme toggle
- Main content area with proper spacing
- Footer (optional, minimal)

**Responsive Breakpoints**
- Desktop: Sidebar always visible (240px width)
- Tablet: Collapsible sidebar (768px breakpoint)
- Mobile: Hidden sidebar, slide-out menu (triggered by hamburger)

**Component Hierarchy**
```
layouts/default.vue (root layout)
├── layout/TopNav.vue (top navigation bar)
│   ├── Logo/brand
│   ├── Navigation items (mobile)
│   ├── ThemeToggle
│   └── User menu (placeholder)
├── layout/Sidebar.vue (side navigation)
│   ├── Navigation sections
│   ├── Collapse/expand button
│   └── User info (optional)
├── layout/Footer.vue (optional footer)
└── <slot /> (main content from pages)
```

### 2. Theming System
**Technology Choice: @nuxtjs/color-mode**
- Nuxt-native solution for theme switching
- Built-in localStorage persistence
- SSR-safe (no hydration mismatch)
- System preference detection
- Smooth transitions between themes

**Theme Implementation Strategy**
- CSS custom properties for color tokens
- Tailwind dark: prefix for dark mode variants
- Class-based dark mode (not media query) for explicit control
- Color tokens defined in app.config.ts or tailwind.config.ts

**Color Token Structure**
```typescript
// Light theme
--color-background: 255 255 255
--color-foreground: 17 24 39
--color-primary: 59 130 246
--color-sidebar: 243 244 246
--color-border: 229 231 235

// Dark theme
--color-background: 17 24 39
--color-foreground: 243 244 246
--color-primary: 96 165 250
--color-sidebar: 31 41 55
--color-border: 55 65 81
```

### 3. Component Architecture

**ThemeToggle Component**
- Sun icon for light mode
- Moon icon for dark mode
- Animated transition between states
- Accessible button with aria-label
- Keyboard navigable (Enter/Space to toggle)

**TopNav Component**
- Sticky positioning
- Hamburger menu for mobile
- ThemeToggle integration
- User menu dropdown (placeholder)
- Responsive height (64px desktop, 56px mobile)

**Sidebar Component**
- Fixed positioning on desktop
- Collapsible state (persisted in localStorage)
- Navigation sections with icons
- Active state highlighting
- Smooth collapse/expand animation

### 4. State Management

**Theme State**
- Managed by @nuxtjs/color-mode
- localStorage key: `color-mode`
- Values: `light`, `dark`, `system`
- Initial load: Check localStorage → Check system preference → Default to light

**Sidebar State**
- Collapsed state persisted in localStorage
- Key: `sidebar-collapsed`
- Reactive state using useState() composable

### 5. Styling Approach

**Tailwind Configuration**
```javascript
// tailwind.config.ts
darkMode: 'class', // Enable class-based dark mode
```

**Transition Strategy**
- Theme transitions: 200-300ms ease-in-out
- Sidebar animations: 300ms ease-out
- Mobile menu: 250ms ease-out with transform
- All transitions use CSS transitions (not JS) for performance

### 6. Accessibility Considerations

**Keyboard Navigation**
- Tab order: TopNav → Sidebar → Main content
- Skip link to main content
- Arrow key navigation in sidebar
- Escape key closes mobile menu

**Screen Readers**
- Proper ARIA labels for all interactive elements
- Live region announcements for theme changes
- Semantic HTML structure
- Heading hierarchy (h1 in main content, h2 for sections)

**Color Contrast**
- WCAG 2.1 AA compliance for both themes
- Minimum 4.5:1 contrast ratio for normal text
- Minimum 3:1 contrast ratio for large text
- Focus indicators with sufficient contrast

### 7. Performance Considerations

**Initial Load**
- No layout shift on theme initialization
- Critical CSS inlined if necessary
- Sidebar state applied before first paint

**Runtime Performance**
- CSS transitions for animations (GPU accelerated)
- Debounced resize handlers
- Lazy-loaded navigation icons (if many)

### 8. Hydration Safety

**SSR/SSG Compatibility**
- @nuxtjs/color-mode handles SSR-safe theme detection
- No window/localStorage access during SSR
- Consistent initial render between server and client
- Theme applied after mount to prevent flash

### 9. Integration Points

**Backend Integration**
- Theme preference could be synced to user profile (future)
- Sidebar navigation items loaded from backend API (future)
- User menu populated from backend (future)

**Future Extensibility**
- Plugin system for additional themes
- Customizable color schemes
- User-defined sidebar items
- Role-based navigation visibility

## Trade-offs

**SB Admin vs Tailwind**
- Not using Bootstrap (SB Admin's native framework)
- Recreating visual patterns with Tailwind utilities
- Maintaining similar look/feel but with modern CSS

**Component Complexity**
- Splitting into multiple components for maintainability
- Potential performance cost of multiple components vs single large component
- Chosen approach prioritizes maintainability and reusability

**State Persistence**
- localStorage for theme and sidebar state
- No server-side persistence (user preference lost on different devices)
- Acceptable for initial implementation, can add backend sync later
