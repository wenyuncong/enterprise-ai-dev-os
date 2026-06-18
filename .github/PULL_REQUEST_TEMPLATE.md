## Summary

Describe what changed and why.

## Area

- [ ] Rules
- [ ] Skills
- [ ] Tool adapters
- [ ] Documentation
- [ ] Audit scripts
- [ ] Website
- [ ] Other

## Verification

Paste the checks you ran:

```text
py scripts/py/audit_methodology.py --project-root .
py scripts/py/check_open_source_boundary.py --project-root .
py scripts/py/score_ai_development_readiness.py --project-root .
powershell -NoProfile -ExecutionPolicy Bypass -File tools/deploy.ps1 -Tool verified -DryRun
```

## Open-Source Boundary

- [ ] I did not include private strategy, raw archives, local tool state, secrets, customer data, or unredacted evidence.
- [ ] I did not commit generated adapter output directories.
- [ ] I updated compatibility claims only with evidence.

## Notes

Add screenshots or references when helpful and safe.
