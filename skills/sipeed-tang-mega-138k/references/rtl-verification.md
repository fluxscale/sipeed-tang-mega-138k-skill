# RTL design, resource mapping, and verification

## Design around explicit contracts

Write down clock domains, reset behavior, data widths, throughput, latency, backpressure and overflow policy before implementing a datapath. At every boundary specify whether addresses count bytes, words or beats and whether lengths include the final transfer. Parameterized modules need supported parameter ranges and valid behavior at minimum widths/depths.

For ready/valid interfaces, count a transfer only when both are asserted on the specified edge. Keep data and sidebands stable while stalled. Do not couple independent command/data channels unless the IP interface explicitly requires it. Define packet/frame boundaries, partial-byte masks, and behavior if reset occurs during a transaction.

For arithmetic, specify signed operands, intermediate widths, rounding, truncation and saturation. Check negative extremes, carry growth and multiply-accumulate width. Inspect synthesis mapping into GW5AST DSP resources rather than estimating physical usage from the count of `*` operators. Pipeline stages change external latency even when steady-state throughput is unchanged.

## Memory inference

Consult the installed Arora V BSRAM/SSRAM guide and synthesis report for supported read latency, port modes, byte enables and read-during-write behavior. A behavioral array does not establish a physical dual-port RAM with the desired semantics.

- Prefer a supported synchronous memory coding pattern when BSRAM is intended.
- Clearing every word on reset can force a RAM into registers. Reset validity/metadata or initialize through a bounded scrub sequence where the application permits it.
- Verify initialization file format, path resolution, size and bit/byte order in simulation and implementation.
- Define same-address simultaneous access and cross-port collision behavior. If unspecified by the primitive, prevent it architecturally.
- Derive logical capacity from actual usable width/depth, including parity/ECC configuration; raw memory bits are not automatically user payload bits.

## Clocks and resets in RTL

Use clock enables for low-rate logic instead of fabric-generated gated clocks. Use dedicated clocking resources for intentional clock generation or muxing. Synchronize asynchronous reset release separately in each clock domain and preserve any IP-specific assertion/deassertion requirements. Do not release a dependent interface merely because an unrelated PLL reports lock.

Mechanical buttons need synchronization and debounce. Synchronizers are not debouncers. Pulse signals require pulse capture/toggle/handshake logic when the destination may miss a narrow source pulse. Read [CDC guidance](constraints-timing.md) for multi-bit crossings.

## Verification ladder

1. **Elaboration/lint:** missing modules, parameter limits, width/signedness mistakes, multiple drivers, latches, unused/undriven ports and implicit nets. Classify warnings instead of globally suppressing them.
2. **Unit simulation:** known boundary values, reset during activity, maximum/minimum lengths, sustained stalls, simultaneous read/write and wraparound. Use assertions and scoreboards tied to externally visible behavior.
3. **Integration simulation:** generated IP models with the required simulator; initialize memories and clocks realistically. Do not replace a vendor block with a simplistic model and call the complete subsystem validated.
4. **Formal checks where useful:** FIFO ordering/occupancy, no duplication or loss, arbitration, address bounds and protocol stability under stalls. Check assumptions for vacuity. Functional formal proof does not establish analog CDC reliability or board timing.
5. **Implementation:** resource mapping, timing coverage, setup/hold, clock routing, IO checks and unconstrained paths.
6. **Hardware:** deterministic counters/patterns, explicit pass/fail/timeout, reproducible capture conditions and workload duration. Preserve raw evidence.

Use [Verilator](https://verilator.org/guide/latest/) or [Icarus](https://github.com/steveicarus/iverilog) for compatible fabric RTL, [cocotb](https://docs.cocotb.org/en/stable/) for transaction-level scoreboards, and [SymbiYosys](https://symbiyosys.readthedocs.io/en/latest/) for suitable formal tasks. Check installed flags and language/model support. Vendor simulation libraries and encrypted IP may require a supported commercial simulator.

## Useful assertions and observations

Test that accepted writes eventually produce the documented observable effect; accepted reads yield exactly the expected responses; stalled outputs remain stable; queue occupancy stays in range; packet lengths match accepted bytes; and reset leaves no stale transaction treated as valid. For bounded liveness checks, define a fair environment or an explicit timeout so the property is meaningful.

Hardware instrumentation should expose event counts, first error address/expected/actual data, sticky fault flags, maximum queue occupancy, reset count and state transitions. Capture the first fault before repeated traffic overwrites it. A logic analyzer samples one clock domain; synchronize cross-domain status or use separate captures.

## Porting from other FPGA vendors

Replace PLL/MMCM, clock buffers, IO SERDES, RAM, DSP and debug primitives through deliberate wrappers. Re-derive reset polarity, registered output latency, memory collision behavior and clock relationships. Do not translate an XDC/QSF constraint mechanically into CST/SDC without reviewing the target's physical and timing model. Keep portable protocol logic separate from vendor-specific wrappers.
