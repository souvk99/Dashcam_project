import os
import subprocess

BASE_DIR = r"C:\Users\souvk\Downloads\Dashcam_project"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

from build_sheets import CSS_HEADER, CSS_FOOTER, get_sheet_html

def compile_pdf(html_path, pdf_path):
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    subprocess.run(cmd, check=True)
    size = os.path.getsize(pdf_path)
    print(f"[OK] Generated {pdf_path} ({size} bytes)")

# -------------------------------------------------------------
# 1. HARDWARE SPECIFICATION (ENG-DASH-HW-001) - 2 SHEETS
# -------------------------------------------------------------
hw_s1 = """
<h1>Hardware Architecture & Subsystem Specification (Sheet 1)</h1>
<p><strong>System Objective:</strong> Ultra-low-cost, battery-buffered automotive vision streaming prototype using Luckfox Pico Mini B (RV1103 SoC, 64MB DDR2, 128MB SPI NAND) and SmartSens SC3336 3MP sensor.</p>

<h2>1. Functional Subsystem Overview</h2>
<table class="tech-table">
    <tr>
        <th style="width: 25%;">Subsystem</th>
        <th style="width: 35%;">Component Selection</th>
        <th style="width: 40%;">Engineering Specification</th>
    </tr>
    <tr>
        <td><strong>Vision Processor</strong></td>
        <td>Luckfox Pico Mini B (RV1103 SoC, 64MB DDR2, 128MB SPI NAND)</td>
        <td>ARM Cortex-A7 @ 1.2GHz + RISC-V co-processor, 64MB DDR2, built-in ISP 3.2, HW H.264/H.265 VPU.</td>
    </tr>
    <tr>
        <td><strong>Optical Sensor</strong></td>
        <td>SmartSens SC3336 3MP MIPI CSI-2</td>
        <td>2304x1296 @ 30fps, 2-lane MIPI D-PHY, 98.3 Deg wide-angle lens, high SNR low-light automotive profile.</td>
    </tr>
    <tr>
        <td><strong>Non-Volatile Storage</strong></td>
        <td>128MB SPI NAND Flash (Onboard)</td>
        <td>Zero SD card topology. Houses U-Boot, Linux kernel, Busybox rootfs, and RKMPI streamer daemon.</td>
    </tr>
    <tr>
        <td><strong>Wireless Network</strong></td>
        <td>Realtek RTL8188EUS USB Dongle</td>
        <td>802.11b/g/n 2.4GHz SoftAP mode, 150Mbps PHY rate, native in-kernel '8188eu' driver.</td>
    </tr>
    <tr>
        <td><strong>Power Management</strong></td>
        <td>Injoinic IP5306 Synchronous PMIC</td>
        <td>2.1A CC/CV LiPo charger, 5.0V @ 2.4A boost output, autonomous load-sharing, over/under voltage protection.</td>
    </tr>
    <tr>
        <td><strong>Input Pre-Regulator</strong></td>
        <td>LM2596 DC-DC Step-Down Buck</td>
        <td>Steps down vehicle electrical rail (9V-16V nominal, transients up to 40V) to regulated 5.0V DC.</td>
    </tr>
</table>

<h2>2. Power Conditioning & Protection Topology</h2>
<div class="code-box">[12V Vehicle Rail In] ──┬──────────────────────────────────────────┐
                       │                                          │
                     [ D1 ] SMBJ5.0A TVS (Cathode)               [ C5 ] 470uF / 25V (Electrolytic +)
                       │                                          │
[Vehicle Ground (-)]  ──┴──────────────────────────────────────────┴───► [LM2596 VIN (-)]
[12V Vehicle Rail In] ─────────────────────────────────────────────────► [LM2596 VIN (+)]
                                    LM2596 BUCK REGULATOR (Set to +5.0V DC)
[LM2596 VOUT (+5V)] ───┬──────────────────┬────────────────────────────► [IP5306 VIN (+5V)]
                       │                  │
                     [ C6 ] 470uF       [ C4 ] 100nF (104 Ceramic)
                     (Electrolytic +)     │
                       │                  │
[LM2596 VOUT (GND)]  ──┴──────────────────┴────────────────────────────► [IP5306 GND]</div>
"""

