import os
import sys
import subprocess

BASE_DIR = r"C:\Users\souvk\Downloads\Dashcam_project"
sys.path.append(os.path.join(BASE_DIR, "documentation"))
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

# -------------------------------------------------------------------------
# 1. SBC SCHEMATICS: LUCKFOX PICO MINI B (RV1103) - 2 SHEETS
# -------------------------------------------------------------------------
sbc_s1 = """
<h1>SBC Schematic Sheet 1: RV1103 Core, Power Tree & Clocking</h1>

<h2>1. Rockchip RV1103 Core Processing & Power Distribution Topology</h2>
<div class="code-box">                        ROCKCHIP RV1103 SINGLE-CHIP VISION PROCESSOR
                        ┌────────────────────────────────────────────────────────┐
                        │                 ARM Cortex-A7 @ 1.2 GHz                │
                        │                 + RISC-V Microcontroller               │
                        ├────────────────────────────────────────────────────────┤
[5.0V VBUS In] ─────────► VCC_SYS (5.0V)                                         │
                        │   │                                                    │
                        │   ├──► SY8089 Buck LDO ──► VDD_ARM_LOG (0.9V - 1.05V)   │
                        │   ├──► Fixed LDO       ──► VCC_DDR (1.8V DDR2 Rail)    │
                        │   ├──► Fixed LDO       ──► VCC_IO  (3.3V Digital I/O)  │
                        │   └──► Analogue LDO    ──► AVDD_1V8 (1.8V MIPI/ADC)    │
                        ├────────────────────────────────────────────────────────┤
[24 MHz Crystal] ───────► OSC_IN / OSC_OUT (System PLL Master Clock)            │
[Reset Circuit]  ───────► RESETn (Active Low System Reset with 10k Pull-Up)      │
                        └────────────────────────────────────────────────────────┘</div>

<h2>2. Power Tree Voltage Rail Schedule</h2>
<table class="tech-table">
    <tr>
        <th>Net Name</th>
        <th>Regulator IC</th>
        <th>Nominal Voltage</th>
        <th>Target Subsystem Node</th>
        <th>Decoupling Capacitors</th>
    </tr>
    <tr>
        <td><strong>VCC_SYS</strong></td>
        <td>External Input (5.0V Pin)</td>
        <td>5.0V DC (4.75V - 5.25V)</td>
        <td>Main system power entry rail, USB VBUS input</td>
        <td>10uF Tantalum + 100nF Ceramic</td>
    </tr>
    <tr>
        <td><strong>VDD_CORE</strong></td>
        <td>Internal DC-DC (SY8089)</td>
        <td>0.90V - 1.05V DC (DVFS)</td>
        <td>ARM Cortex-A7 CPU core, NPU matrix, ISP logic</td>
        <td>22uF MLCC + 4x 100nF Ceramic</td>
    </tr>
    <tr>
        <td><strong>VCC_DDR</strong></td>
        <td>Internal Step-Down LDO</td>
        <td>1.8V DC (DDR2 Level)</td>
        <td>On-chip 64MB DDR2 memory array & PHY</td>
        <td>10uF MLCC + 2x 100nF Ceramic</td>
    </tr>
    <tr>
        <td><strong>VCC_IO</strong></td>
        <td>Internal Step-Down LDO</td>
        <td>3.3V DC (+/- 5%)</td>
        <td>GPIO headers, SPI NAND bus, I2C, UART peripherals</td>
        <td>10uF MLCC + 100nF Ceramic</td>
    </tr>
    <tr>
        <td><strong>AVDD_1V8</strong></td>
        <td>Low-Noise Analogue LDO</td>
        <td>1.80V DC Filtered</td>
        <td>MIPI CSI-2 D-PHY receiver, internal PLL oscillators</td>
        <td>4.7uF MLCC + 100nF Ceramic</td>
    </tr>
</table>
"""

