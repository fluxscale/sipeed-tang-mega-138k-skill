# PCIe, DMA, and SerDes/SFP+

Primary baselines: [non-Pro PCIe demo](https://github.com/sipeed/TangMega-138K-example/tree/main/pcie_dma_demo), [Pro PCIe demo](https://github.com/sipeed/TangMega-138KPro-example/tree/main/pcie_dma_demo), and [Pro SerDes examples](https://github.com/sipeed/TangMega-138KPro-example/tree/main/sfp%2B). Read the generated IP manuals and board schematics. These interfaces depend on package bonding and carrier wiring as well as chip capability.

For reusable optical-link designs and author-reported hardware results, see the [fiber project catalog](fiber-projects.md), including LambdaEth and LiteX White Rabbit.

## PCIe layers

Establish host slot wiring, carrier lane routing, configured width/generation, reference clock topology, reset, power and any adapters. Match the generated hard-IP location and lane map. Treat advertised maxima separately from configured and negotiated link values. Insert/remove a conventional board edge connector only with the equipment powered down according to the board/host instructions.

Bring up in layers:

1. Power, reference clock and PERST/reset sequence.
2. Transceiver readiness and LTSSM progress; capture transitions/recovery loops if accessible.
3. Stable link state and negotiated speed/width.
4. Enumeration: vendor/device IDs, BAR type/size, configuration-space capabilities.
5. A simple documented BAR register read/write.
6. DMA descriptors and buffers, then sustained traffic and error handling.

On Linux, collect `lspci -nn` and `lspci -vv -s <BDF>` output for the identified endpoint, kernel version and relevant kernel messages. Replace `<BDF>` with the observed address. Distinguish endpoint not enumerating from driver binding or application failures. A narrow negotiated link can reflect physical routing, training or configuration; it is not automatically an RTL bandwidth problem.

## DMA integration

Use the operating system's DMA mapping APIs, with correct address width, alignment, ownership, barriers and cache synchronization. Do not treat a userspace virtual pointer or arbitrary physical address as a valid DMA address. Keep descriptors, completions and payload lifetimes explicit; release mappings only after the hardware can no longer access them.

Confirm endianness, byte enables, transfer length units, maximum payload/read-request settings, completion boundaries, tags/credits, and handling of backpressure. Test short, unaligned (if supported), page-boundary and long transfers with known patterns. Use buffers owned by the test and preserve IOMMU isolation; do not disable protections as a default debugging technique.

Driver build/signature problems are separate from FPGA link problems. [Pro issue #18](https://github.com/sipeed/TangMega-138KPro-example/issues/18) is a lead for module signing under Secure Boot. Follow the host's documented signing workflow when needed; a hardware task does not implicitly authorize changing boot policy or enrolling keys.

Report payload throughput, direction, transfer size, queue depth, duration, CPU overhead and negotiated link. Raw serial line rate is not application bandwidth.

## SerDes/SFP+ layers

Map quad/lane, TX/RX direction, reference clock source and frequency, differential pairs, polarity, AC coupling, lane sharing and supported line rate. Confirm reference-clock generator programming and startup state on the actual carrier. Optical module presence, LOS, TX-disable and module compatibility are separate from transceiver lock.

A transceiver is not a complete Ethernet MAC/PCS. PRBS loopback does not establish Ethernet framing, encoding, FEC or interoperability. Likewise, an SFP+ cage does not guarantee every inserted module or rate works.

Use this progression where supported:

- Reference clock and PLL lock.
- Documented reset completion and lane-ready status.
- Internal loopback with generator/checker matched for polynomial, seed and inversion.
- External electrical/optical loopback.
- Link partner with matching protocol, line rate, encoding and alignment.
- Application traffic with explicit error counters and sustained duration.

Measure tested bits and error count to report BER evidence. Zero errors over a finite interval is an observation, not a zero-BER guarantee. Capture loss-of-lock and reset events separately.

When upgrading tools, regenerate the complete PHY collateral and inspect port/status changes. [Pro issue #21](https://github.com/sipeed/TangMega-138KPro-example/issues/21) reports missing generated files and runtime trouble on a newer IDE; it is a diagnostic lead, not a verified universal patch.

## Escalation evidence

Include the exact SOM/carrier, package/revision, EDA/IP version, target lane/quad and refclock settings, host/module/adapter, negotiated state, relevant counters and the last working commit. Provide a bounded reproduction without private host memory, credentials or unrelated kernel logs.