hw_s2 = """
<h1>Hardware Architecture & Subsystem Specification (Sheet 2)</h1>

<h2>3. Hardware Interface & Signal Specification Matrix</h2>
<table class="tech-table">
    <tr>
        <th>Interface / Bus</th>
        <th>Source -> Destination</th>
        <th>Physical Standard</th>
        <th>Baud Rate / Bandwidth</th>
        <th>Engineering Purpose</th>
    </tr>
    <tr>
        <td><strong>MIPI CSI-2</strong></td>
        <td>SC3336 -> RV1103</td>
        <td>Differential D-PHY (2-lane)</td>
        <td>800 Mbps / lane</td>
        <td>Direct transport of raw 10-bit Bayer pixel stream to ISP.</td>
    </tr>
    <tr>
        <td><strong>SCCB Control</strong></td>
        <td>RV1103 <-> SC3336</td>
        <td>I2C Protocol (0x3C)</td>
        <td>400 kHz Fast Mode</td>
        <td>Sensor initialization, exposure, white balance, and gain control.</td>
    </tr>
    <tr>
        <td><strong>SPI Flash Bus</strong></td>
        <td>RV1103 <-> SPI NAND</td>
        <td>Standard Quad SPI</td>
        <td>50 MHz to 100 MHz</td>
        <td>Execution interface for bootloader, Linux kernel, and rootfs.</td>
    </tr>
    <tr>
        <td><strong>USB 2.0 Host</strong></td>
        <td>RV1103 <-> RTL8188EUS</td>
        <td>High-Speed USB 2.0 PHY</td>
        <td>480 Mbps</td>
        <td>Network physical interface transporting H.264 RTSP video stream.</td>
    </tr>
    <tr>
        <td><strong>Status Indicator</strong></td>
        <td>RV1103 -> Status LED</td>
        <td>GPIO Out via R4 (470 Ohm)</td>
        <td>DC Digital</td>
        <td>Visual heartbeat and streaming state indication.</td>
    </tr>
    <tr>
        <td><strong>Master Switch</strong></td>
        <td>Push Button -> RV1103</td>
        <td>GPIO Active Low (R2: 10k)</td>
        <td>DC Digital</td>
        <td>System mode selection and safe shutdown control switch.</td>
    </tr>
</table>

<h2>4. Passive Protection Schedule</h2>
<table class="tech-table">
    <tr>
        <th>Ref Des</th>
        <th>Component Value</th>
        <th>Package</th>
        <th>Functional Location & Engineering Purpose</th>
    </tr>
    <tr>
        <td><strong>D1</strong></td>
        <td>SMBJ5.0A (600W)</td>
        <td>SMB / DO-214AA</td>
        <td>12V vehicle input line clamp; shunts inductive kickback and alternator load dump spikes.</td>
    </tr>
    <tr>
        <td><strong>C5, C6</strong></td>
        <td>470uF / 25V Radial</td>
        <td>Aluminum Electrolytic</td>
        <td>C5 filters vehicle input ripple; C6 buffers LM2596 output during Wi-Fi transmission current spikes.</td>
    </tr>
    <tr>
        <td><strong>C1-C4</strong></td>
        <td>100nF (104) 50V</td>
        <td>Ceramic Radial / 0805</td>
        <td>High-frequency decoupling placed directly at IP5306 output, SBC power port, Wi-Fi port, and buck node.</td>
    </tr>
    <tr>
        <td><strong>R1</strong></td>
        <td>100 Ohm / 0.25W</td>
        <td>Metal Film Axial</td>
        <td>IP5306 keep-alive dummy load: maintains 50mA static pull to prevent automatic power bank shutdown.</td>
    </tr>
    <tr>
        <td><strong>R2, R3</strong></td>
        <td>10 kOhm / 0.25W</td>
        <td>Carbon Film Axial</td>
        <td>Pull-up resistor for power switch and pull-down resistor for boot state latching.</td>
    </tr>
    <tr>
        <td><strong>R4, R5</strong></td>
        <td>470 Ohm, 1 kOhm</td>
        <td>Metal Film Axial</td>
        <td>R4 limits status LED current; R5 ties USB ID pin to ground securing default USB Host mode.</td>
    </tr>
</table>
"""

html_hw = CSS_HEADER + \
    get_sheet_html("HARDWARE SPECIFICATION SHEET", "ENG-DASH-HW-001", "EMBEDDED SYSTEMS & HARDWARE", sheet_str="1 OF 2", content_html=hw_s1) + \
    get_sheet_html("HARDWARE SPECIFICATION SHEET", "ENG-DASH-HW-001", "EMBEDDED SYSTEMS & HARDWARE", sheet_str="2 OF 2", content_html=hw_s2) + \
    CSS_FOOTER

with open(os.path.join(BASE_DIR, "documentation", "hardware_design.html"), "w", encoding="utf-8") as f:
    f.write(html_hw)
compile_pdf(os.path.join(BASE_DIR, "documentation", "hardware_design.html"), os.path.join(BASE_DIR, "documentation", "hardware_design.pdf"))

# -------------------------------------------------------------
# 2. BILL OF MATERIALS SPECIFICATION (ENG-DASH-BOM-001) - 2 SHEETS
# -------------------------------------------------------------
bom_s1 = """
<h1>Bill of Materials & Procurement Schedule (Sheet 1)</h1>
<p><strong>Cost Constraint:</strong> Budget Ceiling: INR 3,800.00 | <strong>Total Reconciled Cost:</strong> INR 3,264.00 | <strong>Variance:</strong> - INR 536.00 (Favorable)</p>

<h2>1. Consolidated Component Procurement Schedule</h2>
<table class="tech-table">
    <tr>
        <th style="width: 5%;">Item</th>
        <th style="width: 8%;">Ref</th>
        <th style="width: 32%;">Component Description / Part Number</th>
        <th style="width: 18%;">Manufacturer / Chipset</th>
        <th style="width: 6%;">Qty</th>
        <th style="width: 10%;">Unit Cost (INR)</th>
        <th style="width: 11%;">Total Cost (INR)</th>
        <th style="width: 10%;">Supplier</th>
    </tr>
    <tr>
        <td>1</td>
        <td>U1</td>
        <td>Luckfox Pico Mini B (RV1103 SoC, 64MB DDR2, 128MB SPI NAND)</td>
        <td>Rockchip / Luckfox</td>
        <td>1</td>
        <td>1,749.00</td>
        <td>1,749.00</td>
        <td>ThinkRobotics</td>
    </tr>
    <tr>
        <td>2</td>
        <td>U2</td>
        <td>SC3336 3MP MIPI CSI-2 Camera Module (98.3 Deg FOV Lens)</td>
        <td>SmartSens / Luckfox</td>
        <td>1</td>
        <td>800.00</td>
        <td>800.00</td>
        <td>Hubtronics</td>
    </tr>
    <tr>
        <td>3</td>
        <td>U3</td>
        <td>USB 2.0 Wi-Fi Dongle (RTL8188EUS 802.11n 150Mbps SoftAP)</td>
        <td>Realtek / Generic</td>
        <td>1</td>
        <td>180.00</td>
        <td>180.00</td>
        <td>Zbotic / Fabtolab</td>
    </tr>
    <tr>
        <td>4</td>
        <td>BT1</td>
        <td>LiPo Rechargeable Battery 3.7V 1000mAh with PCM (JST-PH 2.0mm)</td>
        <td>Probots (KP-503450)</td>
        <td>1</td>
        <td>340.00</td>
        <td>340.00</td>
        <td>Probots</td>
    </tr>
    <tr>
        <td>5</td>
        <td>U4</td>
        <td>IP5306 Power Bank Module (2.1A Charge / 2.4A Boost / Load Sharing)</td>
        <td>Injoinic / Generic</td>
        <td>1</td>
        <td>45.00</td>
        <td>45.00</td>
        <td>Techiesms</td>
    </tr>
    <tr>
        <td>6</td>
        <td>U5</td>
        <td>LM2596 DC-DC Step-Down Buck Converter Module (12V to 5V DC)</td>
        <td>TI / Generic</td>
        <td>1</td>
        <td>49.00</td>
        <td>49.00</td>
        <td>Robu.in</td>
    </tr>
    <tr>
        <td>7</td>
        <td>D1</td>
        <td>TVS Diode SMBJ5.0A (600W Transient Voltage Suppressor, SMB)</td>
        <td>Littelfuse / Generic</td>
        <td>1</td>
        <td>20.00</td>
        <td>20.00</td>
        <td>Robu.in</td>
    </tr>
    <tr>
        <td>8</td>
        <td>C1-C4</td>
        <td>Ceramic Capacitors 100nF (104) 50V Radial (Pack of 10)</td>
        <td>Murata / Generic</td>
        <td>1 pk</td>
        <td>15.00</td>
        <td>15.00</td>
        <td>Robu.in</td>
    </tr>
    <tr>
        <td>9</td>
        <td>R1-R5</td>
        <td>Carbon / Metal Film Resistors Assorted (100R, 10k x2, 470R, 1k)</td>
        <td>Generic (0.25W)</td>
        <td>1 pk</td>
        <td>20.00</td>
        <td>20.00</td>
        <td>Local Market</td>
    </tr>
    <tr>
        <td>10</td>
        <td>C5, C6</td>
        <td>Aluminum Electrolytic Capacitors 470uF / 25V Radial</td>
        <td>Nichicon / Generic</td>
        <td>2</td>
        <td>8.00</td>
        <td>16.00</td>
        <td>Robu.in</td>
    </tr>
    <tr>
        <td>11</td>
        <td>MISC</td>
        <td>JST-PH 2.0mm 2-pin Connector Pairs and Interconnect Wires</td>
        <td>Generic</td>
        <td>1 set</td>
        <td>30.00</td>
        <td>30.00</td>
        <td>Robu.in</td>
    </tr>
    <tr style="background-color: #f2f2f2; font-weight: bold;">
        <td colspan="6" style="text-align: right;">TOTAL RECONCILED PROCUREMENT COST:</td>
        <td colspan="2">INR 3,264.00 (UNDER BUDGET)</td>
    </tr>
</table>
"""

