# Bulk Data Object Registration

## Summary

This change introduces a new bulk registration endpoint for data objects that allows clients to register multiple data objects in a single request. Each data object must include associated data fields, enabling the creation of complete data object hierarchies with their field definitions.

## Why

Clients often need to register multiple related data objects and their fields simultaneously. Currently, they must make separate API calls for each object, which is inefficient and can lead to inconsistent states if some operations succeed while others fail. A bulk registration endpoint will improve performance, reduce network overhead, and ensure atomicity of related object creation.

## What Changes

- Add new POST `/data-objects/bulk` endpoint
- Implement bulk data object and field creation logic  
- Support nested data fields within data objects in bulk requests
- Make `data_fields` required for each data object in bulk operations
- Maintain existing individual data object endpoints for backward compatibility
- Ensure all objects in a bulk request belong to the same domain

## Change ID
bulk_data_object_registration

## Status
Implemented

## Related Work
- Existing data object and data field models
- Data object and data field API endpoints