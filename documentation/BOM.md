```text
╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ 1                                              2                                                   3 ║
║   ╔══════════════════════════════════════════════════════════════════════════════════════════════╗   ║
║ A ║ SPECIFICATION SHEET: BILL OF MATERIALS & PROCUREMENT SCHEDULE                                ║ A ║
║   ║ CLASSIFICATION: CONFIDENTIAL / PROTOTYPE ENGINEERING                                        ║   ║
║   ╚══════════════════════════════════════════════════════════════════════════════════════════════╝   ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

# Engineering Specification: Bill of Materials & Procurement Schedule

---

## 1. Procurement Scope & Target Constraints

- Target Budget Ceiling: INR 3,800.00
- Total Reconciled Cost: **INR 3,264.00**
- Net Variance: **- INR 536.00 (Favorable / Under Budget)**
- Storage Architecture Note: No external SD card. System boots from 128MB onboard SPI NAND Flash on the Luckfox Pico Mini B. Local storage wear is eliminated; video is streamed directly via RTSP to smartphone.

---

## 2. Consolidated Bill of Materials (BOM) Schedule

| Item | Ref Des | Description / Part Number | Manufacturer / Source | Qty | Unit Cost (INR) | Total Cost (INR) | Primary Supplier |
|---|---|---|---|---|---|---|---|
| 1 | U1 | Luckfox Pico Mini B (RV1103 SoC, 64MB DDR2, 128MB SPI NAND) | Rockchip / Luckfox | 1 | 1,749.00 | 1,749.00 | ThinkRobotics / Hubtronics |
| 2 | U2 | SC3336 3MP MIPI CSI-2 Camera Module (98.3 Deg FOV) | SmartSens / Luckfox | 1 | 800.00 | 800.00 | Hubtronics / Robu.in |
| 3 | U3 | USB 2.0 Wi-Fi Dongle (RTL8188EUS 802.11n 150Mbps) | Realtek / Generic | 1 | 180.00 | 180.00 | Zbotic / Fabtolab |
| 4 | BT1 | Rechargeable LiPo Battery 3.7V 1000mAh with PCM (JST-PH 2.0mm) | Probots (KP-503450) | 1 | 340.00 | 340.00 | Probots |
| 5 | U4 | IP5306 Power Bank Management Module (2.1A Charge / 2.4A Boost) | Injoinic / Generic | 1 | 45.00 | 45.00 | Techiesms / IndiaMART |
| 6 | U5 | LM2596 DC-DC Step-Down Buck Converter Module (12V to 5V DC) | Texas Instruments / Generic | 1 | 49.00 | 49.00 | Robu.in |
| 7 | D1 | TVS Diode SMBJ5.0A (600W Transient Voltage Suppressor) | Littelfuse / Generic | 1 | 20.00 | 20.00 | Robu.in |
| 8 | C1-C4 | Ceramic Capacitors 100nF (104) 50V Radial (Pack of 10) | Murata / Generic | 1 pack | 15.00 | 15.00 | Robu.in / Local Market |
| 9 | R1-R5 | Carbon / Metal Film Resistors Assorted (100R, 10k, 470R, 1k) | Generic | 1 pack | 20.00 | 20.00 | Robu.in / Local Market |
| 10 | C5, C6 | Aluminum Electrolytic Capacitors 470uF / 25V Radial | Nichicon / Generic | 2 | 8.00 | 16.00 | Robu.in / Local Market |
| 11 | MISC | JST-PH 2.0mm 2-pin Connector Pairs and Interconnect Jumpers | Generic | 1 set | 30.00 | 30.00 | Robu.in |
| | | **TOTAL RECONCILED COST** | | | | **INR 3,264.00** | |

---

## 3. Component Technical Specifications & Engineering Roles

### Item 1 (U1): Luckfox Pico Mini B Development Board
- Processor: Rockchip RV1103 (Single-core ARM Cortex-A7 @ 1.2GHz + RISC-V Co-processor).
- Memory: Built-in 64MB DDR2 DRAM.
- Non-Volatile Storage: Onboard 128MB SPI NAND Flash (eliminates external SD card requirement).
- Video Input: 2-lane MIPI CSI-2 interface.
- Video Compression: Integrated hardware H.264/H.265 encoder block up to 1080p @ 30fps.
- Operating System: Buildroot Linux with Rockchip Media Process Interface (RKMPI) support.

### Item 2 (U2): SC3336 3MP Camera Module
- Sensor Type: 1/2.8-inch CMOS Sensor with 3MP native resolution (2304x1296).
- Pixel Size: 2.0um x 2.0um with high dynamic range and low-noise characteristics.
- Lens Specification: M12 mount, 98.3 degree diagonal field of view (FOV).
- Interconnect: 15-pin 0.5mm pitch FPC ribbon cable directly compatible with RV1103 MIPI CSI connector.

### Item 3 (U3): USB Wi-Fi Adapter (RTL8188EUS)
- Physical Protocol: USB 2.0 High-Speed Client.
- Wireless Standards: IEEE 802.11b/g/n (2.4GHz ISM band, up to 150Mbps PHY rate).
- Driver Architecture: In-tree Linux kernel driver (`8188eu`), fully supporting HostAPD Access Point (SoftAP) mode.

### Item 4 (BT1): Lithium-Polymer Battery Pack
- Nominal Voltage: 3.7V DC (Discharge plateau 3.7V, Full charge 4.2V).
- Rated Capacity: 1000mAh (3.7 Watt-hours nominal energy).
- Internal Protection Circuit Module (PCM): Overcharge cutoff (4.28V), Over-discharge cutoff (2.8V), Short-circuit protection.
- Termination: 2-pin JST-PH 2.0mm female connector.

### Item 5 (U4): IP5306 Power Management Subsystem
- Charger Architecture: Synchronous switching charger with constant current / constant voltage (CC/CV) profiles up to 2.1A.
- Boost Converter: Synchronous step-up converter supplying regulated 5.0V DC at up to 2.4A continuous.
- Load-Sharing Function: Prioritizes external DC input to run system load while simultaneously charging internal LiPo cell.
- Quiescent Workaround: Requires a static ~50mA pull (R1: 100 Ohm) to disable the default 32-second light-load auto-shutdown timer.

### Item 6 (U5): LM2596 Step-Down Buck Regulator
- Input Voltage Window: 4.5V to 40V DC (safely steps down automotive 12V/24V electrical rails).
- Output Configuration: Set to exactly 5.0V DC via multi-turn cermet potentiometer before system assembly.
- Current Capacity: Up to 3.0A peak load.

### Item 7 (D1): SMBJ5.0A Transient Voltage Suppressor (TVS)
- Standoff Voltage: 5.0V DC; Breakdown Voltage: 6.4V to 7.0V DC; Clamping Voltage: 9.2V peak.
- Peak Pulse Power Dissipation: 600W (10/1000us waveform).
- Function: Shunts high-voltage transient spikes, alternator load dump surges, and reverse polarity pulses away from downstream regulators.

### Items 8-10: Decoupling & Passive Filter Network
- C1-C4 (100nF Ceramic): Positioned adjacent to IC power pins to suppress high-frequency digital switching hash.
- C5, C6 (470uF Electrolytic): Input and output reservoir capacitance smoothing DC ripple and dampening current surges during Wi-Fi transmission bursts.
- R1 (100 Ohm / 0.25W): Static load resistor enforcing 50mA drain on IP5306 output.
- R2, R3 (10 kOhm): Pull-up/pull-down resistors for control inputs.
- R4 (470 Ohm): Forward current-limiting resistor for status LED.
- R5 (1 kOhm): USB OTG ID line pull-down securing USB Host configuration.

---

```text
╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ B                                                                                                  B ║
║   ╔══════════════════════════════════════════════════════════════════════════════════════════════╗   ║
║   ║                                               ╔══════════════════════════════════════════════╣   ║
║   ║                                               ║ PROJECT:    DASHCAM PROTOTYPE PROJECT        ║   ║
║   ║                                               ║ TITLE:      BILL OF MATERIALS SPECIFICATION  ║   ║
║   ║                                               ║ DOC NUMBER: ENG-DASH-BOM-001   REVISION: 1.4 ║   ║
║   ║                                               ║ DATE:       2026-10-08         SHEET: 1 OF 1 ║   ║
║   ║                                               ╠══════════════════════════════════════════════╣   ║
║   ║                                               ║ LEAD ENGR:  Souvik H                         ║   ║
║   ║                                               ║ REGN NO:    IN-ENG-2022-22824                   ║   ║
║   ║                                               ║ DISCIPLINE: PROCUREMENT & COMPONENT ENGR     ║   ║
║   ║                                               ║ STATUS:     APPROVED FOR FABRICATION         ║   ║
║   ║                                               ║ FORMAT:     A4 STANDARD ENGINEERING SHEET    ║   ║
║   ╚═══════════════════════════════════════════════╩══════════════════════════════════════════════╝   ║
║ 1                                              2                                                   3 ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```