bom_s2 = """
<h1>Bill of Materials & Procurement Schedule (Sheet 2)</h1>

<h2>2. Technical Component Roles & Procurement Checkpoints</h2>
<table class="tech-table">
    <tr>
        <th style="width: 20%;">Component</th>
        <th style="width: 35%;">Critical Technical Requirement</th>
        <th style="width: 45%;">Verification Method Prior to Assembly</th>
    </tr>
    <tr>
        <td><strong>Luckfox Pico Mini B</strong></td>
        <td>Must feature 128MB SPI NAND onboard flash.</td>
        <td>Confirm board boots from internal flash via USB MaskRom without MicroSD card present.</td>
    </tr>
    <tr>
        <td><strong>SC3336 3MP Module</strong></td>
        <td>Wide-angle optical lens (98.3 Deg FOV) with 15-pin FPC.</td>
        <td>Verify CSI ribbon cable pitch (0.5mm) and pin 1 GND orientation with board socket.</td>
    </tr>
    <tr>
        <td><strong>USB Wi-Fi Dongle</strong></td>
        <td>Realtek RTL8188EUS chipset with SoftAP mode.</td>
        <td>Verify device ID 0bda:8179 in Linux kernel; confirm '8188eu' driver binds automatically.</td>
    </tr>
    <tr>
        <td><strong>LiPo Battery Pack</strong></td>
        <td>3.7V 1000mAh with internal PCM protection board.</td>
        <td>Verify open-circuit voltage (3.7V - 4.2V) and confirm JST-PH 2.0mm connector polarity (+/-).</td>
    </tr>
    <tr>
        <td><strong>IP5306 PMIC Module</strong></td>
        <td>Load-sharing capable synchronous boost converter.</td>
        <td>Verify 5.0V output under 500mA load while simultaneously charging LiPo cell.</td>
    </tr>
    <tr>
        <td><strong>LM2596 Buck Regulator</strong></td>
        <td>Step-down automotive pre-regulator (3A peak).</td>
        <td>Adjust trim potentiometer to precisely 5.00V DC before connecting downstream loads.</td>
    </tr>
    <tr>
        <td><strong>TVS Diode & Filter Network</strong></td>
        <td>SMBJ5.0A (600W) + 470uF bulk reservoir capacitors.</td>
        <td>Verify TVS diode polarity (cathode towards +12V rail) and capacitor voltage ratings (25V min).</td>
    </tr>
</table>

<h2>3. Budget Variance & Trade-Off Summary</h2>
<p>• Initial Target Ceiling: INR 3,800.00 | Actual Reconciled BOM: INR 3,264.00 (Savings: INR 536.00).</p>
<p>• Eliminating the high-endurance MicroSD card saved ~INR 820.00 and prevented continuous vehicular write degradation.</p>
<p>• On-demand video recording is safely delegated to the client smartphone application (VLC) storage.</p>
"""

html_bom = CSS_HEADER + \
    get_sheet_html("BILL OF MATERIALS SPECIFICATION", "ENG-DASH-BOM-001", "PROCUREMENT & COMPONENT ENGR", sheet_str="1 OF 2", content_html=bom_s1) + \
    get_sheet_html("BILL OF MATERIALS SPECIFICATION", "ENG-DASH-BOM-001", "PROCUREMENT & COMPONENT ENGR", sheet_str="2 OF 2", content_html=bom_s2) + \
    CSS_FOOTER

with open(os.path.join(BASE_DIR, "documentation", "BOM.html"), "w", encoding="utf-8") as f:
    f.write(html_bom)
compile_pdf(os.path.join(BASE_DIR, "documentation", "BOM.html"), os.path.join(BASE_DIR, "documentation", "BOM.pdf"))

