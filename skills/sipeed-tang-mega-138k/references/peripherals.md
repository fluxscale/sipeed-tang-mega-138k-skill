# Peripheral integration and diagnosis

Use the [non-Pro examples](https://github.com/sipeed/TangMega-138K-example) and [Pro examples](https://github.com/sipeed/TangMega-138KPro-example) for their respective targets. Match schematic revision and generated IP before transplanting a peripheral. The procedures below are engineering checks, not claims that every listed interface exists on every carrier.

## Video output: DVI/TMDS, HDMI connectors and RGB panels

An HDMI-shaped connector can carry a DVI-compatible TMDS implementation without audio, HDCP or the rest of HDMI. Name the implemented protocol accurately. Start with a self-contained colorbar before adding DDR/framebuffer traffic.

Specify active pixels, horizontal/vertical porches and sync widths, polarity, refresh rate and pixel clock. Calculate pixel clock from total pixels × total lines × refresh. Match serializer width and serial/parallel clock relationship to the selected implementation. Check PLL settings, supported IO mode, differential pair polarity, drive circuitry, connector direction and hot-plug/DDC behavior.

For a black screen, distinguish absent pixel clock, PLL unlock, wrong timing, output-enable/reset errors, TMDS pin assignment, cable/display compatibility and framebuffer underflow. Check sync counters and test pattern internally. [Non-Pro issue #9](https://github.com/sipeed/TangMega-138K-example/issues/9) and [Pro PLL issue #19](https://github.com/sipeed/TangMega-138KPro-example/issues/19) are leads; reopen comments and match EDA/board versions before applying advice.

For RGB panels, derive PCLK edge, DE/HS/VS requirements, bus width, color ordering and backlight supply/enable from the panel datasheet. Do not equate a panel's resolution with its full timing mode. Start with static color planes to reveal swapped bits/channels.

For framebuffers, calculate bytes per line/frame, stride and burst alignment; design clock crossings and buffering around worst-case DDR service gaps. Count underflows and frame drops. A black or repeated frame may be a buffer-ownership problem even when memory passes a standalone test.

## DVP and MIPI cameras

Identify sensor, power rails, reset/power-down polarity, master clock and register-control bus before receiving pixels. Confirm configuration success through a readable sensor ID/register, then use a sensor test pattern where available. Decode pixel format, byte order, line/frame markers and any blanking words.

DVP uses a parallel pixel bus with a pixel clock; MIPI CSI-2 uses lane signaling, a D-PHY and packet protocol. They are not interchangeable. For MIPI, verify whether the package exposes the required hard PHY or whether a supported soft implementation is intended; check lane count/mapping, clock mode, lane rate, LP/HS transitions, packet data type, virtual channel, ECC and CRC. Do not infer MIPI capability solely from a family feature table.

Use bounded line/frame counters and overflow statistics to isolate sensor configuration, capture timing, clock-domain crossing and video-output issues. Read the corresponding example and [issue #8](https://github.com/sipeed/TangMega-138K-example/issues/8) as a report of a symptom, not a known general cause.

## Ethernet: PHY, RGMII and UDP

Determine PHY model, reset/strap values, MDIO address, reference clock and internal delay configuration from the actual schematic/datasheet. RGMII timing depends on where TX/RX clock skew is introduced; enabling delay at both ends or neither can break a link. Constrain the chosen arrangement from the PHY timing requirements.

Read PHY identity and negotiated link state when MDIO is available. Then check received/transmitted frame counters, CRC errors and packet captures. A carrier link LED is not proof that the FPGA MAC or UDP implementation works. Examples may use fixed MAC/IP/UDP values and may not implement ARP, ICMP, DHCP or a full network stack.

Start on an isolated test network with known addresses and a packet capture. Verify Ethernet framing, minimum frame size/padding, FCS handling, IP/UDP lengths and checksums, byte order and MTU. Separate “no packets emitted” from “host drops malformed packets.” [Pro issue #20](https://github.com/sipeed/TangMega-138KPro-example/issues/20) is a relevant upstream symptom report.

## USB and CH569

Identify which connector reaches the debugger MCU, CH569, FPGA soft USB, or another controller. Power/data capabilities differ. A USB3 connector does not mean the FPGA implements a native USB3 PHY.

For the [CH569 example](https://github.com/sipeed/TangMega-138K-example/tree/main/ch569_hspi2cdc), treat FPGA HSPI logic and CH569 firmware as a versioned pair. Verify bus width, strobe/clock edges, direction changes, flow control, DMA ownership, buffer alignment and firmware endpoint configuration. Test one direction, then bidirectional traffic with backpressure; count dropped/duplicated words and end-to-end payload rate. Firmware flashing is separate from FPGA SRAM loading.

For [Pro soft USB](https://github.com/sipeed/TangMega-138KPro-example/tree/main/usb2_soft), verify IO/PHY circuit assumptions and the implemented USB speed/class. Use enumeration/descriptors and bounded loopback transfers before application traffic. A UART bridge through the debugger is not the FPGA's USB application path.

## Audio, SD, GPIO, fan and LEDs

| Interface | Resolve first | Discriminating test |
| --- | --- | --- |
| I2S/audio codec | Master/slave clocks, MCLK/BCLK/LRCLK ratios, word length, I2S vs justified framing, codec registers | Low-amplitude tone and capture; inspect one-bit alignment and channel order |
| SD | SPI vs SDIO mode, routed data lines, voltage, card initialization and response timing | Read a known block before filesystem work; do not overwrite user media for a bring-up test |
| I2C | Pull-ups/supply, open-drain behavior, address format, clock stretching and bus sharing | Bounded register read of the identified device, not indiscriminate writes |
| UART | Actual source clock, baud divider, voltage, direction and polarity | Known repeated byte pattern; distinguish debugger firmware issues from FPGA divider errors |
| Buttons/LEDs | Active polarity, pull resistors, debounce and shared nets | Clocked counter plus synchronized button status |
| WS2812 | Device timing, level requirements, bit order and reset/latch interval | One pixel, known low-brightness colors; scope timing |
| Fan | Supply, open-drain/push-pull expectation, PWM and tachometer circuit | Verify safe startup and tach count; inspect board-specific errata |

## ADC and power/thermal observations

Identify the ADC instance (on-chip vs external), input network, reference, common-mode range, sample clock and calibration before suggesting measurement code. Never treat an FPGA ADC pin as a generic voltage-tolerant input. Apply a known in-range test signal and compare codes using the actual resolution/reference and analog scaling.

For load-dependent errors, correlate rail behavior, temperature and reset events with traffic. Preserve cooling and record ambient/workload/duration. Tool power estimates are not measured board power, and a passing room-temperature test does not establish operating-range margin.
