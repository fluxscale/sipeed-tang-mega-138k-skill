# Programming, cold boot, and recovery

Sources: the exact board wiki, [Sipeed debugger guide](https://wiki.sipeed.com/hardware/en/tang/common-doc/update_debugger.html), installed Gowin Programmer documentation, UG704 and [openFPGALoader](https://github.com/trabucayre/openFPGALoader). Operation names and support vary with versions; inspect installed help and board definitions.

## Identify the operation

| Operation | Effect | Evidence needed |
| --- | --- | --- |
| Detect JTAG chain | Reads identities; may reset/affect a running target depending on tool | Intended cable/device and access to hardware |
| SRAM configuration | Replaces active FPGA logic until reconfiguration/power loss | Matching bitstream target, IO behavior and physical setup |
| External flash programming | Changes persistent boot contents | Flash type/capacity, image format/offset, erase scope and recovery plan |
| Debugger MCU firmware update | Alters the USB/JTAG bridge | Correct debugger generation and update procedure |
| OTP/security/encryption configuration | May irreversibly change device behavior/access | Explicit task scope and exact vendor procedure |

Read-only discovery is not the same as leaving a running device undisturbed. Coordinate with the user's stated hardware-use constraints. SRAM loading is volatile but can immediately drive external pins; verify the design and connected hardware first.

## First bring-up sequence

1. Identify power input and enabled rails, power-switch state, SOM/carrier revision and cable path. Use the carrier's instructions; a USB connector's role cannot be inferred from its shape.
2. Confirm the OS detects the debugger and the programmer selects that device, especially with multiple boards attached.
3. Inspect the JTAG chain and compare identity/package/revision evidence. If unreliable, check cable, driver/permissions, reset state, power and a supported lower JTAG frequency before blaming the bitstream.
4. Build a minimal, matching design with a verified clock and observable GPIO/UART behavior. Load SRAM using the operation supported by the installed programmer.
5. Check expected behavior with a bounded test. Preserve the log, artifact hash and measured result.
6. Only when persistent boot is requested, identify flash details and write the intended region using the correct bridge/operation. Verify using supported readback/verification, then perform a documented cold-boot test.

For openFPGALoader, begin with its installed `--help`, board list and definitions; do not guess a board alias from a product name. Confirm device support and SRAM versus flash support independently. [GW5AST support PR #364](https://github.com/trabucayre/openFPGALoader/pull/364) and [GW5A flash issue #389](https://github.com/trabucayre/openFPGALoader/issues/389) are historical leads, not a current support guarantee.

## Flash-specific checks

Read the physical flash marking/JEDEC identity where supported, capacity, sector geometry and boot mode. Distinguish Mbit from Mbyte. Verify file size against the actual configuration region, not just total chip capacity. Compression, image format, headers and multiple images affect the stored size/layout.

Some board revisions have different flash populations; never “fix” a programming failure by choosing a larger flash model without evidence. Determine whether FPGA configuration, processor firmware or user data share a chip. Preserve necessary contents if the task requires retaining them. Avoid full-chip erase when the authorized update targets a smaller region.

A successful write can still fail at boot due to wrong offset/format, boot straps, flash mode, image size, startup clock/reset dependencies or programmer operation. Test power removal/reapplication, not just a soft reconfiguration, when claiming cold-boot success.

## Failure decision tree

- **No USB device:** power/data cable, connector role, host port and debugger state.
- **USB visible, programmer cannot open it:** correct interface/driver, permissions and competing process.
- **Cable open, no stable JTAG identity:** FPGA power/reset, chain configuration, cable integrity and JTAG rate.
- **Identity found, configuration rejected:** exact target/silicon, file format, programmer support and bitstream integrity.
- **SRAM load succeeds, no behavior:** actual clock/reset, pin/polarity, target match and whether the design executes the expected test.
- **SRAM works, flash operation fails:** supported bridge/mode, flash identity/size, erase/program algorithm and tool version.
- **Flash verifies, cold boot fails:** boot selection, image layout, startup sequencing and power integrity.

Do not repeatedly retry an erase/program operation without changing an evidence-based cause. Stop when identity/erase scope is uncertain or verification fails, preserve logs and choose a discriminating diagnostic. Firmware updates and host driver changes should follow identified need and the user's authorized scope.
