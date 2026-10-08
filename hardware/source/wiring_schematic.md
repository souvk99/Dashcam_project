```text
╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ 1                                              2                                                   3 ║
║   ╔══════════════════════════════════════════════════════════════════════════════════════════════╗   ║
║ A ║ SPECIFICATION SHEET: ELECTRICAL WIRING & INTERCONNECT SCHEMATIC                              ║ A ║
║   ║ CLASSIFICATION: CONFIDENTIAL / PROTOTYPE ENGINEERING                                        ║   ║
║   ╚══════════════════════════════════════════════════════════════════════════════════════════════╝   ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

# Engineering Specification: Electrical Wiring & Interconnect Schematic

---

## 1. Primary Power Conditioning & Transient Suppression Stage

```text
[+12V DC Vehicle In] ───┬───────────────────────────────────────┐
                        │                                       │
                      [ D1 ] SMBJ5.0A TVS (Cathode)            [ C5 ] 470uF / 25V (Electrolytic +)
                        │                                       │
[Vehicle Ground (-)] ───┴───────────────────────────────────────┴───► [LM2596 VIN (-)]
[+12V DC Vehicle In] ────────────────────────────────────────────────► [LM2596 VIN (+)]

                                     LM2596 BUCK REGULATOR
                                 (Trim pot adjusted to +5.0V)
                                     
[LM2596 VOUT (+5V)] ──┬─────────────────┬───────────────────────────► [IP5306 VIN (+5V)]
                      │                 │
                    [ C6 ] 470uF      [ C4 ] 100nF (104)
                    (Electrolytic +)  (Ceramic)
                      │                 │
[LM2596 VOUT (GND)] ──┴─────────────────┴───────────────────────────► [IP5306 GND]
```

---

## 2. Battery Storage & Power Management Subsystem (IP5306)

```text
[1000mAh LiPo Cell (+)] ────────────────────────────────────────────► [IP5306 BAT (+)]
[1000mAh LiPo Cell (-)] ────────────────────────────────────────────► [IP5306 BAT (-)]

                                     IP5306 PMIC MODULE
                                     
[IP5306 5V OUT (+)] ──┬───────────────┬─────────────────────────────► Main +5.0V System Rail
                      │               │
                    [ R1 ] 100 Ohm  [ C1 ] 100nF (104)
                    (Keep-alive     (Ceramic decoupling)
                     50mA load)       │
                      │               │
[IP5306 GND] ─────────┴───────────────┴─────────────────────────────► Main Ground Rail
```

---

## 3. System Rail Distribution & Subsystem Decoupling

```text
Main +5.0V Rail ──┬─────────────────────────────────────────────────► [Luckfox Pico Mini B 5V Pin]
                  │
                [ C2 ] 100nF (104) Ceramic Decoupling
                  │
Main Ground     ──┴─────────────────────────────────────────────────► [Luckfox Pico Mini B GND Pin]

Main +5.0V Rail ──┬─────────────────────────────────────────────────► [USB Wi-Fi Port Pin 1 (VBUS)]
                  │
                [ C3 ] 100nF (104) Ceramic Decoupling
                  │
Main Ground     ──┴─────────────────────────────────────────────────► [USB Wi-Fi Port Pin 4 (GND)]
```

---

## 4. Signal Interconnects & Peripheral Pin Mapping

### A. Camera Module (SC3336) Interconnect
- Interconnect Interface: 15-pin 0.5mm pitch FPC flexible printed circuit cable.
- Termination: Directly into the MIPI CSI connector on the Luckfox Pico Mini B board.
- Pin Configuration: Differential Data Lane 0 (+/-), Data Lane 1 (+/-), Differential Clock (+/-), I2C SCCB lines (SDA/SCL), and 3.3V/1.8V power feeds.

### B. Wireless USB Network Adapter (RTL8188EUS)
- Pin 1 (VBUS): Connected to Main +5.0V Rail (decoupled via C3 100nF).
- Pin 2 (D-): Connected to Luckfox USB High-Speed Data Negative line.
- Pin 3 (D+): Connected to Luckfox USB High-Speed Data Positive line.
- Pin 4 (GND): Connected to Main System Ground.
- Resistor R5 (1 kOhm): Pull-down connected to USB OTG ID line, forcing USB Host negotiation.

### C. Visual Indication & User Control Hardware
- Optical Status LED: Luckfox GPIO48 ---> [ R4: 470 Ohm ] ---> [ LED Anode (+) ] ---> [ LED Cathode (-) to System GND ].
- Master Control Push-Button: Luckfox GPIO Pin ---> Momentary Switch to System GND, with [ R2: 10 kOhm ] pull-up to 3.3V DC rail.
- Hardware Mode Latch Pin: Luckfox GPIO Pin ---> [ R3: 10 kOhm ] pull-down to System GND.

---

```text
╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ B                                                                                                  B ║
║   ╔══════════════════════════════════════════════════════════════════════════════════════════════╗   ║
║   ║                                               ╔══════════════════════════════════════════════╣   ║
║   ║                                               ║ PROJECT:    DASHCAM PROTOTYPE PROJECT        ║   ║
║   ║                                               ║ TITLE:      ELECTRICAL WIRING & SCHEMATIC    ║   ║
║   ║                                               ║ DOC NUMBER: ENG-DASH-SCH-001   REVISION: 1.4 ║   ║
║   ║                                               ║ DATE:       2026-10-08         SHEET: 1 OF 1 ║   ║
║   ║                                               ╠══════════════════════════════════════════════╣   ║
║   ║                                               ║ LEAD ENGR:  Souvik H                         ║   ║
║   ║                                               ║ REGN NO:    IN-ENG-2022-22824                   ║   ║
║   ║                                               ║ DISCIPLINE: ELECTRICAL WIRING & INTERCONNECT ║   ║
║   ║                                               ║ STATUS:     RELEASED FOR BENCHTOP ASSEMBLY   ║   ║
║   ║                                               ║ FORMAT:     A4 STANDARD ENGINEERING SHEET    ║   ║
║   ╚═══════════════════════════════════════════════╩══════════════════════════════════════════════╝   ║
║ 1                                              2                                                   3 ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```
