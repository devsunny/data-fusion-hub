## ADDED Requirements

### Requirement: Top Navigation Bar
The system SHALL provide a top navigation bar component that appears at the top of every page and includes branding, user menu, and navigation controls.

#### Scenario: Top navigation renders with branding
- **GIVEN** the application is loaded
- **WHEN** any page is rendered
- **THEN** the top navigation bar displays the application logo/name
- **AND** the navigation controls are accessible

#### Scenario: Mobile toggle button visibility
- **GIVEN** the viewport width is less than 768px
- **WHEN** the page is rendered
- **THEN** a sidebar toggle button is visible in the top navigation
- **AND** clicking it shows/hides the sidebar

### Requirement: Sidebar Navigation Menu
The system SHALL provide a sidebar navigation component with menu items that link to different sections of the application.

#### Scenario: Sidebar renders navigation items
- **GIVEN** the sidebar is visible
- **WHEN** the page is rendered
- **THEN** navigation menu items are displayed with icons and labels
- **AND** each item links to a valid route

#### Scenario: Active route highlighting
- **GIVEN** the user is on a specific page
- **WHEN** the sidebar is rendered
- **THEN** the corresponding navigation item is visually highlighted
- **AND** the highlight updates when navigating to a different page

#### Scenario: Navigation item click behavior
- **GIVEN** a navigation item is clickable
- **WHEN** the user clicks on it
- **THEN** the application navigates to the corresponding page
- **AND** on mobile, the sidebar closes after navigation

### Requirement: Navigation Menu Structure
The system SHALL provide a configurable navigation menu structure with support for nested items and icons.

#### Scenario: Navigation items have icons
- **GIVEN** navigation items are defined
- **WHEN** the sidebar renders
- **THEN** each item displays an appropriate icon
- **AND** icons are consistent with the item's purpose

#### Scenario: Navigation items have labels
- **GIVEN** navigation items are defined
- **WHEN** the sidebar renders
- **THEN** each item displays a clear, descriptive label
- **AND** labels are readable and properly aligned with icons

#### Scenario: Navigation supports hierarchy
- **GIVEN** some navigation items have children
- **WHEN** the sidebar renders
- **THEN** parent items show expand/collapse controls
- **AND** child items are indented to show hierarchy
