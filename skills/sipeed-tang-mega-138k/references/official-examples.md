# Official example navigation and baseline selection

Inspected 2026-09-23 through the repositories' trees and selected project files. Paths below are relative to their respective checkout. A path's presence establishes availability, not that it compiles or works on the user's board.

## Non-Pro: sipeed/TangMega-138K-example

Primary repository: [sipeed/TangMega-138K-example](https://github.com/sipeed/TangMega-138K-example).
Inspected commit: [`06e7d8b118d345915ab6f257b7c22226f81575cd`](https://github.com/sipeed/TangMega-138K-example/tree/06e7d8b118d345915ab6f257b7c22226f81575cd).

| Need | Project path at the inspected commit |
| --- | --- |
| GPIO/PMOD baseline | `pmod_led/eda_proj/eda_proj.gprj` |
| DDR3 with UART observations | `ddr_memory/ddr_memory_test_uart/ddr3_1v4_hs.gprj` |
| PCIe configuration alternatives | `pcie_dma_demo/pcie_gen2(5G)/pcie_dma_demo.gprj`, `pcie_dma_demo/pcie_gen3(8G)/pcie_dma_demo.gprj` |
| DVI colorbar / video pipeline | `hdmi_colorbar/eda_proj/hdmi.gprj`, `hdmi_svo/eda_proj/hdmi.gprj` |
| Camera to DVI | `cam_dvi/cam2dvi/cam2dvi.gprj` |
| DVP camera to RGB | `dvp_rgb/ov5640_480_272/ov5640_480_272.gprj` |
| RGB LCD | `lcd_rgb666_screen/eda_proj/eda_proj.gprj` |
| CH569 HSPI | `ch569_hspi2cdc/CH569_HSPI_FPGA/CH569_HSPI_FPGA.gprj` |
| CH569 alternate/reverse FPGA projects | `ch569_hspi2cdc/usb3_ch569_hspi_fpga/fpga/CH569_HSPI_FPGA.gprj`, `CH569_HSPI_FPGA_reverse.gprj` in the same directory |
| RGMII/UDP | `udp_rgmii_send/eda_proj/udp_rgmii_send.gprj` |
| Audio | `audio_i2s/eda_proj/audio.gprj` |
| SD / fan / addressable LED | `sd_card/eda_proj/eda_proj.gprj`, `pwm_fan/eda_proj/eda_proj.gprj`, `ws2812/eda_proj/ws2812.gprj` |
| Controller interface | `joycon/Joycon.gprj` |

The [inspected DDR project](https://github.com/sipeed/TangMega-138K-example/blob/06e7d8b118d345915ab6f257b7c22226f81575cd/ddr_memory/ddr_memory_test_uart/ddr3_1v4_hs.gprj) explicitly selects `GW5AST-138C` and `GW5AST-LV138PG484AC1/I0`. Its source list includes the DDR wrapper, two PLL-related modules, `pll_init.v`, a UART FIFO/path, CST and SDC. Preserve that integration when reproducing this baseline; changing only the device dropdown is not sufficient evidence of a correct B-version port.

Inspect `.gitmodules` for linked projects and their pinned commits. A downloaded archive may omit submodule contents. Do not recursively fetch or run third-party submodule scripts without first inspecting the needed dependency.

## Pro: sipeed/TangMega-138KPro-example

Primary repository: [sipeed/TangMega-138KPro-example](https://github.com/sipeed/TangMega-138KPro-example).
Inspected commit: [`d3cebf1703f1bcd06dca8a53bf2b660c86a5ec16`](https://github.com/sipeed/TangMega-138KPro-example/tree/d3cebf1703f1bcd06dca8a53bf2b660c86a5ec16).

| Need | Project path at the inspected commit |
| --- | --- |
| Basic LED / buttons | `led/led.gprj`, `key_led/key_led.gprj` |
| DDR vendor-specific configurations | `ddr_test/Hynix_400MHz/ddr3_1v4_hs.gprj`, `ddr_test/Micron_400MHz/ddr3_1v4_hs.gprj` |
| DDR UART test | `pro_ddr_test/ddr_test_uart.gprj` |
| AE350 fabric integration | `ae350_customized_demo/ae350_customized_demo.gprj` |
| Custom PHY rates | `sfp+/customized_phy/1.25G/fpga_project.gprj`, `sfp+/customized_phy/10.3125G/fpga_project.gprj`, `sfp+/customized_phy/12.5G/fpga_project.gprj` |
| Serial Ethernet example | `sfp+/10G_Serial_Ethernet/XGbE_UDP/XGbE_UDP.gprj` |
| Video output | `simple_video_out/svo/hdmi.gprj` |
| Camera to DVI | `cam2hdmi_alt/cam2dvi/cam2dvi.gprj` |
| RGB panels | `rgb_screen/480_272_screen/480_272_screen.gprj`, `rgb_screen/800_480_screen/800_480_screen.gprj` |
| Audio | `audio/audio_music/audio_music.gprj`, `audio/audio_sinewave/audio.gprj` |
| Ethernet | `udp_rgmii_send/udp_rgmii_send.gprj` |
| Soft USB loopback / streaming | `usb2_soft/usb_uart_loopback/usb_uart_loopback.gprj`, `usb2_soft/usb_cy_bulkloop/cy_usb_bulkloop.gprj`, `usb2_soft/usb_cy_streamer/usb_refdesign.gprj` |

The [inspected AE350 project](https://github.com/sipeed/TangMega-138KPro-example/blob/d3cebf1703f1bcd06dca8a53bf2b660c86a5ec16/ae350_customized_demo/ae350_customized_demo.gprj) selects `GW5AST-138B` / `GW5AST-LV138FPG676AC1/I0`. Its source list includes an AHB-to-DDR integration module, read/write FIFOs, separate AE350/DDR PLL wrappers and the generated SoC wrapper. Use this to locate the integration boundary; inspect the RTL/manual before assuming bus semantics.

The [inspected Pro DDR UART project](https://github.com/sipeed/TangMega-138KPro-example/blob/d3cebf1703f1bcd06dca8a53bf2b660c86a5ec16/pro_ddr_test/ddr_test_uart.gprj) selects `GW5AST-138B` / `GW5AST-LV138FPG676AES`. That is not the same part string as the AE350 example. Do not generalize a repository-wide target from either file. Folder labels such as `400MHz` and `12.5G` are configuration hints, not measurements of the user's hardware.

The Pro PCIe material is under `pcie_dma_demo`; inspect its README and distributed artifacts rather than inventing a `.gprj` path based on the non-Pro tree.

## Adaptation checklist

Before copying an example, compare its `.gprj` device and source list, actual CST pin/bank settings, SDC/root clocks, generated IP settings, physical peripheral population, reset/power sequencing, and companion host/MCU/processor software. Build and test the baseline first when available. If it fails, search its own issues before changing several subsystems.

When delivering a port, state the baseline commit and list deliberate changes: target selection, regenerated IP, pin mapping, clock configuration, software pairing and tests. Never describe a project as a drop-in Console port solely because it uses PG484.
