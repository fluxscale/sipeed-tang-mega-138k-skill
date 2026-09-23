# Board identification and pin provenance

## Identity matrix

| Target | Identification starting point | Consequence |
| --- | --- | --- |
| Mega 138K Dock | Wiki overview lists GW5AST-LV138PG484A; IDE package PBG484A | Use non-Pro SOM/carrier evidence and selected B/C silicon version |
| Mega 138K Pro Dock | Wiki lists GW5AST-LV138FPG676A; IDE package FCPBG676A | Different package, larger carrier and SFP+ paths; inspect actual silicon revision |
| Tang Console 138K | Console carrier plus fitted 138K SOM | Carrier-specific clocks/peripherals/constraints; “138K” alone is insufficient |
| Custom GW5AST board | Full ordering code, schematic, BOM and actual assembled population | Re-derive power, clocks, bank assignments, flash and boot topology |

Sources: [non-Pro wiki](https://wiki.sipeed.com/hardware/en/tang/tang-mega-138k/mega-138k.html), [Pro wiki](https://wiki.sipeed.com/hardware/en/tang/tang-mega-138k/mega-138k-pro.html), [Console wiki](https://wiki.sipeed.com/tangconsole), [Gowin datasheet](https://cdn.gowinsemi.com.cn/DS1239E.pdf). This is an identification aid, not an exhaustive supported-board table.

## Known documentation traps

The non-Pro wiki has described eight transceivers in prose and four in its table; its PCIe feature, chip capability, and connector rows disagree on width/generation. Its precautions also name the Pro part while selecting the 484 package. Sipeed's family comparison and board pages have reported different maximum transceiver rates. Preserve these disagreements and resolve the actual configuration from package tables, schematics, generated IP and measured link state. Do not advertise a chip maximum as a routed or validated board interface.

“Device version” B/C is separate from PCB revision, package suffix, temperature/speed grade, and the IDE version. Inspect the physical marking and [Sipeed identification guide](https://wiki.sipeed.com/hardware/en/tang/common-doc/questions.html). A project that accepts a bitstream is not proof that the intended silicon was targeted.

Do not assume 27 MHz, 50 MHz, or a programmable clock's remembered setting. Trace the clock circuit and initialization path. Console [issue #13](https://github.com/sipeed/TangMega-138K-example/issues/13) corrects an earlier 27 MHz assumption to 50 MHz for that reported setup. It is evidence for that setup, not a universal clock assignment for all carriers.

## Pin assignment procedure

1. Identify the connector orientation, pin-1 marker, mating side and actual accessory. Numbering can mirror between connector drawings.
2. Trace the carrier signal into the board-to-board connector, then through the SOM schematic to the FPGA ball.
3. Match the ball to the exact package pinout. Check bank supply, input tolerance, IO standard support, reference voltage, direction, differential partner, and dedicated functions.
4. Check shared/multiplexed peripheral nets, straps, pull resistors, level shifters, series termination and default boot behavior. Disconnect competing drivers before driving a shared signal.
5. Compare against the nearest official CST, noting board revisions and whether dedicated IP assigns some pins without ordinary `IO_LOC` statements.
6. Record provenance in the project's pin table and constrain only the top-level ports actually in use. Review placement/IO reports after implementation.

| Logical port | Connector pin | Carrier net | SOM connector/net | FPGA ball | Bank/VCCIO | Standard/direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fill from actual design | Required | Required | Required | Required | Measured/documented | Required | Schematic revision + sheet |

GPIO headers are not a blanket statement that every bank, DDR pin, transceiver, ADC or camera signal tolerates 3.3 V. Read the connected circuit's limits. Do not connect 5 V logic directly based on a peripheral supply pin.

## Baseline capture

Keep photographs or a transcription of the markings, schematic filenames/revisions, power source, jumper/DIP settings, reference clock selection, flash markings, DDR markings, programmer identity, and peripheral cables. Record “unknown” rather than guessing. Ask for a marking/photo only if local project files and available hardware evidence cannot resolve a blocking choice.
