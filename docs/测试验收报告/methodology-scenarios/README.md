# Methodology Scenario Regression Evidence

Generated evidence from `scripts/py/test_methodology_scenarios.py` is written
here. The test intentionally creates temporary miniature methodology fixtures
outside this directory, verifies both passing and failing cases, then removes
those fixtures.

The scenarios cover:

1. Product-led task pack contains the owner/AI handoff, truth map, safety,
   batch, verification, and closure sections.
2. Skill responsibility matrix assigns a single primary owner for key delivery
   stages.
3. Methodology audit accepts a complete fixture and rejects a fixture missing
   the safe change/code location contract.
