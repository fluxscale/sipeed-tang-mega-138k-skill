# Applying upstream fiber projects to engineering tasks

Use this guide when choosing, adapting or debugging an optical-link design. Read the [project catalog](fiber-projects.md) for source provenance and validation limits. These workflows derive engineering decisions from those projects; they do not certify an untested port.

## Choose the baseline from the requested result

| User wants | First baseline | Establish before adapting |
| --- | --- | --- |
| Prove modules, fiber and serial lanes work | Sipeed Customized PHY PRBS | Supported line rate, actual clock setup, matched generator/checker and loop wiring |
| Exchange IP packets over gigabit fiber | LambdaEth 1000BASE-X example | Exact PHY dependency, partner negotiation, MAC/stack limits and application buffering |
| Integrate optical Ethernet into a LiteX SoC | LiteEth GW5_1000BASEX | Supported silicon/lane, platform resources, clock/reset integration and stream interfaces |
| Distribute synchronized time over fiber | LiteX White Rabbit Tang target | Peer compatibility, clock actuation, calibration and independent timing measurement |
| Send application packets between FPGAs | Counter-to-SFP-to-UDP demo | Custom framing, alignment, integrity checks, throughput mismatch and source license |
| Build a 10GbE sender | Sipeed XGbE_UDP | 10G PCS/PMA, MAC and application boundaries; vendor IP and incomplete setup documentation |
| Move a design to another GW5AST carrier | Closest matching PHY implementation | Package/revision, bonded lane, refclock route, SFP controls and physical constraints |

Do not choose a project solely because its repository name says Ethernet or NIC. For example, a raw PRBS test, a custom packet link, a 1000BASE-X stack, a 10GBASE-R stack and a White Rabbit endpoint solve different problems.

## Capture a porting contract

Before changing source, record both upstream and destination values for:

- Device, silicon revision, package, transceiver primitive, quad and lane.
- Reference clock frequency, source pad, clock-generator startup configuration and shared users.
- Parallel interface width and coding boundary: raw symbols versus decoded bytes/control flags, hard versus fabric PCS.
- TX/RX clocks, reset sequencing, status validity, CDC and accepted-transfer semantics.
- SFP presence, TX-disable, RX-loss indication, I2C routing and module identification.
- CSR generation inputs, supported tool build and dependency commits.
- Protocol, link partner settings, application throughput, buffering and error policy.

An enum listing a device establishes a configuration option, not qualification of that device. Do not remove a device guard to force a build without replacing and validating the assumptions it protects. Keep an unchanged upstream build for comparison when possible.

## Diagnose from the physical link toward the application

Use a bounded experiment at each stage and retain the first failing observation:

1. **Module/control:** confirm the module is powered, present and enabled; inspect LOS and the actual optical/cable path. Do not assume an unconnected TX-disable signal enables transmission.
2. **Reference/PLL:** check the selected physical reference and its configured rate, then PLL status using the implementation's documented interpretation.
3. **CDR/alignment:** establish recovered-clock activity, alignment and valid data. Lock alone does not prove usable symbols or packet boundaries.
4. **PCS/protocol:** inspect coding/disparity errors, negotiation state and partner abilities. Test a matched peer before changing negotiation behavior. Loopback success is weaker evidence than interoperability.
5. **MAC:** inspect frame counts, length/FCS errors and drop/overflow counters. Determine where malformed frames are discarded.
6. **Network:** use packet captures to distinguish ARP, IP addressing, checksums and protocol behavior from PHY faults.
7. **Application:** measure accepted payload, loss, sustained throughput and queue occupancy under backpressure. Account for a faster serial input feeding a slower Ethernet output.

For every stage distinguish unavailable instrumentation from a measured zero. A capture clocked by recovered RX cannot complete if that clock stops; provide a timeout and a status path in a clock domain that remains alive.

## Lessons to reuse, with their boundaries

### LambdaEth: complete packets and observable negotiation

Its [pinned README](https://github.com/key2/lambdaeth/blob/14bf0dd19914a583993d119eeee86a3abff235e6/README.md) documents separate SFP negotiation/status observations, frame sniffers and store-and-forward buffering. Use these as instrumentation patterns. Measure protocol-core throughput separately from gigabit bursts on the wire. The pinned version flags CRC failures without dropping those frames ahead of the protocol core; test error propagation and reject invalid frames at the appropriate boundary before production use. Its compact TCP implementation has explicit limitations; validate required connection/flow-control behavior before adopting it for a product. Do not infer two complete application stacks from two negotiating lanes.

### LiteEth: inspect implementation restrictions

The [GW5 PHY source](https://github.com/enjoy-digital/liteeth/blob/8641c497598b13e3016e6e2688da652d785d4b49/liteeth/phy/gw5_1000basex.py) restricts its supported device/lane arrangement and exposes valid data and FIFO occupancy. Preserve that information at integration boundaries. Do not assume a raw interface transfers meaningful data on every cycle or that comma alignment establishes deterministic latency. A different silicon version or reference-clock arrangement requires an evidence-backed port.

### White Rabbit: distinguish a locked servo from accurate time

The [Tang target guide](https://github.com/enjoy-digital/litex_wr_nic/blob/9afea1c6df396c5e0835178f4d95a119af39635b/doc/tang_mega_138k_pro.md) separates reported synchronization from uncompleted absolute calibration. Reuse this distinction: test reacquisition, latency repeatability and physical PPS against an independent reference. Account for module/board delay, fiber asymmetry and cable delay. Clock-generator I2C traffic is part of this design's control loop; avoid competing accesses or arbitrary clock resets during measurements.

### Custom SFP transport: end-to-end accounting

The [two-board forwarding design](https://github.com/JerryPhan15/tangmega138k-pro-dock-demos/tree/main/projects/counter-a-to-b-sfp-rgmii) separates alignment, packet parsing, CRC and forwarding. Reuse the layered diagnostic approach, not unverified pin settings or undisclosed licensing assumptions. Add sequence numbers and counters at ingress/egress so dropped packets can be localized. Confirm the optical protocol with the peer; SFP is a form factor, not proof of Ethernet framing.

## Search the owning component

The helper's `networking` group searches LiteEth, LiteX White Rabbit, LambdaEth and gowin-serdes:

```sh
python3 scripts/search_issues.py --group networking --query 'GW5AST' --dry-run
python3 scripts/search_issues.py --group networking --query 'alignment' --kind all
```

Use a single repository for a specific error and reopen current comments/linked commits. Search Sipeed for its generated example, LiteEth for the GW5 PHY, LambdaEth for its protocol integration, and White Rabbit for its target-specific clock/timing behavior. Zero issue results can mean a young project, poor keywords or a different tracker; inspect source and recent commits before concluding a behavior is supported.

## Deliver the adaptation with evidence

Include the upstream commit, porting contract, exact changed assumptions, build/timing results, link-state observations and bounded traffic test. Report which stages passed, what failed and whether hardware was available. Keep upstream author reports distinct from local measurements. List required proprietary tools/IP and any unresolved license terms; public source availability alone does not establish redistribution permission.
