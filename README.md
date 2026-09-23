# Sipeed Tang Mega 138K / GW5AST FPGA skill

A detailed engineering skill for **Sipeed Tang Mega 138K, Mega 138K Pro, Tang Console 138K, and Gowin GW5AST-138**. It helps coding agents design RTL, trace hardware constraints, reproduce vendor projects, close timing, bring up interfaces, and investigate upstream failures using primary documentation and version-specific evidence.

The skill starts with the actual SOM, carrier, package, and silicon revision. It distinguishes documented facts, upstream reports, engineering hypotheses, and reproduced results. It does not assume that Pro, non-Pro, and Console pinouts or clocks are interchangeable.

## Installation

### 1. skills.sh

With Node.js/npm available:

```sh
npx skills add fluxscale/sipeed-tang-mega-138k-skill --skill sipeed-tang-mega-138k
```

Choose your agent and installation scope in the prompts. Inspect discoverable skills first if desired:

```sh
npx skills add fluxscale/sipeed-tang-mega-138k-skill --list
```

See the [skills.sh CLI documentation](https://skills.sh/docs/cli) and [skills CLI options](https://github.com/vercel-labs/skills). The commands require the skill files to be pushed to the public repository; a local working copy is not automatically published.

### 2. Claude

For Claude Code, install globally:

```sh
npx skills add fluxscale/sipeed-tang-mega-138k-skill --skill sipeed-tang-mega-138k --agent claude-code --global
```

Or install manually from a checkout, without Node.js:

```sh
git clone https://github.com/fluxscale/sipeed-tang-mega-138k-skill.git
cd sipeed-tang-mega-138k-skill
mkdir -p ~/.claude/skills
cp -R skills/sipeed-tang-mega-138k ~/.claude/skills/
```

Use a fresh destination for the manual copy; remove or back up an older installation first to avoid leaving stale files. For project scope, copy the skill directory into your project's `.claude/skills/` instead. Invoke `/sipeed-tang-mega-138k`, or describe a matching FPGA task. See [Claude Code skills](https://code.claude.com/docs/en/skills).

For Claude on the web, package just the skill folder from this checkout:

```sh
cd skills
zip -r ../sipeed-tang-mega-138k.zip sipeed-tang-mega-138k
```

Upload the ZIP through the custom Skills settings available to your account. Check [Claude's Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) for current availability. Network access and local FPGA hardware/tools depend on the environment; uploading a skill does not provide them.

### 3. Codex

Install globally:

```sh
npx skills add fluxscale/sipeed-tang-mega-138k-skill --skill sipeed-tang-mega-138k --agent codex --global
```

Or, from the repository checkout, install manually:

```sh
mkdir -p ~/.agents/skills
cp -R skills/sipeed-tang-mega-138k ~/.agents/skills/
```

Use a fresh destination for the manual copy. For project scope, use your project's `.agents/skills/` directory. Invoke `$sipeed-tang-mega-138k`, or let Codex select it for a matching task. Current official documentation uses `~/.agents/skills` for user skills; installations that use a legacy/custom skill path should follow their local configuration. See [OpenAI's skill documentation](https://learn.chatgpt.com/docs/build-skills).

## What it covers

| Area | Included guidance |
| --- | --- |
| Hardware identity | SOM/carrier revisions, PG484 vs FPG676, device B/C, clocks, bank voltage and schematic-to-ball tracing |
| Documentation research | Sipeed schematics/wiki/examples, Gowin datasheets and Arora V/IP manuals, source precedence and revision tracking |
| Toolchains | Gowin project inspection, reproducible builds, generated-IP migration and feature-specific open-source support checks |
| RTL and verification | Streaming protocols, DSP/memory inference, resets, simulation, formal checks and hardware observability |
| Constraints and timing | CST, SDC, root/generated clocks, IO budgets, CDC, reset crossings, setup/hold and justified exceptions |
| DDR3 | Geometry, calibration, IP handshakes, ordering, alias tests, capacity coverage and measured bandwidth |
| PCIe and SerDes | Refclocks, resets, training, BARs, DMA, SFP+, loopback and error-rate evidence |
| Peripherals | DVI/TMDS, RGB panels, DVP/MIPI cameras, RGMII/UDP, CH569/USB, audio, SD, GPIO, ADC and fan control |
| AE350 | Hard RISC-V subsystem, BSP/firmware/boot, fabric integration, interrupts, caches and shared memory |
| Programming | JTAG, SRAM, flash identity/layout, cold boot, debugger recovery and failure isolation |
| Issue research | Read-only GitHub search, closed issues/PRs, correction history, release applicability and reproducible reports |

Browse the [skill entry point](skills/sipeed-tang-mega-138k/SKILL.md), [documentation map](skills/sipeed-tang-mega-138k/references/documentation.md), and [troubleshooting guide](skills/sipeed-tang-mega-138k/references/troubleshooting.md). Detailed references load only when needed.

## Primary example repositories

- **[sipeed/TangMega-138K-example](https://github.com/sipeed/TangMega-138K-example)** — the primary non-Pro source for DDR3, PCIe, video, CH569, Ethernet, audio, GPIO and other examples. Its issues and PRs are part of the research workflow.
- **[sipeed/TangMega-138KPro-example](https://github.com/sipeed/TangMega-138KPro-example)** — Pro-specific examples, including SFP+/SerDes and AE350 integration.

Examples are starting points, not guaranteed compatible binaries. Pin commits and verify the target before building or programming.

## Fiber and SFP projects

The [fiber project catalog](skills/sipeed-tang-mega-138k/references/fiber-projects.md) covers LambdaEth 1000BASE-X, LiteX White Rabbit on the Pro dock, Sipeed PRBS fiber/DAC tests, and its 10GbE UDP demo, with source links and validation limits. The [applied fiber workflows](skills/sipeed-tang-mega-138k/references/fiber-workflows.md) turn those findings into baseline selection, porting checks and staged diagnostics.

## Example requests

- “Identify this Mega 138K board and derive a pin table from its SOM and carrier schematics.”
- “Use Sipeed's TangMega-138K-example DDR3 project as the baseline. Diagnose calibration failure on my device-C Console.”
- “Review my CST and SDC for missing clocks, invalid bank voltages, unsafe CDC, and hidden timing violations.”
- “Migrate this Pro SerDes example to my Gowin EDA version and investigate upstream issues.”
- “Bring up a PCIe BAR test, then validate DMA buffers and measure payload throughput.”
- “Determine which parts of this GW5AST-138C design the current open-source flow supports.”

## Issue-search helper

Python 3, no third-party dependencies:

```sh
python3 skills/sipeed-tang-mega-138k/scripts/search_issues.py \
  --repo sipeed/TangMega-138K-example --query DDR3

python3 skills/sipeed-tang-mega-138k/scripts/search_issues.py \
  --group tools --query GW5AST --format json
```

Use `--help` for filters and `--dry-run` to inspect queries without network access. An optional `GITHUB_TOKEN` or `GH_TOKEN` raises authenticated API limits when applicable. Queries are sent to GitHub; use public keywords rather than private logs. The helper searches issues and PRs but does not execute suggested fixes or post anything.

## Validation and publication

Run the repository checks with Python 3.9 or newer:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

To verify local skills CLI discovery without installing:

```sh
npx skills add . --list
```

The repository uses the standard `skills/<name>/SKILL.md` layout and includes its references and helper inside the installable directory. To release, review the diff, commit and push the files to the public GitHub repository, then check remote discovery with the install command's `--list` option. Confirm visibility on [skills.sh](https://skills.sh/) separately; local validation does not establish directory listing. The [skills.sh documentation](https://skills.sh/docs) explains its installation-based discovery/ranking.

The checked-in workflow validates package structure and runs the helper tests. It does not run vendor FPGA builds or hardware tests. Research baseline: **2026-09-23**. Source content and issue status must be rechecked for the target's versions.

## Contributing and license

For corrections, include the affected board/silicon/tool versions, authoritative source or reproducible evidence, and what remains untested. Keep the entry point compact; put subsystem detail in its existing reference. Never add guessed pinouts or present an upstream comment as a verified fix.

Original skill content and helper code are [MIT licensed](LICENSE). Linked manuals, vendor IP, and third-party examples retain their own licenses. This is an independent community project, not an official Sipeed or Gowin product.
