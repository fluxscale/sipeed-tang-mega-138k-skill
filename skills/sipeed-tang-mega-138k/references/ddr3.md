# DDR3, on-chip memory, and bandwidth validation

Start from the exact board's official example: [non-Pro `ddr_memory`](https://github.com/sipeed/TangMega-138K-example/tree/main/ddr_memory) or [Pro repository](https://github.com/sipeed/TangMega-138KPro-example) (`ddr_test` / `pro_ddr_test`). Check available subdirectories and their target before choosing one. Use the Gowin DDR3 IP guide delivered with the generated controller.

## Establish topology

Identify DDR package markings, density, number of components, data width per chip, rank/chip-select wiring, bank/row/column geometry, DQ/DQS/DM mapping, supply/reference/termination, clock source and fitted speed grade. Two memory packages do not by themselves establish the controller's configured capacity.

Separate physical pin width, burst length and user-interface width. Determine whether each address field counts bytes, memory words, bursts or user beats from the actual IP manual. Calculate the address range using that definition. Record data-lane ordering and byte-mask polarity explicitly.

## Reproduce calibration first

1. Use an unmodified, matching baseline. Record input clock frequency and target B/C revision before changing the controller.
2. Regenerate DDR3 and supporting PLL IP for the target when necessary. Preserve the generated clock/reset/calibration structure, including `PLL_INIT` or dynamic-PLL logic where generated.
3. Implement with all required IP constraints. Check clock reports, IO placement and setup/hold coverage.
4. Observe power/reset, reference clock, PLL status and controller initialization/calibration completion. Add a bounded timeout and report which stage stalls.
5. Issue no application traffic until the controller's documented ready/calibrated condition is satisfied. Check reset polarity and synchronization into its user domain.

A useful caution: [non-Pro issue #13](https://github.com/sipeed/TangMega-138K-example/issues/13) resolved a Console calibration report by correcting a clock assumption; the preceding [#12](https://github.com/sipeed/TangMega-138K-example/issues/12) should not be treated as an independent hardware defect. [PR #14](https://github.com/sipeed/TangMega-138K-example/pull/14) adds related documentation/evidence. Read current comments and applicability before using them.

## Verify user-interface semantics

Treat command acceptance, write-data acceptance, read-response validity and completion as separate events if the IP presents them that way. Never advance an address or retire a transaction just because valid was asserted. Respect write-data end markers, alignment, mask polarity and outstanding-transaction limits.

Do not assume the final accepted write is already visible to an immediately issued read. Follow the controller's ordering/completion guarantees. An arbitrary fixed delay can help diagnose an ordering problem but is not a portable replacement for a documented completion contract. Record any bounded settling period and why it is valid for the chosen configuration.

## Memory tests in increasing scope

| Test | Evidence it provides |
| --- | --- |
| Fixed address, complementary patterns | Basic command/data path and obvious stuck bits |
| Walking ones/zeros and byte masks | Data-bit/lane and mask behavior |
| Distinct values at base, power-of-two address offsets and final aligned beat | Address alias and endpoint mapping; not exhaustive cell coverage |
| Burst boundary, row/bank boundary and turnaround tests | Address conversion, scheduling and burst behavior |
| Random address/data with a scoreboard | Reordering, loss, duplication and data integrity within tested space |
| Sustained mixed reads/writes, refresh periods and backpressure | Stability and traffic-dependent faults |
| Full-range patterns and long-duration tests | Broader capacity/retention/load evidence with stated coverage |

Reserve a scratch region if firmware/framebuffers use the same memory. Do not run destructive patterns over live code or shared state. Count accepted operations, compare every returned beat, retain the first mismatch (address/expected/actual/mask), and expose timeout/overflow counters.

## Throughput and buffering

Theoretical payload bandwidth is transfer rate × aggregate data width / 8. User throughput is limited by refresh, row changes, read/write turnaround, arbitration, burst sizes and the controller interface. Measure accepted payload bytes per elapsed interval; distinguish write acceptance from externally completed work.

Size FIFOs for worst-case service gaps and clock-rate mismatch, not only average bandwidth. For video, compute frame storage, pixel throughput, burst packing and line buffering. For PCIe/USB, include host backpressure and transaction overhead. Record efficiency relative to the actual configured memory rate.

## Failure separation

Calibration never finishes: clock/PLL/reset/topology/constraints/power first. Calibration succeeds but all reads fail: handshake/address units/masks/ordering first. Periodic or aliased errors: lane mapping, geometry, burst addressing and width conversion. Failures only under load: FIFO overflow, arbitration, timing, power integrity or thermal margin. Do not conclude defective RAM from a single unverified example.
