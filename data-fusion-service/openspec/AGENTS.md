# Data Fusion Hub Service - OpenSpec Agents

## Overview

This document defines the roles and responsibilities for managing the Data Fusion Hub Service project using the OpenSpec framework. It outlines how changes are proposed, reviewed, implemented, and documented.

## Agent Roles

### Project Maintainer
- Responsible for overall project direction and architecture decisions
- Reviews and approves all major changes to the specification  
- Ensures code quality standards are maintained
- Manages release cycles and versioning strategy

### Technical Lead
- Leads implementation of new features and specifications
- Coordinates between different development teams
- Reviews pull requests and code changes
- Maintains technical documentation and API specifications

### Documentation Specialist
- Responsible for maintaining all project documentation including:
  - Project specification (`openspec/project.md`)
  - Change proposals and their implementations  
  - API documentation and usage examples
- Ensures consistency in technical writing across the project

## Change Proposal Process

All significant changes to the project must follow this process:

1. **Proposal Creation**: Create a new proposal file in `openspec/changes/` with timestamped naming convention (`YYYYMMDD-HHMMSS-description.md`)
2. **Specification Review**: All stakeholders review the proposed change
3. **Implementation**: Developer implements the change following established conventions  
4. **Testing**: Comprehensive testing including unit, integration and API tests
5. **Documentation Update**: Update relevant documentation files
6. **Approval**: Project maintainer approves the implementation
7. **Versioning**: Apply version tag to indicate completion

## Change Proposal Format

Each proposal should include:

### Title
Clear description of what is being changed

### Summary  
Brief overview of the change and its purpose

### Change Details
Detailed technical specification of what will be implemented

### Impact Assessment
- What existing functionality this affects (if any)
- New capabilities introduced
- Breaking changes (if applicable)

### Implementation Plan
- Files to be modified/created
- Dependencies that need to be added  
- Testing approach

## Versioning Strategy

The project uses timestamp-based versioning for OpenSpec changes:

```
YYYYMMDD-HHMMSS-description.md
```

Examples:
- `20251122-144846-design.md` - Design specification from 2025-11-22 at 14:48:46
- `20251122-150102-proposal.md` - Proposal document from 2025-11-22 at 15:01:02

## Documentation Standards

### Project Specification (`openspec/project.md`)
This file should contain:
- Overview and purpose of the project
- Tech stack and architecture patterns  
- Project structure and conventions
- Implementation status tracking
- Development environment setup instructions

### Change Proposals 
Each change proposal in `openspec/changes/` should follow this format:
1. Title with timestamp prefix
2. Summary section explaining what's being changed
3. Detailed technical specification  
4. Impact assessment
5. Implementation plan and testing approach

## Review Process

All changes must go through the following review stages:

### Initial Review (by Technical Lead)
- Technical feasibility check
- Code quality standards verification
- Integration with existing architecture  

### Final Approval (by Project Maintainer) 
- Strategic alignment check  
- Impact assessment approval
- Documentation completeness verification

## Communication Channels

### GitHub Issues
All changes should be tracked through GitHub issues:
- Create issue for each major change or feature
- Use labels to categorize by type (bug, enhancement, documentation)
- Link pull requests to relevant issues  

### Pull Requests
When submitting code changes:
1. Reference the related issue(s) in PR description  
2. Include comprehensive testing information
3. Update documentation as needed
4. Ensure all tests pass before merging

## Best Practices

### Code Quality
- Follow PEP 8 style guidelines
- Write clear, descriptive commit messages
- Maintain consistent code formatting across project
- Use type hints throughout the codebase  

### Documentation Consistency  
- Keep documentation in sync with implementation
- Update both API documentation and internal specs
- Use consistent terminology throughout all documents
- Include usage examples where appropriate

### Testing Coverage
- All new features must include unit tests
- Integration tests for complex workflows
- End-to-end testing for critical user flows
- Regular test suite execution as part of CI/CD pipeline

## Emergency Procedures

In case of urgent fixes or security patches:
1. Create emergency issue with high priority label  
2. Bypass normal review process but ensure minimal impact analysis
3. Document the emergency change in project specification
4. Schedule follow-up review for full documentation update

This framework ensures consistent, well-documented development practices across all aspects of the Data Fusion Hub Service project.