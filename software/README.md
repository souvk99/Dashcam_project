# Software

This folder contains all firmware and embedded software for the dashcam prototype.

## Target Platform & Hardware

- **Target SBC**: Luckfox Pico Mini B (RV1103 SoC, 64MB DDR2, 128MB SPI NAND)
- **Camera Interface**: SmartSens SC3336 via MIPI CSI-2
- **Storage Subsystem**: 128MB SPI NAND Flash (UBIFS partitions; zero external SD card)
- **Network Interface**: RTL8188EUS USB Wi-Fi dongle (802.11n SoftAP)

## Structure

| Folder | Contents |
|--------|----------|
| `source/` | C production streamer source code (`dashcam_streamer.c`), CMake build scripts |
| `simulation/` | Software-in-the-loop (SIL) scripts, stream test harnesses |

## Toolchain & Software Stack

- **Operating System**: Buildroot Linux (Kernel 5.10 + Busybox)
- **Media Framework**: Rockchip Media Process Interface (RKMPI)
- **Compression**: Hardware H.264 VPU (1080p @ 30fps CBR 4 Mbps)
- **Transport**: RTSP server on port 554 (`rtsp://192.168.169.1/live/0`)
- **Wireless Daemon**: HostAPD + udhcpd
- **Build System**: CMake / Luckfox SDK cross-compiler (`arm-rockchip830-linux-uclibcgnueabihf`)

## Implemented Features

- [x] Zero-copy hardware video pipeline (SC3336 -> ISP 3.2 -> H.264 VPU)
- [x] Onboard 128MB SPI NAND Flash execution (sub-6s cold boot)
- [x] Point-to-point Wi-Fi SoftAP access point (`DashCam-Proto`)
- [x] Real-time RTSP H.264 video streaming to smartphone (VLC player)
- [x] Auto-start system daemon (`/etc/init.d/S99dashcam`)
- [x] GPIO visual status indicator (GPIO48)

## Compilation & Build

```bash
# Set cross-compiler toolchain from Luckfox SDK
cd software/source
mkdir build && cd build
cmake -DCMAKE_SYSROOT=/path/to/luckfox-pico-sdk/sysroot ..
make
```
