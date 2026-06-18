# Stable Foundation Checklist

Use this checklist when a GERP task touches version, module, feature, permission, route, API, FieldPackage, parameters, reports, schema sync, or release closure.

## Classification

- [ ] Which single source of truth owns the change?
- [ ] Which table/service is authoritative?
- [ ] Which runtime output should consume it?
- [ ] Which frontend/backend consumers must be updated?

## Reality Check

- [ ] DB structure checked with `DESCRIBE`.
- [ ] Counts or sample rows checked.
- [ ] Existing service/controller/interceptor located.
- [ ] Existing docs and release task read.
- [ ] No conclusion based only on naming.

## Closure

- [ ] Source object exists.
- [ ] Ownership is clear.
- [ ] Runtime compiler or profile output exists.
- [ ] Consumer uses runtime output.
- [ ] Backend guard exists.
- [ ] Cache/version invalidation is defined.
- [ ] Allow/deny tests or smoke checks exist.
- [ ] Evidence file is written.

## Evidence

Record at least one of:

- SQL result;
- API smoke;
- browser smoke;
- compile/test output;
- log proof;
- screenshot if UI behavior matters.