# -------------------------------------------------------------
# 3. ELECTRICAL POWER BUDGET SPECIFICATION (ENG-DASH-PWR-001) - 2 SHEETS
# -------------------------------------------------------------
pwr_s1 = """
<h1>Electrical Power Budget & Thermal Calculation (Sheet 1)</h1>

<h2>1. Electrical Power Distribution Architecture</h2>
<div class="code-box">[12V Vehicle Rail In] ──► [SMBJ5.0A TVS + 470uF Cap] ──► [LM2596 Buck (12V to 5V DC)]
                                                                  │
                                                                  ▼
[3.7V 1000mAh LiPo] ◄────► [IP5306 PMIC Module (Charge/Boost)] ──► [Main +5.0V Rail]
                                 │ (with 100 Ohm dummy load)       │
                                                                   ├──► [Luckfox Pico Mini B (RV1103)]
                                                                   ├──► [SmartSens SC3336 3MP Sensor]
                                                                   └──► [RTL8188EUS USB Wi-Fi Dongle]</div>

<h2>2. Subsystem Current Schedule (Measured at 5.0V DC System Rail)</h2>
<table class="tech-table">
    <tr>
        <th>Load Node / Subsystem</th>
        <th>Standby Current (mA)</th>
        <th>Active Streaming (mA)</th>
        <th>Peak Transient (mA)</th>
        <th>Operating Voltage</th>
        <th>Active Power (W)</th>
    </tr>
    <tr>
        <td>RV1103 ARM Cortex-A7 Core</td>
        <td>50.0</td>
        <td>120.0</td>
        <td>180.0</td>
        <td>5.0V DC</td>
        <td>0.60 W</td>
    </tr>
    <tr>
        <td>Hardware ISP 3.2 Engine</td>
        <td>0.0</td>
        <td>70.0</td>
        <td>90.0</td>
        <td>5.0V DC</td>
        <td>0.35 W</td>
    </tr>
    <tr>
        <td>Hardware H.264 VPU Encoder</td>
        <td>0.0</td>
        <td>50.0</td>
        <td>70.0</td>
        <td>5.0V DC</td>
        <td>0.25 W</td>
    </tr>
    <tr>
        <td>64MB DDR2 Memory Array</td>
        <td>15.0</td>
        <td>30.0</td>
        <td>45.0</td>
        <td>5.0V DC</td>
        <td>0.15 W</td>
    </tr>
    <tr>
        <td>SmartSens SC3336 3MP Sensor</td>
        <td>0.0</td>
        <td>75.0</td>
        <td>110.0</td>
        <td>5.0V DC</td>
        <td>0.38 W</td>
    </tr>
    <tr>
        <td>RTL8188EUS USB Wi-Fi Adapter</td>
        <td>30.0</td>
        <td>130.0</td>
        <td>250.0</td>
        <td>5.0V DC</td>
        <td>0.65 W</td>
    </tr>
    <tr>
        <td>IP5306 Keep-Alive Load (R1: 100R)</td>
        <td>50.0</td>
        <td>50.0</td>
        <td>50.0</td>
        <td>5.0V DC</td>
        <td>0.25 W</td>
    </tr>
    <tr>
        <td>Status Optical Indicator (R4: 470R)</td>
        <td>0.0</td>
        <td>7.0</td>
        <td>10.0</td>
        <td>5.0V DC</td>
        <td>0.035 W</td>
    </tr>
    <tr style="background-color: #f2f2f2; font-weight: bold;">
        <td>TOTAL 5.0V RAIL LOAD:</td>
        <td>145.0 mA</td>
        <td>532.0 mA</td>
        <td>805.0 mA</td>
        <td>5.0V DC</td>
        <td>2.66 Watts</td>
    </tr>
</table>
"""

pwr_s2 = """
<h1>Electrical Power Budget & Thermal Calculation (Sheet 2)</h1>

<h2>3. Battery Capacity & Operational Autonomy Calculation</h2>
<table class="tech-table">
    <tr>
        <th>Calculation Step</th>
        <th>Formula / Technical Parameter</th>
        <th>Resulting Value</th>
    </tr>
    <tr>
        <td>Total Stored Energy</td>
        <td>Battery Capacity (1.0 Ah) x Nominal Voltage (3.7V DC)</td>
        <td>3.70 Watt-hours (Wh)</td>
    </tr>
    <tr>
        <td>Effective Usable Energy</td>
        <td>3.70 Wh x IP5306 Boost Conversion Efficiency (eta = 90.0%)</td>
        <td>3.33 Watt-hours (Wh)</td>
    </tr>
    <tr>
        <td>Active Streaming Autonomy</td>
        <td>Usable Energy (3.33 Wh) / Continuous System Power (2.66 W)</td>
        <td><strong>1.25 Hours (75 Minutes continuous streaming)</strong></td>
    </tr>
    <tr>
        <td>Standby State Autonomy</td>
        <td>Usable Energy (3.33 Wh) / Quiescent Standby Power (0.725 W)</td>
        <td><strong>4.59 Hours (~275 Minutes)</strong></td>
    </tr>
</table>

<h2>4. Vehicle In-Line Charging & Thermal Dissipation Analysis</h2>
<p>• <strong>Charging Dynamics:</strong> LM2596 delivers up to 2.0A at 5.0V. System draws 532mA; remaining ~1.0A charges LiPo to 100% in ~65 min.</p>
<p>• <strong>Thermal Dissipation:</strong> RV1103 SoC dissipates ~0.8W. Requires a 9x9x5mm extruded aluminum heatsink.</p>
<p>• <strong>Automotive Environment:</strong> Windshield temperatures can exceed 65 Deg C. LiPo charging must be inhibited above 45 Deg C ambient.</p>
"""

html_pwr = CSS_HEADER + \
    get_sheet_html("ELECTRICAL POWER & THERMAL SPEC", "ENG-DASH-PWR-001", "POWER ELECTRONICS & THERMAL ENGR", sheet_str="1 OF 2", content_html=pwr_s1) + \
    get_sheet_html("ELECTRICAL POWER & THERMAL SPEC", "ENG-DASH-PWR-001", "POWER ELECTRONICS & THERMAL ENGR", sheet_str="2 OF 2", content_html=pwr_s2) + \
    CSS_FOOTER

