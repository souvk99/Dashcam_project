```text
╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ 1                                              2                                                   3 ║
║   ╔══════════════════════════════════════════════════════════════════════════════════════════════╗   ║
║ A ║ SPECIFICATION SHEET: ARCHITECTURE DECISION RECORDS (ADR)                                     ║ A ║
║   ║ CLASSIFICATION: CONFIDENTIAL / PROTOTYPE ENGINEERING                                        ║   ║
║   ╚══════════════════════════════════════════════════════════════════════════════════════════════╝   ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

# Engineering Specification: Architecture Decision Records (ADR)

---

## ADR-001: Platform Selection — Rockchip RV1103 over ESP32-S3

- Decision Status: Accepted
- Engineering Context: Real-time high-definition video capture with wireless transmission to mobile clients. The legacy ESP32-S3 platform relies on software JPEG encoding, producing high processor loading, bus contention, and severe frame rate stuttering.
- Technical Resolution: Adopt the **Luckfox Pico Mini B (Rockchip RV1103)**.
- Rationale & Verification:
  - Hardware ISP 3.2 executes Bayer-to-YUV demosaicing, auto-exposure, and 3D noise reduction in dedicated silicon.
  - Hardware H.264/H.265 VPU encoder operates independently of the ARM Cortex-A7 CPU, completely eliminating frame drop artifacts.
  - Produces consistent 30.0 fps video at 4 Mbps bitrate with negligible CPU overhead (<15%).
- Engineering Impact: External USB Wi-Fi dongle required for networking; embedded Linux toolchain adopted.

---

## ADR-002: Storage Architecture — Zero External SD Card (SPI NAND Execution)

- Decision Status: Accepted
- Engineering Context: External MicroSD cards represent the highest cost driver and single point of failure in automotive dashcams (high-endurance 32GB cards cost upwards of INR 800.00). Target prototype budget is capped at INR 3,800.00.
- Technical Resolution: **Eliminate the MicroSD card entirely.** Boot and execute all firmware from the **128MB SPI NAND Flash** integrated on the Luckfox Pico Mini B.
- Rationale & Verification:
  - Saves approximately INR 800.00, reducing total bill of materials to INR 3,264.00 (under budget ceiling).
  - Eliminates file system corruption caused by sudden vehicle ignition power loss.
  - Lean Buildroot Linux distribution (Kernel + Busybox + RKMPI daemon) requires only ~38MB of the available 128MB flash.
  - Video stream is recorded on demand directly inside the client smartphone application (e.g. VLC Media Player).
- Engineering Impact: Flashing executed over USB via Rockchip RKDevTool / SocToolKit.

---

## ADR-003: Video Transport Protocol — Hardware H.264 RTSP via Wi-Fi SoftAP

- Decision Status: Accepted
- Engineering Context: Video feed must transmit wirelessly to mobile devices without reliance on external cellular connectivity or home routers.
- Technical Resolution: Implement an **ad-hoc IEEE 802.11n Wi-Fi Access Point (SoftAP)** using an RTL8188EUS USB adapter and stream video over **RTSP/RTP**.
- Rationale & Verification:
  - H.264 compression lowers bandwidth demand to ~4 Mbps (vs 25+ Mbps for MJPEG).
  - RTSP is natively supported on iOS and Android via VLC Media Player and standard CCTV viewer applications.
  - End-to-end glass-to-glass latency remains below 200 milliseconds.
- Engineering Impact: Mobile device connects directly to private SSID `DashCam-Proto`.

---

## ADR-004: Optical Sensor — SmartSens SC3336 3MP MIPI CSI-2

- Decision Status: Accepted
- Engineering Context: Selection of an optical sensor matching the RV1103 ISP pipeline without requiring manual driver or device tree modifications.
- Technical Resolution: Utilize the **SmartSens SC3336 3MP MIPI CSI-2 Camera Module** with 98.3 degree diagonal FOV lens.
- Rationale & Verification:
  - Full native support within the official Luckfox SDK with pre-calibrated Image Quality (IQ) tuning binaries.
  - High sensitivity sensor characteristics optimized for challenging low-light and high-contrast automotive road scenes.
- Engineering Impact: Physical connection established via standard 15-pin 0.5mm pitch FPC ribbon cable.

---

## ADR-005: Power Management & Input Transient Suppression Topology

- Decision Status: Accepted
- Engineering Context: Automotive 12V rails exhibit severe electrical noise, inductive load dumps up to 40V, and alternator ripple. Additionally, the IP5306 power bank IC enters auto-shutdown if output current drops below 50mA.
- Technical Resolution: Deploy a multi-stage electrical protection and conditioning circuit:
  - SMBJ5.0A TVS Diode clamps overvoltage spikes at the vehicle input.
  - Dual 470uF / 25V bulk electrolytic capacitors absorb low-frequency surges and buffer transmit bursts.
  - Four 100nF ceramic capacitors provide low-impedance high-frequency decoupling across regulator rails.
  - Static 100 Ohm resistor (R1) across the IP5306 output establishes a continuous 50mA drain, inhibiting the auto-sleep timer.
- Rationale & Verification: Guarantees uninterrupted 5.0V DC system rail under all vehicle operational states.

---

```text
╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ B                                                                                                  B ║
║   ╔══════════════════════════════════════════════════════════════════════════════════════════════╗   ║
║   ║                                               ╔══════════════════════════════════════════════╣   ║
║   ║                                               ║ PROJECT:    DASHCAM PROTOTYPE PROJECT        ║   ║
║   ║                                               ║ TITLE:      ARCHITECTURE DECISION RECORDS    ║   ║
║   ║                                               ║ DOC NUMBER: ENG-DASH-ADR-001   REVISION: 1.4 ║   ║
║   ║                                               ║ DATE:       2026-10-08         SHEET: 1 OF 1 ║   ║
║   ║                                               ╠══════════════════════════════════════════════╣   ║
║   ║                                               ║ LEAD ENGR:  Souvik H                         ║   ║
║   ║                                               ║ REGN NO:    IN-ENG-2022-22824                   ║   ║
║   ║                                               ║ DISCIPLINE: ARCHITECTURE & SYSTEMS ENGR      ║   ║
║   ║                                               ║ STATUS:     APPROVED ENGINEERING RECORD      ║   ║
║   ║                                               ║ FORMAT:     A4 STANDARD ENGINEERING SHEET    ║   ║
║   ╚═══════════════════════════════════════════════╩══════════════════════════════════════════════╝   ║
║ 1                                              2                                                   3 ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```
