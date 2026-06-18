# Field Governance Checklist | 字段治理检查清单

## Before adding a field to any page

- [ ] Database: column exists in schema, type verified (DESCRIBE table)
- [ ] Metadata: field registered in central metadata registry with label, type, validation
- [ ] Configuration: default visibility, ordering, required state defined
- [ ] Consumers: all pages referencing this entity identified

## Before modifying a field

- [ ] Database: column type matches metadata claims
- [ ] All consumers: trace every page/component using this field
- [ ] No page-local overrides will break (check for hard-coded labels/columns)

## Before creating a new page

- [ ] Reuse check: is there a shared component that can render this entity?
- [ ] businessCode/entityKey defined in metadata layer
- [ ] All fields consumed from metadata, not hard-coded
- [ ] Field labels from metadata layer, not page-local strings

## Report governance

- [ ] Standard list/chart reports use shared report engine with reportCode
- [ ] Custom report pages only when metadata-driven approach insufficient
- [ ] Report permissions enforced by backend engine, not frontend component
- [ ] Relation fields auto-imported from master data (productId → productName)

## Anti-patterns

- Hard-coded field labels in page files
- Duplicate filter/form definitions across pages of the same entity
- page_config used as primary field definition source
- Database columns added without metadata registration