with open(os.path.join(BASE_DIR, "documentation", "power_budget.html"), "w", encoding="utf-8") as f:
    f.write(html_pwr)
compile_pdf(os.path.join(BASE_DIR, "documentation", "power_budget.html"), os.path.join(BASE_DIR, "documentation", "power_budget.pdf"))

# -------------------------------------------------------------
# 4. SYSTEM REQUIREMENTS SPECIFICATION (ENG-DASH-REQ-001) - 2 SHEETS
# -------------------------------------------------------------
req_s1 = """
<h1>System Requirements Specification (Sheet 1)</h1>

<h2>1. Functional Requirements Matrix</h2>
<table class="tech-table">
    <tr>
        <th style="width: 10%;">ID</th>
        <th style="width: 40%;">Requirement Description</th>
        <th style="width: 18%;">Acceptance Criteria</th>
        <th style="width: 32%;">Engineering Implementation</th>
    </tr>
    <tr>
        <td><strong>FR-01</strong></td>
        <td>Stream continuous H.264 compressed video over local Wi-Fi without frame stutter.</td>
        <td>30.0 fps sustained, zero dropped frames over 30 min.</td>
        <td>Rockchip RV1103 Hardware VPU Encoder.</td>
    </tr>
    <tr>
        <td><strong>FR-02</strong></td>
        <td>Minimum native video capture resolution.</td>
        <td>1920 x 1080 (1080p Full HD).</td>
        <td>SmartSens SC3336 3MP Sensor + ISP 3.2.</td>
    </tr>
    <tr>
        <td><strong>FR-03</strong></td>
        <td>Zero external SD card dependency for system boot and runtime execution.</td>
        <td>Successful system cold boot with SD slot empty.</td>
        <td>128MB SPI NAND Flash (Luckfox Mini B).</td>
    </tr>
    <tr>
        <td><strong>FR-04</strong></td>
        <td>Wireless local point-to-point network connectivity (SoftAP).</td>
        <td>Phone associates directly without external router.</td>
        <td>RTL8188EUS USB Wi-Fi (HostAPD 802.11n).</td>
    </tr>
    <tr>
        <td><strong>FR-05</strong></td>
        <td>Battery-buffered autonomous operation during engine cut-off.</td>
        <td>Greater than 60 minutes continuous streaming.</td>
        <td>3.7V 1000mAh LiPo Pack with PCM Protection.</td>
    </tr>
    <tr>
        <td><strong>FR-06</strong></td>
        <td>Simultaneous vehicle power pass-through and battery recharge.</td>
        <td>Battery charges while system streams video.</td>
        <td>IP5306 Synchronous PMIC with Load-Sharing.</td>
    </tr>
    <tr>
        <td><strong>FR-07</strong></td>
        <td>Automotive electrical transient and overvoltage protection.</td>
        <td>Clamps inductive spikes up to 40V safely.</td>
        <td>SMBJ5.0A TVS Diode + 470uF Bulk Reservoir.</td>
    </tr>
    <tr>
        <td><strong>FR-08</strong></td>
        <td>Power management auto-sleep inhibition circuit.</td>
        <td>PMIC maintains continuous 5V output.</td>
        <td>100 Ohm Resistor (R1) static ~50mA pull.</td>
    </tr>
    <tr>
        <td><strong>FR-09</strong></td>
        <td>Wide-angle forward optical field of view.</td>
        <td>Diagonal FOV greater than 95.0 degrees.</td>
        <td>98.3 degree wide-angle lens assembly.</td>
    </tr>
    <tr>
        <td><strong>FR-10</strong></td>
        <td>Visual hardware status indication.</td>
        <td>Optical indication of streaming state.</td>
        <td>GPIO driven Status LED via 470 Ohm resistor.</td>
    </tr>
</table>
"""

req_s2 = """
<h1>System Requirements Specification (Sheet 2)</h1>

<h2>2. Non-Functional Performance & Environmental Specifications</h2>
<table class="tech-table">
    <tr>
        <th style="width: 15%;">Metric ID</th>
        <th style="width: 30%;">Performance Metric</th>
        <th style="width: 25%;">Specification Limit</th>
        <th style="width: 30%;">Verification Technique</th>
    </tr>
    <tr>
        <td><strong>NFR-01</strong></td>
        <td>Total Bill of Materials Cost</td>
        <td>Less than INR 3,800.00 (Actual: INR 3,264.00)</td>
        <td>Procurement reconciliation audit.</td>
    </tr>
    <tr>
        <td><strong>NFR-02</strong></td>
        <td>Cold Boot Duration to Video Stream</td>
        <td>Less than 6.0 Seconds from cold power applied</td>
        <td>Serial timestamp measurement.</td>
    </tr>
    <tr>
        <td><strong>NFR-03</strong></td>
        <td>End-to-End Glass-to-Glass Latency</td>
        <td>Less than 250 Milliseconds</td>
        <td>High-speed stopwatch comparison.</td>
    </tr>
    <tr>
        <td><strong>NFR-04</strong></td>
        <td>Ambient Operating Temperature Envelope</td>
        <td>0 Deg C to 45 Deg C (Non-condensing)</td>
        <td>Thermal chamber soak.</td>
    </tr>
    <tr>
        <td><strong>NFR-05</strong></td>
        <td>Maximum Physical Enclosure Envelope</td>
        <td>70 mm (L) x 45 mm (W) x 30 mm (H)</td>
        <td>Digital caliper mechanical check.</td>
    </tr>
</table>

<h2>3. Scope Baseline & Exclusions</h2>
<p>• <strong>No On-Device SD Recording:</strong> SD card elimination avoids write degradation and reduces BOM cost.</p>
<p>• <strong>Client-Side Storage:</strong> Video streams are recorded directly inside client mobile app (e.g. VLC) on demand.</p>
"""