sbc_s2 = """
<h1>SBC Schematic Sheet 2: 128MB SPI NAND, MIPI CSI & USB Interfaces</h1>

<h2>3. 128MB SPI NAND Flash & MIPI CSI-2 Camera Connector Interconnect</h2>
<div class="code-box">          128MB SPI NAND FLASH (W25N01GV)                 15-PIN 0.5mm MIPI CSI-2 FPC CONNECTOR
          ┌─────────────────────────────┐                 ┌─────────────────────────────────┐
RV1103    │                             │                 │ Pin 1: GND                      │
FSPI_CLK ─┼─► CLK (Pin 6)               │       RV1103    │ Pin 2: MIPI_RX_D0_N (Lane 0 -)  │
FSPI_CS0 ─┼─► /CS (Pin 1)               │  MIPI_D0_N ─────┼─► Pin 3: MIPI_RX_D0_P (Lane 0 +)  │
FSPI_D0  ─┼─► DI / IO0 (Pin 5)          │  MIPI_D0_P ─────┼─► Pin 4: GND                    │
FSPI_D1  ─┼─► DO / IO1 (Pin 2)          │  MIPI_CLK_N ────┼─► Pin 5: MIPI_RX_CLK_N (Clock -)│
FSPI_D2  ─┼─► /WP / IO2 (Pin 3)         │  MIPI_CLK_P ────┼─► Pin 6: MIPI_RX_CLK_P (Clock +)│
FSPI_D3  ─┼─► /HOLD / IO3 (Pin 7)       │                 │ Pin 7: GND                      │
          │ VCC (3.3V, Pin 8) ──► 100nF │  MIPI_D1_N ─────┼─► Pin 8: MIPI_RX_D1_N (Lane 1 -)  │
          │ GND (Pin 4)                 │  MIPI_D1_P ─────┼─► Pin 9: MIPI_RX_D1_P (Lane 1 +)  │
          └─────────────────────────────┘                 │ Pin 10: GND                     │
                                                   GPIO   │ Pin 11: CAM_RSTn (Sensor Reset) │
          USB 2.0 HIGH-SPEED HOST PORT             GPIO   │ Pin 12: CAM_PDN (Power Down)    │
          ┌─────────────────────────────┐        I2C_SCL ─┼─► Pin 13: I2C3_SCL (SCCB Clock) │
RV1103    │ Pin 1: VBUS (+5.0V DC)      │        I2C_SDA ─┼─► Pin 14: I2C3_SDA (SCCB Data)  │
USB_DM  ──┼─► Pin 2: Data Negative (D-) │                 │ Pin 15: VCC_3V3 (Sensor Power)  │
USB_DP  ──┼─► Pin 3: Data Positive (D+) │                 └─────────────────────────────────┘
          │ Pin 4: GND (System Ground)  │
          └─────────────────────────────┘</div>

<h2>4. Board Pinout & Peripheral Mapping Summary</h2>
<table class="tech-table">
    <tr>
        <th>Header Pin</th>
        <th>Default GPIO</th>
        <th>Multiplexed Signal</th>
        <th>Target Function in Dashcam Project</th>
    </tr>
    <tr>
        <td><strong>Pin 1</strong></td>
        <td>GPIO1_C7</td>
        <td>UART2_TX</td>
        <td>Serial Debug Console (115200 / 1.5Mbps)</td>
    </tr>
    <tr>
        <td><strong>Pin 2</strong></td>
        <td>GPIO1_C6</td>
        <td>UART2_RX</td>
        <td>Serial Debug Console (Receive)</td>
    </tr>
    <tr>
        <td><strong>Pin 5</strong></td>
        <td>GPIO1_D2</td>
        <td>I2C3_SCL</td>
        <td>SC3336 Camera Configuration Clock</td>
    </tr>
    <tr>
        <td><strong>Pin 6</strong></td>
        <td>GPIO1_D3</td>
        <td>I2C3_SDA</td>
        <td>SC3336 Camera Configuration Data</td>
    </tr>
    <tr>
        <td><strong>Pin 10</strong></td>
        <td>GPIO1_B0</td>
        <td>GPIO48</td>
        <td>Status Optical LED Drive (via 470 Ohm)</td>
    </tr>
    <tr>
        <td><strong>Pin 14</strong></td>
        <td>GPIO1_A2</td>
        <td>GPIO34</td>
        <td>Tactile Power / Mode Button (with 10k Pull-Up)</td>
    </tr>
    <tr>
        <td><strong>Pin 19, 20</strong></td>
        <td>5V_IN, GND</td>
        <td>VCC_SYS, GND</td>
        <td>Primary System DC Power Connection from PMIC</td>
    </tr>
</table>
"""

html_sbc = CSS_HEADER + \
    get_sheet_html("SBC SCHEMATICS SPECIFICATION", "ENG-DASH-SBC-SCH-001", "EMBEDDED HARDWARE & SCHEMATICS", sheet_str="1 OF 2", content_html=sbc_s1) + \
    get_sheet_html("SBC SCHEMATICS SPECIFICATION", "ENG-DASH-SBC-SCH-001", "EMBEDDED HARDWARE & SCHEMATICS", sheet_str="2 OF 2", content_html=sbc_s2) + \
    CSS_FOOTER

sbc_html_path = os.path.join(BASE_DIR, "hardware", "source", "sbc_schematics.html")
sbc_pdf_path = os.path.join(BASE_DIR, "hardware", "source", "sbc_schematics.pdf")

