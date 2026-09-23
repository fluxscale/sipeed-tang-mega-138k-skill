# Toolchains, project structure, and IP migration

## Choose a complete path

The vendor flow is the baseline for complex GW5AST IP. Determine device support in the installed EDA edition, release, license and IP catalog. Support and licensing have changed over time: do not repeat historical claims that 138K is categorically unsupported in educational editions. Verify current requirements through the [board wiki](https://wiki.sipeed.com/hardware/en/tang/tang-mega-138k/mega-138k.html), vendor release notes and installed device selector. Avoid freezing public floating-license IP addresses into a project.

For an open-source request, establish all of: RTL frontend/synthesis mapping, exact device database, package and silicon version, nextpnr backend, primitive coverage, constraints handling, packing, and programming. A successful blinker proves a narrow path. It does not prove DDR3, PCIe, SerDes or AE350 support.

Research leads show incremental GW5AST-138C work: [nextpnr #1631](https://github.com/YosysHQ/nextpnr/pull/1631), [Apicula clock support #437](https://github.com/YosysHQ/apicula/pull/437), [BSRAM #463](https://github.com/YosysHQ/apicula/pull/463), [IO #464](https://github.com/YosysHQ/apicula/pull/464), and [reset handling #466](https://github.com/YosysHQ/apicula/pull/466). Recheck merged status, release inclusion and required companion commits before choosing versions. Do not call the family universally unsupported, or treat these PRs as complete device support.

## Inspect before building

Inventory `.gprj`, `.v/.sv/.vhd`, `.cst`, `.sdc`, Tcl, IP configuration/generated wrappers, initialization files, simulation models, scripts and submodules. Inspect the top module, synthesis language, include paths, macros, file order, target part/version, speed grade and enabled options. Keep case-sensitive paths valid on Linux.

```sh
rg --files -g '*.gprj' -g '*.cst' -g '*.sdc' -g '*.tcl' -g '*.v' -g '*.sv' -g '*.vhd'
rg -n 'Device|Part|TopModule|IO_LOC|IO_PORT|create_clock|PLL|PLL_INIT|FCLKIN' .
git submodule status
```

Read existing Tcl or export a script from the installed IDE. Discover executable paths and CLI syntax from that release's help/SUG100. Do not invent command-line flags or claim a sample Tcl sequence works across releases. Build from a clean output directory while preserving sources, IP settings and the last known-good artifacts.

Capture full logs and synthesis/placement/timing reports. Fail the build on actual tool failure and missing expected artifacts; wrappers can return success despite an incomplete downstream step. Record build seed/options and hash the bitstream.

## Reproducible project contract

A deliverable should include the exact target, source list/top, constraints, IP regeneration inputs, simulator setup, documented build invocation, and necessary memory initialization files. Separate generated build products from generated IP needed by the tool. Do not blindly ignore every generated HDL/netlist if it is required to reproduce the design.

A firmware-plus-FPGA project also needs compiler/SDK version, linker script, boot layout and a description of which image configures which subsystem. State which vendor files cannot legally be redistributed and how the owner obtains them.

## Migration procedure

1. Build the untouched baseline using its documented version if available. Preserve logs, source commit and output hash.
2. Duplicate the project in an isolated working directory. Record the destination package, silicon version and tool build.
3. Open each device-dependent IP configuration in the target generator. Regenerate the wrapper, implementation, simulation files and constraints as a set.
4. Diff ports, reset polarity, clock ratios, latency, bus width, address units, primitive parameters and auxiliary initialization modules. Update instantiations intentionally.
5. Check the source list for duplicate old/new modules and obsolete generated constraints. Re-run simulation and implementation; compare resource use, clock reports and slack.
6. Run the smallest corresponding hardware test, then the application's real workload. Keep rollback artifacts.

For PLLs, recompute using the installed generator and UG306; a patch to divisor encodings from an issue is version-specific. For DDR3, preserve dynamic PLL/calibration/initialization arrangements. For SerDes, preserve generated collateral (including configuration files) and documented reset sequencing.

## Resource and performance investigation

Compare inferred vs expected BSRAM, LUTRAM, DSP and register counts. A large resource jump after a minor RTL change usually deserves inspection of signedness, synchronous memory inference, reset fanout, mux topology or missed DSP mapping. Separate logical utilization from placement congestion and clock/IO resource limits. Pipeline based on timing reports, then recheck latency and throughput contracts.