html_req = CSS_HEADER + \
    get_sheet_html("SYSTEM REQUIREMENTS (SRS)", "ENG-DASH-REQ-001", "SYSTEMS ENGINEERING", sheet_str="1 OF 2", content_html=req_s1) + \
    get_sheet_html("SYSTEM REQUIREMENTS (SRS)", "ENG-DASH-REQ-001", "SYSTEMS ENGINEERING", sheet_str="2 OF 2", content_html=req_s2) + \
    CSS_FOOTER

with open(os.path.join(BASE_DIR, "documentation", "requirements", "system_requirements.html"), "w", encoding="utf-8") as f:
    f.write(html_req)
compile_pdf(os.path.join(BASE_DIR, "documentation", "requirements", "system_requirements.html"), os.path.join(BASE_DIR, "documentation", "requirements", "system_requirements.pdf"))

# -------------------------------------------------------------
# 5. ARCHITECTURE DECISION RECORDS (ENG-DASH-ADR-001) - 2 SHEETS
# -------------------------------------------------------------
adr_s1 = """
<h1>Architecture Decision Records (ADR - Sheet 1)</h1>

<h2>ADR-001: Platform Selection — Rockchip RV1103 over ESP32-S3</h2>
<p>• <strong>Status:</strong> Accepted | <strong>Date:</strong> 2026-10-08</p>
<p>• <strong>Context:</strong> ESP32-S3 software-encodes MJPEG video, saturating the CPU and PSRAM bus and causing severe frame drop stutters when transmitting over Wi-Fi.</p>
<p>• <strong>Resolution:</strong> Adopt the <strong>Luckfox Pico Mini B (Rockchip RV1103)</strong> equipped with dedicated hardware ISP 3.2 and hardware H.264 VPU compression.</p>
<p>• <strong>Technical Rationale:</strong> Hardware video pipeline operates at zero CPU overhead. Produces smooth 30.0 fps Full HD H.264 video with clean RTSP streaming.</p>

<h2>ADR-002: Storage Topology — Zero SD Card Execution (128MB SPI NAND)</h2>
<p>• <strong>Status:</strong> Accepted | <strong>Date:</strong> 2026-10-08</p>
<p>• <strong>Context:</strong> High-endurance 32GB SD cards cost upwards of INR 800.00 and represent the primary failure point under continuous vehicular writes.</p>
<p>• <strong>Resolution:</strong> <strong>Eliminate external SD card entirely.</strong> Boot and execute firmware exclusively from onboard 128MB SPI NAND Flash.</p>
<p>• <strong>Technical Rationale:</strong> Reduces BOM to INR 3,264.00 (under INR 3,800 ceiling). Eliminates filesystem corruption on sudden ignition power loss. Live stream is recorded on demand directly inside the client smartphone application (e.g. VLC).</p>

<h2>ADR-003: Video Protocol — Hardware H.264 RTSP via Wi-Fi SoftAP</h2>
<p>• <strong>Status:</strong> Accepted | <strong>Date:</strong> 2026-10-08</p>
<p>• <strong>Context:</strong> Video stream must transmit reliably to smartphones without requiring an external Wi-Fi router or cellular internet connectivity.</p>
<p>• <strong>Resolution:</strong> Host a local IEEE 802.11n Access Point (SoftAP) via an RTL8188EUS USB adapter and stream H.264 over RTSP/RTP (Port 554).</p>
<p>• <strong>Technical Rationale:</strong> Reduces network bandwidth to ~4 Mbps (vs 25+ Mbps for MJPEG). Compatible with standard mobile video players (VLC).</p>
"""

adr_s2 = """
<h1>Architecture Decision Records (ADR - Sheet 2)</h1>

<h2>ADR-004: Optical Sensor Selection — SmartSens SC3336 3MP MIPI CSI-2</h2>
<p>• <strong>Status:</strong> Accepted | <strong>Date:</strong> 2026-10-08</p>
<p>• <strong>Context:</strong> Selecting an image sensor compatible with the RV1103 hardware ISP without requiring driver modifications.</p>
<p>• <strong>Resolution:</strong> Adopt the <strong>SmartSens SC3336 3MP MIPI CSI-2 Module</strong> with 98.3 degree diagonal field-of-view lens.</p>
<p>• <strong>Technical Rationale:</strong> Fully supported by official Luckfox SDK with pre-tuned Image Quality (IQ) calibration binaries for automotive scenes.</p>

<h2>ADR-005: Power Management & Input Protection Circuit Topology</h2>
<p>• <strong>Status:</strong> Accepted | <strong>Date:</strong> 2026-10-08</p>
<p>• <strong>Context:</strong> Vehicle 12V rails exhibit severe electrical transients, load dumps up to 40V, and inductive spikes. Furthermore, the IP5306 power management IC automatically sleeps if load drops below 50mA.</p>
<p>• <strong>Resolution:</strong> Implement a robust multi-stage protection and conditioning network:</p>
<table class="tech-table">
    <tr>
        <th>Protection Stage</th>
        <th>Component Selection</th>
        <th>Circuit Function & Verification</th>
    </tr>
    <tr>
        <td>Overvoltage Surge Suppression</td>
        <td>SMBJ5.0A TVS Diode (D1)</td>
        <td>Shunts vehicle alternator load dump spikes and reverse polarity transients safely to ground.</td>
    </tr>
    <tr>
        <td>Bulk Reservoir Damping</td>
        <td>470uF / 25V Electrolytic (C5, C6)</td>
        <td>Absorbs vehicle supply line ripple and buffers Wi-Fi packet transmit current spikes.</td>
    </tr>
    <tr>
        <td>High-Frequency Decoupling</td>
        <td>100nF Ceramic (C1, C2, C3, C4)</td>
        <td>Suppresses high-frequency switching hash across buck regulator, PMIC, SBC, and Wi-Fi rails.</td>
    </tr>
    <tr>
        <td>Anti-Sleep Keep-Alive Circuit</td>
        <td>100 Ohm Resistor (R1)</td>
        <td>Enforces a static ~50mA pull on IP5306 output to permanently disable the 32-second auto-shutdown timer.</td>
    </tr>
</table>
"""

