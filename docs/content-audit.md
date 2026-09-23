# Content and helper audit — 2026-09-23

Scope: the skill entry point, 15 reference guides, README installation/publication claims, issue-search helper and its tests. This is a source/document review with targeted primary-source verification. It is not a hardware qualification, an exhaustive external-link crawl or an independent agent behavioral evaluation.

## Findings and disposition

| Priority | Finding | Disposition |
| --- | --- | --- |
| P2 | The issue helper rejected literal diagnostics such as `"PLL not locked"`, including words inside quotes, contradicting its exact-error-search workflow. | Fixed: validate only unquoted search syntax; preserve quoted literals. Regression cases cover ordinary lowercase wording, quoted OR/NOT, scope overrides and malformed quotes. |
| P2 | The LambdaEth recommendation mentioned TCP/throughput limits but omitted the pinned implementation's CRC-failed-frame handling. This could make it look more ready for application reuse than its own documentation supports. | Added the specific limitation and a validation requirement to the catalog and applied workflow. Author-reported fiber tests remain clearly distinguished from local tests. |
| P3 | The pinout index called UG986 a generic “138-device” document and attributed ambiguity to naming differences. This was insufficiently precise for selecting the correct chip-family pinout. | Replaced with the vendor's explicit GW5AST-138 UG986 listing and distinguished GW5AS-138 UG1107. |
| P3 | Detailed LiteEth device/lane assumptions pointed at a mutable branch. | Pinned the relevant source links to inspected HEAD `8641c497598b13e3016e6e2688da652d785d4b49`. |
| P3 | Repository validation was advertised for unspecified Python 3, but uses `Path.is_relative_to`, requiring Python 3.9+. | README now specifies Python 3.9+ for repository checks. |

## Evidence checked

- [LambdaEth pinned README](https://github.com/key2/lambdaeth/blob/14bf0dd19914a583993d119eeee86a3abff235e6/README.md): SFP hardware claims and limitations.
- [White Rabbit pinned target guide](https://github.com/enjoy-digital/litex_wr_nic/blob/9afea1c6df396c5e0835178f4d95a119af39635b/doc/tang_mega_138k_pro.md): optical operation versus uncompleted absolute calibration.
- [Gowin UG986 listing](https://www.gowinsemi.com/en/document/main/database/1/?order=DESC&page=8&support_search=&type=version) and [UG1107 listing](https://gowinsemi.com/en/document/main/database/2915/?order=ASC&page=1&support_search=&type=version): distinct device-family pinouts.
- Git remote HEAD checks confirmed the official example hashes already recorded in the example index. The example targets are not presented as repository-wide or universally compatible.
- Manual consistency review retained the distinctions between Pro/non-Pro/Console, silicon versus PCB revision, SRAM versus flash, raw link versus Ethernet, and source availability versus open-source licensing.

## Verification performed after fixes

Verification used Python 3.12.3 from the repository root. The audited state includes uncommitted modifications and new files over base commit `5797e24bf2c0706c30b8d30dcab33e11851b9176`; the base commit alone does not contain the audited fixes. This report does not identify an immutable snapshot of those working-tree changes.

Commands used:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
python3 /home/aurelien/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/sipeed-tang-mega-138k
git diff --check
```

The skill-creator validator is an external local tool, not bundled in this repository; its absolute path records this environment and must be adapted on another installation.

- Ten helper unit tests passed, including the new literal-diagnostic regression cases.
- The repository validator passed: all 15 references are reachable, and local file links recognized by its Markdown-link pattern resolve in README.md and the Markdown files reachable from the skill entry point. It does not scan every repository document, including this audit.
- The skill-creator frontmatter validator passed.
- `git diff --check` passed.

These checks do not validate external document contents, every Markdown anchor, electrical pin mappings, vendor builds, timing closure or actual boards. The repository validator is a lightweight check of this package's expected format, not a general YAML/Markdown or Agent Skills conformance implementation.

## Remaining limitations

There is no demonstrated board test or vendor implementation run for this skill's recommendations in this workspace. Reference projects retain their own applicability, licensing and validation limits. Some manual entries are exact-title discovery keys rather than inspected full manuals; they should not be interpreted as an audited vendor-document archive. The earlier publication record still requires pushing the reviewed repository and checking remote skills discovery.

A future behavioral evaluation should exercise an ambiguous-board pin request, a wrong-clock DDR diagnosis, a B-to-C PHY port, and a “10GbE” request offered a 1GbE baseline. No such independent evaluation is claimed by this audit.