with open(sbc_html_path, "w", encoding="utf-8") as f:
    f.write(html_sbc)
compile_pdf(sbc_html_path, sbc_pdf_path)

# -------------------------------------------------------------------------
# 2. CAMERA SCHEMATICS: SMARTSENS SC3336 3MP MODULE - 2 SHEETS
# -------------------------------------------------------------------------
cam_s1 = """
<h1>Camera Module Schematics: SmartSens SC3336 (Sheet 1)</h1>

<h2>1. Optical Sensor Core Circuit & Architecture</h2>
<div class="code-box">                          SMARTSENS SC3336 3MP CMOS IMAGE SENSOR (1/2.8")
                          ┌────────────────────────────────────────────────────────┐
                          │               High-Dynamic Range Pixel Array           │
                          │                     (2304 x 1296 @ 30fps)              │
                          ├────────────────────────────────────────────────────────┤
[3.3V DC In] ─────────────► AVDD_2V8 LDO (Low-Noise RT9013) ──► AVDD (2.8V Analogue)│
                          │   ├──► Decoupling: 4.7uF Tantalum + 100nF Ceramic      │
                          │ DOVDD (1.8V Digital I/O) ───► From Luckfox Onboard LDO │
                          │ DVDD (1.2V Digital Core) ───► Internal Core Regulator  │
                          ├────────────────────────────────────────────────────────┤
[24 MHz MCLK] ────────────► EXTCLK (Master Pixel Clock from RV1103)               │
[I2C Control] ────────────► SCL / SDA (SCCB Protocol, 400kHz, Slave Addr: 0x3C)   │
                          ├────────────────────────────────────────────────────────┤
                          │ MIPI CSI-2 D-PHY Differential Output Stage (2-Lane):   │
                          │   Lane 0: MDP0 / MDN0 ──► (Differential Pixel Pair 0)  │
                          │   Lane 1: MDP1 / MDN1 ──► (Differential Pixel Pair 1)  │
                          │   Clock:  MCP / MCN   ──► (Differential Clock Pair)    │
                          └────────────────────────────────────────────────────────┘</div>

<h2>2. Optical & Electrical Operating Parameters</h2>
<table class="tech-table">
    <tr>
        <th>Parameter</th>
        <th>Specification</th>
        <th>Engineering Note</th>
    </tr>
    <tr>
        <td><strong>Optical Format</strong></td>
        <td>1/2.8-inch Progressive Scan CMOS</td>
        <td>High-sensitivity pixel architecture for automotive night vision.</td>
    </tr>
    <tr>
        <td><strong>Active Resolution</strong></td>
        <td>2304 (H) x 1296 (V) pixels (3.0 Megapixels)</td>
        <td>Captures 1080p Full HD with zero scaling loss and 2K capability.</td>
    </tr>
    <tr>
        <td><strong>Pixel Size</strong></td>
        <td>2.0 um x 2.0 um BSI Technology</td>
        <td>High signal-to-noise ratio (SNR) with low dark-current noise.</td>
    </tr>
    <tr>
        <td><strong>Output Interface</strong></td>
        <td>MIPI CSI-2 (2-lane, D-PHY specification)</td>
        <td>Differential signaling up to 800 Mbps per data lane.</td>
    </tr>
    <tr>
        <td><strong>Supply Rails</strong></td>
        <td>AVDD: 2.8V, DOVDD: 1.8V, DVDD: 1.2V</td>
        <td>Filtered via low-noise LDOs and ferrite bead decoupling.</td>
    </tr>
</table>
"""

