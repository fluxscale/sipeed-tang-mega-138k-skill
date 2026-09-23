# Physical constraints, clocking, CDC, and timing closure

Authority: exact-package pinout and [Arora V clock guide UG306](https://cdn.gowinsemi.com.cn/UG306E.pdf), plus installed Gowin timing/physical-constraints manuals. Verify command support in the installed SDC dialect.

## CST: prove the physical mapping

For each used top-level port, review `IO_LOC`, `IO_PORT`, IO standard, bank supply, drive strength, slew and pull settings. Use the [pin-provenance procedure](board-identification.md). Confirm vector indices and differential P/N pairs. Check conflicting assignments and ports optimized away. Dedicated hard-IP pins may follow IP-specific placement rules instead of ordinary GPIO constraints.

Keep the original board-wide CST as a reference; include a reviewed subset for the design. Do not resolve a bank-voltage error by changing an IO standard until the actual hardware voltage and connected device are known. A legal tool setting can still be electrically wrong.

## Clock inventory

Build a table of root clock port/pin, physical source, frequency/tolerance, generated outputs, phase/duty cycle, consumers and reset dependencies. Trace programmable clock initialization and any mux/strap selection. Inspect PLL lock and input clock presence independently.

For each root clock, constrain the actual period. The following is an SDC illustration for a **verified 50 MHz input named `clk_in`**, not a board pin assignment:

```tcl
create_clock -name clk_in -period 20.000 [get_ports {clk_in}]
```

Check `get_ports`/`get_pins` collections resolve and reports show the expected clocks. Use generated-clock constraints or supported automatic derivation for PLL/divider outputs; avoid duplicate definitions. Recheck hierarchy paths after IP regeneration. A divided fabric signal used as a clock needs deliberate clock architecture and timing treatment; replacing it with a clock enable is often simpler.

## IO timing

Derive input/output delays from the external component's timing, board flight times/skew, and clock topology. Specify both minimum and maximum delays. Account for both edges on DDR interfaces when applicable. Source-synchronous RX and TX require their own launch/capture analysis; do not copy a system-synchronous delay template.

The timing budget should expose each term: external clock-to-out/setup/hold, board data delay, board clock delay, clock uncertainty and required phase. A nominal frequency alone does not constrain an external interface. Preserve generated DDR/PCIe/SerDes constraints and inspect which paths they cover.

## CDC and reset-domain crossings

Classify each crossing rather than adding broad asynchronous groups:

| Signal type | Typical structure | Review requirement |
| --- | --- | --- |
| Slowly changing single bit | Destination synchronizer | Metastability settling, placement, no combinational fanout from first stage |
| Event/pulse | Toggle or request/acknowledge | Event spacing, reset alignment, no loss when destination is slower |
| Multi-bit control word | Stable-data handshake | Data stable for complete transfer; synchronized control alone is insufficient |
| Streaming data | Asynchronous FIFO | Gray-pointer logic, full/empty safety, reset protocol, pointer skew constraints |
| Related generated clocks | Synchronous timing relationship | Preserve clock derivation; do not declare asynchronous solely because names differ |
| Reset release | Per-domain synchronization/IP sequence | No partial release, recovery/removal checks where applicable |

For Gray pointers, one-bit source transitions do not ensure destination observation without physical skew/delay control. Follow the supported FIFO IP constraints or derive appropriate crossing constraints; use tool-supported commands rather than importing another vendor's syntax.

An asynchronous clock-group exception can suppress more analysis than intended. Check exception precedence and retain needed max-delay/bus-skew constraints. Narrow false paths to justified structures. Every exception needs source/destination scope, a hardware reason and evidence it does not hide a real requirement.

## Timing-closure loop

1. Check constraint coverage, unconstrained endpoints, unresolved collections, derived clocks and IP constraints before believing slack.
2. Read setup and hold reports by clock pair/path group. Record worst slack and violating endpoints; include IO and recovery/removal where supported.
3. Identify logic depth versus route delay, fanout, clock skew, congestion and resource placement. Correlate the path back to RTL.
4. Make a functional change suited to the cause: pipeline, rebalance arithmetic, localize control, reduce mux depth, add buffering/replication supported by the tool, or change floorplanning after evidence.
5. Re-run implementation and protocol tests. Check latency, backpressure, resource growth and other clock domains.
6. Review hold separately; reducing clock frequency is not a general hold fix. Use supported routing/placement or IO-delay mechanisms.

Do not lower clock constraints while leaving the physical clock unchanged. Do not add arbitrary multicycle exceptions: establish the real launch/capture enable relationship and its corresponding hold treatment in the tool's model. Retain before/after reports and disclose if the achieved frequency is timing-derived but untested on hardware.
