# Reproducibility and evidence templates

Use the relevant subset. Unknown fields remain explicitly unknown; do not block unrelated work to fill every field.

## Target and build record

```text
Task / expected behavior:
SOM name and PCB revision:
Carrier name and PCB revision:
FPGA full marking / package / silicon version / speed grade:
DDR and flash markings / populated capacity:
Power source / clock source and measured or documented frequency:
Boot straps / attached peripherals:
Schematic revision and pages:
Project URL + commit / local changes:
EDA edition + complete build / IP versions:
Programmer + debugger firmware / OS:
Top module / CST / SDC / build command:
Bitstream path + SHA-256 / build seed and options:
Programming target (SRAM or named flash region):
```

## Constraint and timing review

```text
Pin provenance table attached:
Bank voltage and IO standards checked:
Root/generated clock inventory:
Input/output min/max timing budgets:
CDC structures and reset-domain strategy:
Exceptions, scope and rationale:
Unconstrained paths and unresolved collections:
Setup/hold and relevant IO/recovery/removal results:
Resource/clock/IO warnings requiring action:
```

## Hardware experiment

```text
Hypothesis:
Known-good control:
Single change under test:
Procedure and maximum duration:
Expected observations / pass and fail conditions:
Observed counters, state, traces and first error:
Traffic size, address coverage, iterations and duration:
Reset/power-cycle history:
Result: reproduced / not reproduced / inconclusive
What this establishes:
What remains untested:
Artifacts and hashes:
Next discriminating action:
```

## Upstream issue draft

```text
Title: [subsystem] observed failure on [part/revision] with [tool version]

Expected behavior:
Actual behavior and first relevant error:
Hardware/software identity:
Minimal source/configuration and exact reproduction commands:
Known-good comparison and first failing revision if known:
Constraint/timing/programming evidence:
Observed hardware state and bounded tests:
Related issues/PRs, including why they do or do not apply:
Sanitized logs/waveforms and artifact hashes:
```

Exclude license keys, API tokens, private host identifiers and unrelated logs. Identify third-party files that cannot be redistributed and provide lawful acquisition instructions. A draft is not a submission; preserve the user's authority over external posting.

## Completion wording

Say exactly what was checked: “RTL elaborates and the FIFO scoreboard passes; vendor implementation and board tests remain unrun” or “This image completed N specified transactions over T seconds on this board revision.” Avoid “fully validated,” “timing clean” without coverage, or “1 GB tested” when only endpoints/address bits were checked.
