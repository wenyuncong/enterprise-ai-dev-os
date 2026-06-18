# Security Policy

## Supported Versions

The `main` branch is the supported development line.

## Reporting A Vulnerability

Please do not disclose vulnerabilities publicly before maintainers have had a chance to review them.

Use GitHub private vulnerability reporting if it is enabled for the repository. If it is not enabled, open a minimal issue that says a private report is needed, without posting secrets, exploit details, customer data, or private paths.

## What To Report

Please report:

- scripts that may leak private files
- boundary-check bypasses
- unsafe generated adapter behavior
- accidental inclusion of secrets, local paths, private archives, or unredacted material
- supply-chain or workflow risks

## Open-Source Boundary Incidents

If a contribution accidentally includes private material:

1. Stop merging or publishing related changes.
2. Remove the material from the PR.
3. Run `py scripts/py/check_open_source_boundary.py --project-root .`.
4. Ask maintainers whether history cleanup is needed.

## Required Local Checks

```powershell
py scripts/py/audit_methodology.py --project-root .
py scripts/py/check_open_source_boundary.py --project-root .
```
