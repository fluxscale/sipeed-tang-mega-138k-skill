# Open-source SFP, fiber and SerDes projects

Research date: 2026-09-23. The demonstrated board applications below target the **Mega 138K Pro dock**; the FPGA-level section covers reusable code and non-Sipeed references. Hardware results below are author reports; this skill's maintainers did not reproduce them. Open-source application/PHY logic can still require Gowin's implementation tools and hard transceiver primitives. Check dependency licenses separately before redistribution.

## LambdaEth: Ethernet applications over fiber

[Repository](https://github.com/key2/lambdaeth) · [inspected README at 14bf0dd](https://github.com/key2/lambdaeth/blob/14bf0dd19914a583993d119eeee86a3abff235e6/README.md).

BSD-2-Clause Amaranth Ethernet stack with a Pro 1000BASE-X example: `examples/tang_mega_138k_1000basex.py`. Authors report simultaneous negotiation on both SFP cages and ICMP/UDP/TCP echo over fiber. One lane carries the full stack; the other supplies negotiation and observation. This is gigabit Ethernet, not a 10GbE implementation. The byte-wide protocol core limits sustained throughput to roughly 400 Mb/s at 50 MHz; TCP also has explicit simplicity/feature limits. Inspect its `gowin-serdes` dependency and patched Amaranth dependencies. Cached search results showed an older RGMII-only README: use the pinned source when evaluating SFP support.

## LiteX White Rabbit: timing over optical Ethernet

[Repository](https://github.com/enjoy-digital/litex_wr_nic) · [Pro guide at inspected commit 9afea1c](https://github.com/enjoy-digital/litex_wr_nic/blob/9afea1c6df396c5e0835178f4d95a119af39635b/doc/tang_mega_138k_pro.md).

The Pro target uses GW5AST-138B SerDes, the dock's clock generator and FPGA clock adjustment for White Rabbit. Its guide reports master/slave synchronization against SPEC-A7 and supports selecting either SFP cage, one lane per build. It documents optical setup and pinned build dependencies. Absolute timing accuracy remains unqualified until latency/asymmetry calibration and independent PPS measurements are completed. Servo-reported statistics are not independent timing accuracy. Despite the repository name, this Tang target has no PCIe NIC or persistent storage. Repository licensing is BSD-2-Clause, with White Rabbit under CERN OHL; inspect component-specific terms.

## Sipeed Customized PHY: fiber/DAC link bring-up

[Demo and instructions](https://github.com/sipeed/TangMega-138KPro-example/blob/main/sfp%2B/customized_phy/readme.md).

Official Pro examples at 1.25, 10.3125 and 12.5 Gb/s use PRBS7 checking over the two cages. Instructions cover paired optical modules and fiber or DAC/AOC loopback. Suitable as a physical-link baseline before implementing an application. PRBS success is not Ethernet interoperability. Check reference clock settings, module rate compatibility and current IDE/IP compatibility. The repository's Apache-2.0 license does not replace separate vendor-IP terms.

## Sipeed 10GbE UDP: application demo

[Project directory](https://github.com/sipeed/TangMega-138KPro-example/tree/main/sfp%2B/10G_Serial_Ethernet) · [repository overview](https://github.com/sipeed/TangMega-138KPro-example).

Sipeed labels this an SFP+ 10GbE UDP-send demo and marks its SFP examples verified. The subdirectory's `readme.txt` was only `TBD` during inspection. Use the actual `XGbE_UDP` project, generated IP, clock setup and constraints to reconstruct the setup; do not infer a complete NIC or bidirectional network stack from the label.

## Reusable SerDes infrastructure

[key2/gowin-serdes](https://github.com/key2/gowin-serdes) exposes Amaranth configuration/instantiation and CSR generation for Gowin transceivers; its inspected `pyproject.toml` declares MIT. LambdaEth uses it for its SFP PHY. Review the source and supported mode before reuse.

[key2/gowin_pipe](https://github.com/key2/gowin_pipe) is related USB PIPE/SerDes work with reported Pro bring-up. Its documented gaps include missing coding/ordered-set work and incomplete training reliability; it is not evidence of a completed fiber Ethernet product.

## Selection and further research

- For an observable optical link first, use the Sipeed PRBS example.
- For packet processing over 1GbE fiber, inspect LambdaEth.
- For clock/time distribution, inspect the White Rabbit target and its calibration limits.
- For a 10GbE application baseline, inspect Sipeed's UDP example and reconstruct its undocumented setup.

No turnkey, production-qualified open-source fiber product was established by this search. This is a bounded finding, not proof that none exists. Search repository READMEs as well as names/descriptions: GitHub queries such as `"138k" "sfp" in:readme` found projects that ordinary web searches missed. Recheck HEAD and pin the resulting source before building; search indexes can lag actual code.


## FPGA-level search beyond Sipeed

### LiteEth's GW5AST PHY

[BSD-2-Clause source: `gw5_1000basex.py`](https://github.com/enjoy-digital/liteeth/blob/master/liteeth/phy/gw5_1000basex.py) provides `GW5SerDes` and `GW5_1000BASEX`. The inspected implementation explicitly restricts the device to **GW5AST-138B**, Q1 lanes 0/1, at 1.25 Gb/s; the Ethernet wrapper uses a 100 MHz Q1 REFCLK1. This is reusable FPGA-specific source, not a general validated backend for every GW5AT/GW5AST revision. A custom board must supply the matching physical resources or adapt and validate the implementation. RX validity and FIFO occupancy matter; raw interface alignment does not guarantee deterministic latency.

### Amaranth's multi-device configuration layer

The [gowin-serdes configuration source](https://github.com/key2/gowin-serdes/blob/master/gowin_serdes/config.py) enumerates GW5AT-15, GW5AT-60, GW5AT-138 and GW5AST-138, with different hard-macro/quad metadata. Treat these as implemented configuration choices, not proof of hardware qualification for every device/mode. Porting requires the actual package, silicon version, primitive, lane/refclock selection, reset sequence, CSR collateral and timing constraints.

### Public generic GW5AST reference design

[ymj134/Gowin_Customized_PHY_RefDesign](https://github.com/ymj134/Gowin_Customized_PHY_RefDesign) contains a Gowin project, PRBS7 generator/checker and SerDes wrapper targeting **GW5AST-LV138FPG676AES**. Its README does not establish a specific carrier or optical hardware test. No clear repository license was established during this search: classify it as public reference material, not an independently licensed open-source product. Match constraints and vendor-IP terms before reuse.

### Non-Sipeed board and vendor optical IP

[Gowin DK_START_GW5AST-LV138FPG676A_V2.1](https://www.gowinsemi.com.cn/dev/31) is a same-family evaluation platform with official board documentation and SFP/SerDes applications. It is a hardware/reference-design route, not evidence of a complete open-source optical product.

[Gowin 10G Serial Ethernet guide](https://www.gowinsemi.com/upload/database_doc/2756/document/6831354fc9183.pdf) documents a 10GBASE-R PCS/PMA with XGMII and identifies its design files as encrypted Verilog. Do not list the vendor implementation as open-source because its reference wrapper is visible. Similarly, investigate [CPRI](https://www.gowinsemi.com/upload/database_doc/2485/document/671f0091ac9bd.pdf) and [BCDR](https://www.gowinsemi.com/upload/database_doc/3035/document/66f65cae45cf4.pdf) as vendor optical-transport references; their applicability and licenses need separate confirmation.

## Additional board-to-board application

[JerryPhan15 counter-to-SFP-to-UDP demo](https://github.com/JerryPhan15/tangmega138k-pro-dock-demos/tree/main/projects/counter-a-to-b-sfp-rgmii) documents two Pro boards: one sends framed counter data over SFP; the receiver handles alignment, de-whitening, CRC and buffering, then forwards packets to a PC over RGMII/UDP. It provides two projects and PC validation instructions. This is custom serial transport over SFP, not established Ethernet on the optical link. Public source and instructions were inspected; hardware results and redistribution license were not independently established. A companion [PRBS loopback demo](https://github.com/JerryPhan15/tangmega138k-pro-dock-demos/tree/main/projects/sfp-10g-loopback-ln0-ln1) is also available.

Broader search terms included GW5AST/GW5AT with SFP, SerDes, 10G, fiber and Chinese optical terms, plus README searches. GitHub API rate limiting curtailed some metadata retrieval; direct source inspection supplied the relevant code/documentation. No exhaustive ecosystem census or non-Sipeed hardware reproduction is claimed.