cam_s2 = """
<h1>Camera Module Schematics: FPC Pinout & Interconnect (Sheet 2)</h1>

<h2>3. 15-Pin 0.5mm Pitch FPC Connector Pin Assignment & Signal Definition</h2>
<table class="tech-table">
    <tr>
        <th style="width: 8%;">Pin</th>
        <th style="width: 15%;">Pin Name</th>
        <th style="width: 15%;">Signal Type</th>
        <th style="width: 15%;">Voltage Level</th>
        <th style="width: 47%;">Description & Interconnect Details</th>
    </tr>
    <tr>
        <td><strong>1</strong></td>
        <td>GND</td>
        <td>Power Ground</td>
        <td>0V</td>
        <td>System Ground return and shielding plane.</td>
    </tr>
    <tr>
        <td><strong>2</strong></td>
        <td>MIPI_D0_N</td>
        <td>MIPI D-PHY Out</td>
        <td>+/- 200mV Diff</td>
        <td>MIPI CSI-2 Data Lane 0 Negative Differential Signal.</td>
    </tr>
    <tr>
        <td><strong>3</strong></td>
        <td>MIPI_D0_P</td>
        <td>MIPI D-PHY Out</td>
        <td>+/- 200mV Diff</td>
        <td>MIPI CSI-2 Data Lane 0 Positive Differential Signal.</td>
    </tr>
    <tr>
        <td><strong>4</strong></td>
        <td>GND</td>
        <td>Power Ground</td>
        <td>0V</td>
        <td>Isolation ground between Data 0 and Clock lanes.</td>
    </tr>
    <tr>
        <td><strong>5</strong></td>
        <td>MIPI_CLK_N</td>
        <td>MIPI D-PHY Out</td>
        <td>+/- 200mV Diff</td>
        <td>MIPI CSI-2 Clock Negative Differential Signal.</td>
    </tr>
    <tr>
        <td><strong>6</strong></td>
        <td>MIPI_CLK_P</td>
        <td>MIPI D-PHY Out</td>
        <td>+/- 200mV Diff</td>
        <td>MIPI CSI-2 Clock Positive Differential Signal.</td>
    </tr>
    <tr>
        <td><strong>7</strong></td>
        <td>GND</td>
        <td>Power Ground</td>
        <td>0V</td>
        <td>Isolation ground between Clock and Data 1 lanes.</td>
    </tr>
    <tr>
        <td><strong>8</strong></td>
        <td>MIPI_D1_N</td>
        <td>MIPI D-PHY Out</td>
        <td>+/- 200mV Diff</td>
        <td>MIPI CSI-2 Data Lane 1 Negative Differential Signal.</td>
    </tr>
    <tr>
        <td><strong>9</strong></td>
        <td>MIPI_D1_P</td>
        <td>MIPI D-PHY Out</td>
        <td>+/- 200mV Diff</td>
        <td>MIPI CSI-2 Data Lane 1 Positive Differential Signal.</td>
    </tr>
    <tr>
        <td><strong>10</strong></td>
        <td>GND</td>
        <td>Power Ground</td>
        <td>0V</td>
        <td>Digital signal ground shielding plane.</td>
    </tr>
    <tr>
        <td><strong>11</strong></td>
        <td>CAM_RSTn</td>
        <td>Digital Input</td>
        <td>3.3V / 1.8V</td>
        <td>Active-low sensor hardware reset line (driven by RV1103).</td>
    </tr>
    <tr>
        <td><strong>12</strong></td>
        <td>CAM_PDN</td>
        <td>Digital Input</td>
        <td>3.3V / 1.8V</td>
        <td>Sensor power-down control line (pulled low for active state).</td>
    </tr>
    <tr>
        <td><strong>13</strong></td>
        <td>I2C_SCL</td>
        <td>Bidirectional</td>
        <td>3.3V Open-Drain</td>
        <td>SCCB register programming clock with 2.2k pull-up to 3.3V.</td>
    </tr>
    <tr>
        <td><strong>14</strong></td>
        <td>I2C_SDA</td>
        <td>Bidirectional</td>
        <td>3.3V Open-Drain</td>
        <td>SCCB register programming data with 2.2k pull-up to 3.3V.</td>
    </tr>
    <tr>
        <td><strong>15</strong></td>
        <td>VCC_3V3</td>
        <td>Power Feed</td>
        <td>3.3V DC (+/- 5%)</td>
        <td>Main power feed to onboard 2.8V AVDD low-noise LDO regulator.</td>
    </tr>
</table>

<h2>4. Signal Integrity & Layout Constraints</h2>
<p>• Differential impedance for MIPI data and clock pairs: 100 Ohm (+/- 10%) differential.</p>
<p>• Intra-pair length matching: skew less than 0.5mm between positive and negative traces.</p>
<p>• Dedicated solid ground reference plane directly beneath all MIPI differential routing.</p>
"""

html_cam = CSS_HEADER + \
    get_sheet_html("CAMERA SCHEMATICS SPECIFICATION", "ENG-DASH-CAM-SCH-001", "OPTICAL SENSORS & SCHEMATICS", sheet_str="1 OF 2", content_html=cam_s1) + \
    get_sheet_html("CAMERA SCHEMATICS SPECIFICATION", "ENG-DASH-CAM-SCH-001", "OPTICAL SENSORS & SCHEMATICS", sheet_str="2 OF 2", content_html=cam_s2) + \
    CSS_FOOTER

cam_html_path = os.path.join(BASE_DIR, "hardware", "source", "cam_schematics.html")
cam_pdf_path = os.path.join(BASE_DIR, "hardware", "source", "cam_schematics.pdf")

with open(cam_html_path, "w", encoding="utf-8") as f:
    f.write(html_cam)
compile_pdf(cam_html_path, cam_pdf_path)

print("SCHEMATIC PDF GENERATION COMPLETE!")
