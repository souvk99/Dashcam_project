# Hardware

This folder contains all electronic hardware design assets for the dashcam prototype.

## Structure

| Folder | Contents |
|--------|----------|
| `source/` | Schematics, PCB layout files, BOM (Bill of Materials), Gerber files, wiring diagrams |
| `simulation/` | SPICE simulations, signal integrity analysis, power analysis |

## Recommended Tools

- **Schematic / PCB**: KiCad / EasyEDA / Altium Designer
- **SPICE Simulation**: LTspice / Ngspice
- **Component Research**: Octopart / DigiKey / Mouser / Robu.in

## Selected System Components

- **Core SBC**: Luckfox Pico Mini B (RV1103 SoC, 64MB DDR2, 128MB SPI NAND)
- **Camera Module**: SmartSens SC3336 3MP MIPI CSI-2 (98.3° wide-angle lens)
- **Onboard Storage**: 128MB SPI NAND Flash (zero external SD card required)
- **Wireless Interface**: Realtek RTL8188EUS USB 802.11n Wi-Fi Dongle (SoftAP RTSP streaming)
- **Battery & PMIC**: 3.7V 1000mAh LiPo Battery (PCM protected) + IP5306 Synchronous PMIC (load-sharing)
- **Vehicle Pre-Regulator**: LM2596 DC-DC Step-Down Buck (12V to 5.0V DC)
- **Transient Protection**: SMBJ5.0A TVS diode, 470µF bulk electrolytic capacitors, 100nF ceramic decoupling

## Design Considerations

- Automotive 12V transient overvoltage protection (clamping up to 40V spikes)
- Low-power operation (~2.66W active streaming)
- Multi-stage decoupling and anti-sleep keep-alive circuit for the PMIC
