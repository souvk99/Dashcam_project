```text
╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ 1                                              2                                                   3 ║
║   ╔══════════════════════════════════════════════════════════════════════════════════════════════╗   ║
║ A ║ SPECIFICATION SHEET: SYSTEM REQUIREMENTS SPECIFICATION (SRS)                                 ║ A ║
║   ║ CLASSIFICATION: CONFIDENTIAL / PROTOTYPE ENGINEERING                                        ║   ║
║   ╚══════════════════════════════════════════════════════════════════════════════════════════════╝   ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

# Engineering Specification: System Requirements Specification (SRS)

---

## 1. Project Engineering Scope & Boundary

This specification establishes the definitive baseline requirements for a self-contained automotive vision sensor prototype designed to capture, hardware-compress, and stream video wirelessly to a mobile device.

Primary Engineering Boundaries:
- Bill of Materials Ceiling: INR 3,800.00 max (Target Reconciled: INR 3,264.00).
- Zero External Storage Architecture: Operation completely from 128MB onboard SPI NAND Flash (no MicroSD card).
- Video Latency & Stability: Real-time H.264 video delivered with zero frame drops or buffer stutters.
- Vehicle Electrical Interface: Automotive 12V DC input with transient suppression and load-sharing power bank subsystem.

---

## 2. Functional Requirements Matrix

| Requirement ID | Requirement Description | Verification Method | Acceptance Criteria | Engineering Implementation |
|---|---|---|---|---|
| FR-01 | Stream continuous H.264 compressed video over local Wi-Fi without frame stutter | Test / Measurement | 30.0 fps sustained, zero dropped frames over 30 min | Rockchip RV1103 Hardware VPU Encoder |
| FR-02 | Minimum native video resolution | Inspection | 1920 x 1080 (1080p Full HD) | SmartSens SC3336 3MP Sensor + ISP 3.2 |
| FR-03 | Zero external SD card dependency for system boot and runtime execution | Demonstration | Successful system cold boot with SD slot empty | 128MB SPI NAND Flash (Luckfox Mini B) |
| FR-04 | Wireless local point-to-point network connectivity (SoftAP) | Test | Mobile phone associates directly without router | RTL8188EUS USB Wi-Fi (HostAPD 802.11n) |
| FR-05 | Battery-buffered autonomous operation during engine cut-off | Test / Timing | Greater than 60 minutes continuous streaming | 3.7V 1000mAh LiPo Pack with PCM Protection |
| FR-06 | Simultaneous vehicle power pass-through and battery recharge | Test / Current Probe | Battery charges while system operates normally | IP5306 Synchronous PMIC with Load-Sharing |
| FR-07 | Automotive electrical transient and overvoltage protection | Test / Surge Spike | Clamps inductive spikes up to 40V safely | SMBJ5.0A TVS Diode + 470uF Bulk Reservoir |
| FR-08 | Power management auto-sleep inhibition circuit | Inspection / Test | PMIC maintains continuous output regardless of load | 100 Ohm Resistor (R1) static ~50mA pull |
| FR-09 | Wide-angle forward optical field of view | Optical Measurement | Diagonal FOV greater than 95.0 degrees | 98.3 degree wide-angle lens assembly |
| FR-10 | Visual hardware status indication | Inspection | Continuous optical indication of streaming state | GPIO driven Status LED via 470 Ohm resistor |

---

## 3. Non-Functional Performance & Environmental Metrics

| Metric ID | Performance Metric | Specification Limit | Verification Technique |
|---|---|---|---|
| NFR-01 | Total Bill of Materials Cost | Less than INR 3,800.00 (Actual: INR 3,264.00) | Procurement reconciliation audit |
| NFR-02 | Cold Boot Duration to Video Stream | Less than 6.0 Seconds from cold power applied | Logic analyzer / Serial timestamp measurement |
| NFR-03 | End-to-End Glass-to-Glass Latency | Less than 250 Milliseconds | High-speed stopwatch camera comparison |
| NFR-04 | Ambient Operating Temperature Envelope | 0 Deg C to 45 Deg C (Non-condensing) | Environmental chamber operational soak |
| NFR-05 | Maximum Physical Enclosure Envelope | 70 mm (L) x 45 mm (W) x 30 mm (H) | Digital caliper mechanical envelope check |

---

## 4. Architectural Exclusions & Scope Baseline

- Local High-Capacity Recording: Local storage of historical video clips is intentionally excluded to eliminate SD card cost, write-cycle degradation, and bus contention.
- Client-Side Archival: Any required video recording is delegated to the client mobile application (e.g. VLC Media Player recording function).

---

```text
╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ B                                                                                                  B ║
║   ╔══════════════════════════════════════════════════════════════════════════════════════════════╗   ║
║   ║                                               ╔══════════════════════════════════════════════╣   ║
║   ║                                               ║ PROJECT:    DASHCAM PROTOTYPE PROJECT        ║   ║
║   ║                                               ║ TITLE:      SYSTEM REQUIREMENTS (SRS)        ║   ║
║   ║                                               ║ DOC NUMBER: ENG-DASH-REQ-001   REVISION: 1.4 ║   ║
║   ║                                               ║ DATE:       2026-10-08         SHEET: 1 OF 1 ║   ║
║   ║                                               ╠══════════════════════════════════════════════╣   ║
║   ║                                               ║ LEAD ENGR:  Souvik H                         ║   ║
║   ║                                               ║ REGN NO:    IN-ENG-2022-22824                   ║   ║
║   ║                                               ║ DISCIPLINE: SYSTEMS ENGINEERING              ║   ║
║   ║                                               ║ STATUS:     RELEASED FOR DESIGN EXECUTION    ║   ║
║   ║                                               ║ FORMAT:     A4 STANDARD ENGINEERING SHEET    ║   ║
║   ╚═══════════════════════════════════════════════╩══════════════════════════════════════════════╝   ║
║ 1                                              2                                                   3 ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```
