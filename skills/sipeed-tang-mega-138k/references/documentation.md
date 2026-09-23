# Documentation and evidence map

Research baseline: 2026-09-23. Links identify sources, not a promise that their current contents match an old tool release. Manuals and issue states change; verify the relevant revision when applying advice. This skill supplies engineering procedures and source navigation, not redistributed vendor manuals.

## Evidence precedence

For wiring, use the schematic for the physical SOM/carrier revision, then the package pinout and project constraints. For silicon limits, use the exact part/speed-grade datasheet and errata. For IP behavior, use the manual delivered with that IP generation. A working example establishes only its actual configuration. Marketing pages and issue reports are useful discovery aids, but do not override contradictory electrical evidence.

Record document title/ID, revision/date, URL, section or printed page, board applicability, and retrieval date. For downloaded PDFs, record a SHA-256 when reproducibility matters. Printed page numbers can differ from PDF page indices. Inspect schematic diagrams visually; PDF text extraction can detach a net label from its pin. Do not infer missing pin mappings from extracted text order.

## Sipeed primary sources

| Source | What to retrieve |
| --- | --- |
| [Mega 138K Dock wiki](https://wiki.sipeed.com/hardware/en/tang/tang-mega-138k/mega-138k.html) | Non-Pro overview, tool/programming notes, revision caveats; contains internal inconsistencies discussed in board identification |
| [Mega 138K Pro wiki](https://wiki.sipeed.com/hardware/en/tang/tang-mega-138k/mega-138k-pro.html) | Pro overview, carrier peripherals, initial bring-up guidance |
| [Tang Console wiki](https://wiki.sipeed.com/tangconsole) | Console carrier identification and hardware links |
| [Non-Pro schematics](https://dl.sipeed.com/shareURL/TANG/Mega_138K_60K/02_Schematic) | Choose both the correct 138K SOM and carrier PDFs; this directory also covers 60K |
| [Non-Pro miscellaneous/constraints](https://dl.sipeed.com/shareURL/TANG/Mega_138K_60K/08_Misc) | Candidate complete CST; validate against schematic before using |
| [Pro schematics](https://dl.sipeed.com/shareURL/TANG/Mega_138K_Pro/02_Schematic) | Pro SOM and dock schematics |
| [Pro specification](https://dl.sipeed.com/shareURL/TANG/Mega_138K_Pro/01_Specification) | Mechanical/electrical context and block diagrams |
| [Console schematics](https://dl.sipeed.com/shareURL/TANG/Console/02_Schematic) | Console carrier wiring; match hardware revision |
| [Tang common questions](https://wiki.sipeed.com/hardware/en/tang/common-doc/questions.html) | Device-version identification and shared tool/debugger problems |
| [Debugger update guide](https://wiki.sipeed.com/hardware/en/tang/common-doc/update_debugger.html) | Firmware procedures for the identified debugger; updating is a separate mutation |
| [Wiki source/history](https://github.com/sipeed/sipeed_wiki) | Compare English/Chinese revisions, inspect corrections and broken links |

During the baseline link check, two Sipeed download listings returned transient HTTP 502 errors and the SUG283 CDN fetch timed out. Their official discovery links are retained; use the board wiki or vendor database if direct retrieval fails. No successful download is claimed for those checks.

Download portals can require JavaScript and directory selection. If a link renders an empty listing, navigate from the board wiki or inspect the wiki source; do not manufacture a PDF filename.

## Gowin manuals

Start at the [Gowin documentation database](https://www.gowinsemi.com/en/document/) or [official search](https://www.gowinsemi.com/en/support/search/). Search by exact title and document ID. Some files require a vendor account or are bundled with the installation. Prefer official access; do not route around access restrictions.

| Document / search key | Use and applicability check |
| --- | --- |
| [DS1239: GW5AST series datasheet](https://cdn.gowinsemi.com.cn/DS1239E.pdf) | Current family resource/package tables, electrical limits, speed grades; inspect actual PDF revision |
| [DS1104: older GW5AST datasheet](https://cdn.gowinsemi.com.cn/DS1104E.pdf) | Historical projects; compare against DS1239 rather than mixing limits |
| UG1102, GW5AST package and pinout guide | Package outline, ball/bank relationships; select PG484 or FPG676 as fitted |
| [UG986, GW5AST-138 pinout](https://www.gowinsemi.com/en/document/main/database/1/?order=DESC&page=8&support_search=&type=version) | Obtain the PDF/XLSX for the exact package; do not substitute the separate GW5AS-138 pinout (UG1107) |
| UG984, GW5AT/GW5AST schematic manual | Custom carrier/SOM design checks; not a Sipeed schematic |
| [UG306: Arora V clock guide](https://cdn.gowinsemi.com.cn/UG306E.pdf) | PLL, global/HCLK routing, clock placement and supported modes |
| UG304, Arora V programmable IO (GPIO) guide | IO logic, serializers, delay resources, electrical mode restrictions |
| Arora V BSRAM & SSRAM user guide | Supported widths/depths, read/write modes, initialization and ECC |
| Arora V DSP user guide | Arithmetic modes, internal registers, cascade and mapping |
| Arora V CFU user guide | LUT/carry/fabric structure where inference or placement needs investigation |
| UG704, Arora V 138K programming/configuration guide | Boot modes, external flash and configuration sequencing; title scope can include 75K in newer editions |
| [SUG283: Gowin primitives](https://cdn.gowinsemi.com.cn/SUG283E.pdf) | Primitive declarations and parameters; follow its Arora V-specific references |
| SUG100, Gowin software user guide | Project flow, supported options and Tcl usage |
| Gowin timing constraints / timing analysis guides | Installed SDC dialect, reports, generated clocks and exceptions |
| Arora V design physical constraints guide | CST syntax, IO/clock placement and legal physical resources |
| Gowin Programmer user guide and release notes | Exact operation names and device/flash support in the installed version |
| Gowin DDR3 Memory Interface IP user guide | Geometry, user interface timing, initialization/calibration, generated constraints |
| Arora V PCI Express Controller IP user guide | Hard-IP configuration, streaming interfaces, BARs and resets |
| Gowin SerDes / Customized PHY IP guides | PLL/refclock choices, lane/quad restrictions, reset and status sequencing |
| Gowin RISC-V AE350 SOC hardware/software manuals | Subsystem integration, address map, SDK, boot and debugger requirements |
| Arora V hardened MIPI D-PHY guide | Hard-PHY availability by device/package, lane mapping and electrical requirements |

Do not use the general Gowin clock guide UG286 as the sole authority for Arora V; SUG283 directs Arora V clock users to UG306. Do not assume similarly named GW5A/GW5AT/GW5AR manuals cover GW5AST features.

The database listing and the downloaded DS1239 cover carried different release dates during research. Record the actual downloaded revision and hash instead of labeling any CDN file “latest.” Recheck the database and errata for hardware-critical decisions.

## Examples and source repositories

Use the [official example index](official-examples.md) for inspected commit hashes, project paths, and target differences within each repository.

- [Sipeed Mega 138K examples](https://github.com/sipeed/TangMega-138K-example): inspect `pmod_led`, `ddr_memory`, `pcie_dma_demo`, `hdmi_colorbar`, `hdmi_svo`, `ch569_hspi2cdc`, `udp_rgmii_send`, `audio_i2s`, and `system_report` as relevant.
- [Sipeed Pro examples](https://github.com/sipeed/TangMega-138KPro-example): inspect `key_led`, `ddr_test`, `pro_ddr_test`, `pcie_dma_demo`, `sfp+`, `simple_video_out`, `ae350_customized_demo`, and `usb2_soft`.
- [Apicula](https://github.com/YosysHQ/apicula), [nextpnr](https://github.com/YosysHQ/nextpnr), [Yosys](https://github.com/YosysHQ/yosys): open-source synthesis, device databases, placement/routing and packing. Check each stage separately.
- [openFPGALoader](https://github.com/trabucayre/openFPGALoader): programming support, board definitions, device/flash paths. Its support does not imply synthesis support.
- [Verilator manual](https://verilator.org/guide/latest/), [Icarus Verilog](https://github.com/steveicarus/iverilog), [cocotb documentation](https://docs.cocotb.org/en/stable/), [SymbiYosys documentation](https://symbiyosys.readthedocs.io/en/latest/): simulation and formal verification; vendor encrypted models may require another simulator.

Use pinned commit links in delivered designs. Example folder presence does not establish compatibility, completeness, or maintenance status. Keep third-party code license/attribution when copying permitted portions; vendor IP has separate licensing.