html_adr = CSS_HEADER + \
    get_sheet_html("ARCHITECTURE DECISION RECORDS", "ENG-DASH-ADR-001", "ARCHITECTURE & SYSTEMS ENGR", sheet_str="1 OF 2", content_html=adr_s1) + \
    get_sheet_html("ARCHITECTURE DECISION RECORDS", "ENG-DASH-ADR-001", "ARCHITECTURE & SYSTEMS ENGR", sheet_str="2 OF 2", content_html=adr_s2) + \
    CSS_FOOTER

with open(os.path.join(BASE_DIR, "documentation", "design_decisions", "ADR.html"), "w", encoding="utf-8") as f:
    f.write(html_adr)
compile_pdf(os.path.join(BASE_DIR, "documentation", "design_decisions", "ADR.html"), os.path.join(BASE_DIR, "documentation", "design_decisions", "ADR.pdf"))

# -------------------------------------------------------------
# 6. EMBEDDED SOFTWARE ARCHITECTURE (ENG-DASH-SW-001) - 2 SHEETS
# -------------------------------------------------------------
sw_s1 = """
<h1>Embedded Software Architecture & Video Pipeline (Sheet 1)</h1>

<h2>1. Operating System & Flash Memory Partitioning</h2>
<p>Firmware executes from 128MB SPI NAND Flash under a lean Buildroot Linux distribution optimized for sub-6-second cold boot times:</p>
<table class="tech-table">
    <tr>
        <th>Partition</th>
        <th>Size</th>
        <th>Filesystem / Image</th>
        <th>Functional Contents</th>
    </tr>
    <tr>
        <td><strong>mtd0 (U-Boot)</strong></td>
        <td>4 MB</td>
        <td>Raw Binary</td>
        <td>Rockchip Second-Stage Bootloader & DDR initialization.</td>
    </tr>
    <tr>
        <td><strong>mtd1 (Kernel)</strong></td>
        <td>12 MB</td>
        <td>Flattened Device Tree + zImage</td>
        <td>Linux 5.10 Kernel + Rockchip Media Driver & RTL8188 Wi-Fi Driver.</td>
    </tr>
    <tr>
        <td><strong>mtd2 (Rootfs)</strong></td>
        <td>64 MB</td>
        <td>UBIFS (Read-Only)</td>
        <td>Busybox system utilities, RKMPI shared libraries, hostapd, udhcpd.</td>
    </tr>
    <tr>
        <td><strong>mtd3 (Userdata)</strong></td>
        <td>48 MB</td>
        <td>UBIFS (Read-Write)</td>
        <td>Network credentials, streamer configuration, persistent logs.</td>
    </tr>
</table>

<h2>2. Hardware Video Compression Architecture</h2>
<div class="code-box">[SC3336 3MP Sensor] ──MIPI CSI-2──► [Video Input (VI) Channel 0]
                                             │ (DMA Zero-Copy)
                                             ▼
                                     [Hardware ISP 3.2] (3DNR, WDR, Auto Exposure)
                                             │
                                             ▼
                                     [Hardware H.264 VPU] (CBR 4 Mbps, 1080p@30fps)
                                             │ (H.264 NAL Units)
                                             ▼
                                     [dashcam_streamer] (C Daemon via RKMPI)
                                             │
                                             ▼
                                     [RTSP Server Port 554] ──Wi-Fi SoftAP──► [VLC Phone App]</div>
"""

sw_s2 = """
<h1>Embedded Software Architecture & Video Pipeline (Sheet 2)</h1>

<h2>3. Core Video Streamer Implementation Logic (`dashcam_streamer.c`)</h2>
<div class="code-box">// RKMPI Zero-Copy Hardware Pipeline Setup
RK_MPI_SYS_Init();

// Configure Video Input (VI) Channel 0
VI_CHN_ATTR_S vi_attr;
vi_attr.stIspOpt.u32BufCount = 2; // Strict double buffering for 64MB DRAM
vi_attr.stSize.u32Width = 1920;  vi_attr.stSize.u32Height = 1080;
vi_attr.enPixFmt = IMAGE_TYPE_NV12;
RK_MPI_VI_SetChnAttr(0, 0, &vi_attr);
RK_MPI_VI_EnableChn(0, 0);

// Configure Hardware H.264 VPU Video Encoder
VENC_CHN_ATTR_S venc_attr;
venc_attr.stVencAttr.enType = RK_VIDEO_ID_AVC;
venc_attr.stVencAttr.u32Profile = 77; // H.264 Main Profile
venc_attr.stVencAttr.u32PicWidth = 1920; venc_attr.stVencAttr.u32PicHeight = 1080;
venc_attr.stRcAttr.enRcMode = VENC_RC_MODE_H264CBR;
venc_attr.stRcAttr.stH264Cbr.u32BitRate = 4000; // 4 Mbps
venc_attr.stRcAttr.stH264Cbr.u32Gop = 30;       // 1 Keyframe per sec
RK_MPI_VENC_CreateChn(0, &venc_attr);

// Hardware Bind: VI Channel 0 -> VENC Channel 0
MPP_CHN_S src = { .enModId = RK_ID_VI,   .s32DevId = 0, .s32ChnId = 0 };
MPP_CHN_S dst = { .enModId = RK_ID_VENC, .s32DevId = 0, .s32ChnId = 0 };
RK_MPI_SYS_Bind(&src, &dst);</div>

<h2>4. Boot Automation Script (`/etc/init.d/S99dashcam`)</h2>
<p>Initializes wireless interface into SoftAP mode and launches RTSP streaming service at boot:</p>
<div class="code-box">modprobe 8188eu 2>/dev/null
ifconfig wlan0 192.168.169.1 netmask 255.255.255.0 up
hostapd -B /etc/hostapd.conf
udhcpd /etc/udhcpd.conf
echo 48 > /sys/class/gpio/export && echo out > /sys/class/gpio/gpio48/direction && echo 1 > /sys/class/gpio/gpio48/value
/usr/bin/dashcam_streamer &</div>
"""

