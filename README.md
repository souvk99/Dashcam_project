# Dashcam Prototype Project

A full-stack dashcam prototype built from scratch, covering mechanical design, hardware, software, and documentation.

## Project Structure

```
Dashcam_project/
├── mechanicals/        # CAD models, enclosure, mounts, and physical design
│   ├── source/         # Original design files (CAD, STL, STEP, etc.)
│   └── simulation/     # Structural / thermal simulations
├── hardware/           # PCB schematics, circuit design, component selection
│   ├── source/         # KiCad / Eagle / Altium design files
│   └── simulation/     # SPICE and circuit simulations
├── software/           # Firmware and application code
│   ├── source/         # Production source code
│   └── simulation/     # Software-in-the-loop / emulation scripts
└── documentation/      # Datasheets, design decisions, user guides, reports
```

## Project Goals

- [ ] Design a compact dashcam enclosure
- [ ] Select and integrate camera, storage, and power hardware
- [ ] Develop firmware for video capture, loop recording, and event detection
- [ ] Validate design through simulation before prototyping
- [ ] Produce complete documentation for reproducibility

## Getting Started

Refer to each subfolder's `README.md` for domain-specific instructions and toolchain requirements.

## License

TBD
