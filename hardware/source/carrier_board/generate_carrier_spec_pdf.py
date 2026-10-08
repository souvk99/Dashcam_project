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

spec_s1 = """
<h1>Carrier Board Specification: Hardware Architecture & Net Schedule</h1>

<h2>1. Carrier Board Design Objective & Functional Subsystems</h2>
<p>The Dashcam Carrier Board (ENG-DASH-PCB-001) serves as the central electro-mechanical backplane integrating the <strong>Luckfox Pico Mini B SBC (RV1103)</strong>, <strong>SmartSens SC3336 3MP Camera</strong>, <strong>1000mAh LiPo Battery</strong>, <strong>IP5306 BMS Module</strong>, and automotive power conditioning.</p>

<div class="code-box">                                 DASHCAM CARRIER BOARD TOPOLOGY
┌───────────────────────────┐     ┌────────────────────────────┐     ┌────────────────────────────┐
│ 12V VEHICLE POWER IN (J1) │ ──► │ LM2596 STEP-DOWN BUCK (U1) │ ──► │ IP5306 BMS & CHARGER (U2)  │
│ SMBJ5.0A TVS + 470uF Cap  │     │ 12V DC -> 5.0V Pre-Reg     │     │ + 1000mAh LiPo Cell (J2)   │
└───────────────────────────┘     └────────────────────────────┘     └─────────────┬──────────────┘
                                                                                   │ +5V_SYS Main Rail
                                                                                   ▼
┌───────────────────────────┐     ┌────────────────────────────┐     ┌────────────────────────────┐
│ SC3336 3MP CAMERA (J5)    │ ◄── │ LUCKFOX PICO MINI B (J3/J4)│ ──► │ USB 2.0 WI-FI DONGLE (J7)  │
│ 15-Pin 0.5mm FPC MIPI CSI │     │ RV1103 SoC + 128MB NAND    │     │ RTL8188EUS SoftAP (4 Mbps) │
└───────────────────────────┘     └─────────────┬──────────────┘     └────────────────────────────┘
                                                │
                                                ▼
                                  ┌────────────────────────────┐
                                  │ USER INTERFACE CONTROLS    │
                                  │ Status LED (D2) + SW1 Tact │
                                  └────────────────────────────┘</div>

<h2>2. Subsystem Net Interconnect & Decoupling Matrix</h2>
<table class="tech-table">
    <tr>
        <th>Subsystem Block</th>
        <th>Ref Des</th>
        <th>Component / Connector</th>
        <th>Key Signals / Power Rails</th>
        <th>Decoupling & Protection</th>
    </tr>
    <tr>
        <td><strong>Automotive In</strong></td>
        <td>J1, D1, C1</td>
        <td>Terminal Block 2-Pin 5.08mm</td>
        <td>+12V_IN, GND</td>
        <td>SMBJ5.0A TVS + 470uF/25V Electrolytic Reservoir</td>
    </tr>
    <tr>
        <td><strong>Pre-Regulator</strong></td>
        <td>U1, C2, C3</td>
        <td>LM2596 DC-DC Step-Down Module</td>
        <td>+12V_IN -> +5V_PRE (Pre-regulated 5V)</td>
        <td>470uF/25V Reservoir + 100nF Ceramic Decoupling</td>
    </tr>
    <tr>
        <td><strong>BMS & Battery</strong></td>
        <td>U2, J2, R1, C4, C5</td>
        <td>IP5306 Synchronous PMIC + JST-PH</td>
        <td>VBAT (+3.7V LiPo), +5V_PRE In, +5V_SYS Out</td>
        <td>R1 (100 Ohm) Keep-Alive Dummy Load + 100nF Decoupling</td>
    </tr>
    <tr>
        <td><strong>SBC Sockets</strong></td>
        <td>J3, J4, C6, C7</td>
        <td>2x 1x08 2.54mm Female Sockets</td>
        <td>+5V_SYS, +3V3, UART2, I2C3, USB, GPIOs</td>
        <td>100nF MLCC at +5V_SYS (J4) and +3V3 (J3)</td>
    </tr>
    <tr>
        <td><strong>Camera MIPI</strong></td>
        <td>J5, C8</td>
        <td>15-Pin 0.5mm FPC Bottom-Contact</td>
        <td>MIPI_D0_P/N, MIPI_CLK_P/N, MIPI_D1_P/N, SCCB</td>
        <td>100nF Decoupling on Sensor 3.3V Supply Rail</td>
    </tr>
    <tr>
        <td><strong>Wi-Fi Dongle</strong></td>
        <td>J7, C9</td>
        <td>USB Type-A Female Receptacle</td>
        <td>+5V_SYS (VBUS), USB_DM (D-), USB_DP (D+), GND</td>
        <td>100nF MLCC Decoupling directly across VBUS/GND</td>
    </tr>
    <tr>
        <td><strong>User Interface</strong></td>
        <td>SW1, R2, D2, R3</td>
        <td>Tactile Switch + 0805 Green LED</td>
        <td>SW_SENSE (GPIO34), STAT_LED (GPIO48)</td>
        <td>R2 (10k Pull-up), R3 (470 Ohm LED Current Limiting)</td>
    </tr>
</table>
"""