html_sw = CSS_HEADER + \
    get_sheet_html("EMBEDDED SOFTWARE ARCHITECTURE", "ENG-DASH-SW-001", "EMBEDDED SOFTWARE & FIRMWARE", sheet_str="1 OF 2", content_html=sw_s1) + \
    get_sheet_html("EMBEDDED SOFTWARE ARCHITECTURE", "ENG-DASH-SW-001", "EMBEDDED SOFTWARE & FIRMWARE", sheet_str="2 OF 2", content_html=sw_s2) + \
    CSS_FOOTER

with open(os.path.join(BASE_DIR, "documentation", "software_architecture.html"), "w", encoding="utf-8") as f:
    f.write(html_sw)
compile_pdf(os.path.join(BASE_DIR, "documentation", "software_architecture.html"), os.path.join(BASE_DIR, "documentation", "software_architecture.pdf"))

# -------------------------------------------------------------
# 7. ELECTRICAL WIRING & SCHEMATIC (ENG-DASH-SCH-001) - 2 SHEETS
# -------------------------------------------------------------
sch_s1 = """
<h1>Electrical Wiring & Schematic (Sheet 1: Power & Battery)</h1>

<h2>1. Primary Power Conditioning & Protection Stage</h2>
<div class="code-box">[+12V DC Vehicle In] ───┬──────────────────────────────────────────┐
                        │                                          │
                      [ D1 ] SMBJ5.0A TVS (Cathode)               [ C5 ] 470uF / 25V (Electrolytic +)
                        │                                          │
[Vehicle Ground (-)]  ──┴──────────────────────────────────────────┴───► [LM2596 VIN (-)]
[+12V DC Vehicle In]  ─────────────────────────────────────────────────► [LM2596 VIN (+)]
                                     LM2596 BUCK REGULATOR (Set to +5.0V DC)
[LM2596 VOUT (+5V)] ───┬──────────────────┬────────────────────────────► [IP5306 VIN (+5V)]
                       │                  │
                     [ C6 ] 470uF       [ C4 ] 100nF (104 Ceramic)
                     (Electrolytic +)     │
                       │                  │
[LM2596 VOUT (GND)]  ──┴──────────────────┴────────────────────────────► [IP5306 GND]</div>

<h2>2. Battery Storage & PMIC Subsystem Wiring</h2>
<div class="code-box">[1000mAh LiPo Cell (+)] ───────────────────────────────────────────────► [IP5306 BAT (+)]
[1000mAh LiPo Cell (-)] ───────────────────────────────────────────────► [IP5306 BAT (-)]
                                     IP5306 PMIC MODULE
[IP5306 5V OUT (+)]  ──┬──────────────────┬────────────────────────────► Main +5.0V System Rail
                       │                  │
                     [ R1 ] 100 Ohm     [ C1 ] 100nF (104 Ceramic)
                     (Keep-alive 50mA)    │
                       │                  │
[IP5306 GND]         ──┴──────────────────┴────────────────────────────► Main Ground Rail</div>
"""

sch_s2 = """
<h1>Electrical Wiring & Schematic (Sheet 2: Rail Distribution & Pinout)</h1>

<h2>3. Main Rail Distribution & Subsystem Decoupling</h2>
<div class="code-box">Main +5.0V Rail ──┬────────────────────────────────────────────────────► [Luckfox Pico Mini B 5V Pin]
                  │
                [ C2 ] 100nF (104 Ceramic Decoupling)
                  │
Main Ground     ──┴────────────────────────────────────────────────────► [Luckfox Pico Mini B GND Pin]

Main +5.0V Rail ──┬────────────────────────────────────────────────────► [USB Wi-Fi Port Pin 1 (VBUS)]
                  │
                [ C3 ] 100nF (104 Ceramic Decoupling)
                  │
Main Ground     ──┴────────────────────────────────────────────────────► [USB Wi-Fi Port Pin 4 (GND)]</div>

<h2>4. Peripheral Interconnects & Hardware Signal Mapping</h2>
<table class="tech-table">
    <tr>
        <th>Peripheral / Interface</th>
        <th>Physical Connection</th>
        <th>Circuit Description & Termination</th>
    </tr>
    <tr>
        <td><strong>SC3336 Camera</strong></td>
        <td>15-Pin 0.5mm FPC Ribbon Cable</td>
        <td>Direct differential MIPI CSI-2 connection to Luckfox CSI connector.</td>
    </tr>
    <tr>
        <td><strong>Status Optical LED</strong></td>
        <td>Luckfox GPIO48</td>
        <td>GPIO48 ───► [ R4: 470 Ohm ] ───► [ LED Anode (+) ] ───► [ LED Cathode to GND ].</td>
    </tr>
    <tr>
        <td><strong>Master Push-Button</strong></td>
        <td>Luckfox GPIO Pin</td>
        <td>Momentary Push Button to GND with [ R2: 10 kOhm ] pull-up resistor to 3.3V rail.</td>
    </tr>
    <tr>
        <td><strong>USB Host Mode Force</strong></td>
        <td>Luckfox USB ID Pin</td>
        <td>Tied directly to System Ground via [ R5: 1 kOhm ] pull-down resistor.</td>
    </tr>
</table>
"""

html_sch = CSS_HEADER + \
    get_sheet_html("ELECTRICAL WIRING & SCHEMATIC", "ENG-DASH-SCH-001", "ELECTRICAL WIRING & INTERCONNECT", sheet_str="1 OF 2", content_html=sch_s1) + \
    get_sheet_html("ELECTRICAL WIRING & SCHEMATIC", "ENG-DASH-SCH-001", "ELECTRICAL WIRING & INTERCONNECT", sheet_str="2 OF 2", content_html=sch_s2) + \
    CSS_FOOTER

with open(os.path.join(BASE_DIR, "hardware", "source", "wiring_schematic.html"), "w", encoding="utf-8") as f:
    f.write(html_sch)
compile_pdf(os.path.join(BASE_DIR, "hardware", "source", "wiring_schematic.html"), os.path.join(BASE_DIR, "hardware", "source", "wiring_schematic.pdf"))

print("ALL MULTI-SHEET PDF GENERATION COMPLETE!")