spec_s2 = """
<h1>Carrier Board Specification: Pinout Schedules & PCB Layout Rules</h1>

<h2>3. Comprehensive Connector Pinout Schedule</h2>
<table class="tech-table">
    <tr>
        <th style="width: 15%;">Connector</th>
        <th style="width: 10%;">Pin Number</th>
        <th style="width: 25%;">Net Designation</th>
        <th style="width: 20%;">Signal Standard</th>
        <th style="width: 30%;">Functional Description</th>
    </tr>
    <tr>
        <td><strong>J1 (12V Input)</strong></td>
        <td>Pin 1 / 2</td>
        <td>+12V_IN / GND</td>
        <td>Automotive 12V DC</td>
        <td>Vehicle ignition / accessory electrical line entry.</td>
    </tr>
    <tr>
        <td><strong>J2 (LiPo Batt)</strong></td>
        <td>Pin 1 / 2</td>
        <td>VBAT / GND</td>
        <td>Lithium Polymer (3.7V - 4.2V)</td>
        <td>1000mAh battery cell buffer with integrated PCM.</td>
    </tr>
    <tr>
        <td><strong>J3 (SBC Left)</strong></td>
        <td>Pins 1 to 8</td>
        <td>UART2_TX, RX, GND, +3V3, I2C3_SCL, SDA, GND, STAT_LED</td>
        <td>LVCMOS 3.3V Logic</td>
        <td>Console debug, peripheral power, camera SCCB, LED drive.</td>
    </tr>
    <tr>
        <td><strong>J4 (SBC Right)</strong></td>
        <td>Pins 1 to 8</td>
        <td>+5V_SYS, GND, USB_DM, USB_DP, CAM_RSTn, CAM_PDN, SW_SENSE, GND</td>
        <td>USB 2.0 / DC Power</td>
        <td>Main 5V system entry, USB host signals, camera control.</td>
    </tr>
    <tr>
        <td><strong>J5 (Camera FPC)</strong></td>
        <td>Pins 1 to 15</td>
        <td>GND, D0_N/P, GND, CLK_N/P, GND, D1_N/P, GND, RST, PDN, SCL, SDA, 3V3</td>
        <td>MIPI D-PHY (800 Mbps/lane)</td>
        <td>SmartSens SC3336 3MP raw Bayer image sensor link.</td>
    </tr>
    <tr>
        <td><strong>J7 (Wi-Fi USB)</strong></td>
        <td>Pins 1 to 4</td>
        <td>+5V_SYS, USB_DM, USB_DP, GND</td>
        <td>USB 2.0 High-Speed</td>
        <td>RTL8188EUS 802.11n Wi-Fi adapter receptacle.</td>
    </tr>
</table>

<h2>4. High-Speed PCB Layout Guidelines & Physical Constraints</h2>
<p>• <strong>MIPI CSI-2 Differential Pairs:</strong> Route MIPI_D0, MIPI_CLK, and MIPI_D1 as 100 Ohm differential controlled impedance microstrips over an unbroken solid ground plane (Layer 2). Keep intra-pair length skew below 0.5 mm (20 mils) and inter-pair skew below 1.5 mm.</p>
<p>• <strong>USB 2.0 Differential Routing:</strong> Route USB_DM and USB_DP as 90 Ohm differential pairs. Avoid via transitions between SBC and USB-A receptacle.</p>
<p>• <strong>Power Distribution:</strong> Form a wide polygon pour for +5V_SYS and +12V_IN rails (>35 mil trace width or plane pour) to minimize IR drop during Wi-Fi transmission bursts (up to 805 mA peak system draw).</p>
<p>• <strong>Physical Dimensions & Mounting:</strong> Form factor: 60.0 mm x 38.0 mm, 2-layer FR4, 1.6 mm thickness, 1 oz copper. Features 4x M2.5 mounting holes on a 53.0 mm x 31.0 mm rectangle matching the enclosure standoffs.</p>
<p>• <strong>Manufacturing Gerbers & 3D Renders:</strong> Production Gerbers (F_Cu, B_Cu, F_SilkS, B_SilkS, F_Mask, B_Mask, Edge_Cuts, Drill) exported to <code>hardware/source/carrier_board/gerbers/</code>. High-resolution raytraced 3D renders available in <code>hardware/source/carrier_board/carrier_board_3d_top.png</code> and <code>carrier_board_3d_iso.png</code>.</p>
<p>• <strong>KiCad 10 Project Assets:</strong> Fully editable KiCad project files located in <code>hardware/source/carrier_board/</code> (<code>carrier_board.kicad_pro</code>, <code>carrier_board.kicad_sch</code>, <code>carrier_board.kicad_pcb</code>, <code>carrier_board_schematic.pdf</code>, <code>carrier_board_top_layer.pdf</code>, <code>carrier_board_bottom_layer.pdf</code>).</p>
"""

html_carrier_spec = CSS_HEADER + \
    get_sheet_html("CARRIER BOARD HARDWARE SPEC", "ENG-DASH-PCB-001", "EMBEDDED HARDWARE & PCB DESIGN", sheet_str="1 OF 2", content_html=spec_s1) + \
    get_sheet_html("CARRIER BOARD HARDWARE SPEC", "ENG-DASH-PCB-001", "EMBEDDED HARDWARE & PCB DESIGN", sheet_str="2 OF 2", content_html=spec_s2) + \
    CSS_FOOTER

out_html = os.path.join(BASE_DIR, "hardware", "source", "carrier_board_spec.html")
out_pdf = os.path.join(BASE_DIR, "hardware", "source", "carrier_board_spec.pdf")

with open(out_html, "w", encoding="utf-8") as f:
    f.write(html_carrier_spec)

compile_pdf(out_html, out_pdf)
print("[OK] Carrier board specification PDF generated successfully!")
