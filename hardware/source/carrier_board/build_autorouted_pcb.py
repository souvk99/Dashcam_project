import os
import uuid
import subprocess
import re

BASE_DIR = r"C:\Users\souvk\Downloads\Dashcam_project"
CARRIER_DIR = os.path.join(BASE_DIR, "hardware", "source", "carrier_board")
KICAD_CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
JAVA_EXE = r"C:\Users\souvk\jre-25\jdk-25.0.4.1+1-jre\bin\java.exe"
FREEROUTING_JAR = r"C:\Users\souvk\AppData\Roaming\kicad\10.0\scripting\plugins\kicad_ai_assistant\freerouting-2.2.3.jar"

def uid():
    return str(uuid.uuid4())

# Board Dimensions: 65.0 x 42.0 mm (Origin at 100, 80)
X0 = 100.0
Y0 = 80.0
BW = 65.0
BH = 42.0

def generate_pcb():
    # Net definitions with standard indexing
    nets = [
        (0, ""),
        (1, "GND"),
        (2, "+12V"),
        (3, "+5V_PRE"),
        (4, "VBAT"),
        (5, "+5V_SYS"),
        (6, "+3V3"),
        (7, "MIPI_D0_P"),
        (8, "MIPI_D0_N"),
        (9, "MIPI_CLK_P"),
        (10, "MIPI_CLK_N"),
        (11, "MIPI_D1_P"),
        (12, "MIPI_D1_N"),
        (13, "I2C3_SCL"),
        (14, "I2C3_SDA"),
        (15, "CAM_RSTn"),
        (16, "CAM_PDN"),
        (17, "USB_DP"),
        (18, "USB_DM"),
        (19, "STAT_LED"),
        (20, "SW_SENSE"),
        (21, "UART2_TX"),
        (22, "UART2_RX"),
        (23, "Net-(D2-A)")
    ]

    net_map = {name: nid for nid, name in nets if name}
    net_lines = "\n".join([f'\t(net {nid} "{nname}")' for nid, nname in nets])

    # Board Outline (Edge.Cuts) with rounded corners (r=2.5 mm)
    r = 2.5
    x1, y1 = X0, Y0
    x2, y2 = X0 + BW, Y0 + BH
    edge_cuts = [
        f'\t(gr_line (start {x1+r} {y1}) (end {x2-r} {y1}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{uid()}"))',
        f'\t(gr_line (start {x2} {y1+r}) (end {x2} {y2-r}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{uid()}"))',
        f'\t(gr_line (start {x2-r} {y2}) (end {x1+r} {y2}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{uid()}"))',
        f'\t(gr_line (start {x1} {y2-r}) (end {x1} {y1+r}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{uid()}"))',
        f'\t(gr_arc (start {x1+r} {y1}) (mid {x1+0.73} {y1+0.73}) (end {x1} {y1+r}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{uid()}"))',
        f'\t(gr_arc (start {x2} {y1+r}) (mid {x2-0.73} {y1+0.73}) (end {x2-r} {y1}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{uid()}"))',
        f'\t(gr_arc (start {x2-r} {y2}) (mid {x2-0.73} {y2-0.73}) (end {x2} {y2-r}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{uid()}"))',
        f'\t(gr_arc (start {x1} {y2-r}) (mid {x1+0.73} {y2-0.73}) (end {x1+r} {y2}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{uid()}"))',
    ]

    # Professional Silkscreen markings (Zero pad overlap, clean clearance)
    silks = [
        # Front Silkscreen
        f'\t(gr_text "DASHCAM CARRIER" (at {X0+31.5} {Y0+16.0} 0) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 0.85 0.85) (thickness 0.15) (bold yes))))',
        f'\t(gr_text "REV 1.4" (at {X0+31.5} {Y0+18.0} 0) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 0.8 0.8) (thickness 0.12))))',
        f'\t(gr_text "SC3336 CAMERA [15P FPC]" (at {X0+31.5} {Y0+1.8} 0) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 0.8 0.8) (thickness 0.15))))',
        f'\t(gr_text "LUCKFOX PICO MINI B" (at {X0+31.5} {Y0+33.5} 0) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 0.85 0.85) (thickness 0.15))))',
        f'\t(gr_text "12V IN" (at {X0+12.0} {Y0+2.5} 0) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 0.8 0.8) (thickness 0.15))))',
        f'\t(gr_text "LIPO 3.7V" (at {X0+12.0} {Y0+39.5} 0) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 0.8 0.8) (thickness 0.15))))',
        f'\t(gr_text "USB WI-FI" (at {X0+57.0} {Y0+16.5} 0) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 0.8 0.8) (thickness 0.15))))',
        # SBC Outline box on silkscreen
        f'\t(gr_rect (start {X0+23.0} {Y0+9.0}) (end {X0+40.24} {Y0+35.0}) (stroke (width 0.15) (type dash)) (layer "F.SilkS") (uuid "{uid()}"))',
        # Back Silkscreen: Full Engineering Title & Credentials placed in open bottom-right zone
        f'\t(gr_text "DASHCAM CARRIER BOARD V1.4" (at {X0+48.0} {Y0+36.0} 0) (layer "B.SilkS") (uuid "{uid()}") (effects (font (size 0.85 0.85) (thickness 0.15) (bold yes)) (justify mirror)))',
        f'\t(gr_text "SOUVIK H | IN-ENG-2022-22824" (at {X0+48.0} {Y0+38.5} 0) (layer "B.SilkS") (uuid "{uid()}") (effects (font (size 0.8 0.8) (thickness 0.12)) (justify mirror)))'
    ]

    footprints = []

    # 4 M2.5 Mounting Holes
    def add_mounting_hole(x, y):
        return f"""\t(footprint "MountingHole:MountingHole_2.7mm_M2.5_Pad" (layer "F.Cu") (uuid "{uid()}") (at {x} {y})
\t\t(pad "1" thru_hole circle (at 0 0) (size 4.5 4.5) (drill 2.7) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t)"""

    footprints.append(add_mounting_hole(X0+3.5, Y0+3.5))
    footprints.append(add_mounting_hole(X0+BW-3.5, Y0+3.5))
    footprints.append(add_mounting_hole(X0+3.5, Y0+BH-3.5))
    footprints.append(add_mounting_hole(X0+BW-3.5, Y0+BH-3.5))

    # J1: 12V In Terminal Block at (X0+7.5, Y0+8.5)
    j1_x, j1_y = X0+7.5, Y0+8.5
    footprints.append(f"""\t(footprint "TerminalBlock:TerminalBlock_bornier-2_P5.08mm" (layer "F.Cu") (uuid "{uid()}") (at {j1_x} {j1_y})
\t\t(property "Reference" "J1" (at 0 -3.5 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "12V_IN" (at 0 3.5 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" thru_hole rect (at -2.54 0) (size 2.5 2.5) (drill 1.3) (layers "*.Cu" "*.Mask") (net 2 "+12V"))
\t\t(pad "2" thru_hole circle (at 2.54 0) (size 2.5 2.5) (drill 1.3) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t)""")

    # D1: SMBJ5.0A TVS at (X0+15.0, Y0+8.5)
    d1_x, d1_y = X0+15.0, Y0+8.5
    footprints.append(f"""\t(footprint "Diode_SMD:D_SMB" (layer "F.Cu") (uuid "{uid()}") (at {d1_x} {d1_y})
\t\t(property "Reference" "D1" (at 0 -2.5 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "SMBJ5.0A" (at 0 2.5 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" smd rect (at -2.15 0) (size 2.2 2.1) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "+12V"))
\t\t(pad "2" smd rect (at 2.15 0) (size 2.2 2.1) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
\t)""")

    # C1: 470uF Bulk Cap at (X0+7.5, Y0+16.5)
    c1_x, c1_y = X0+7.5, Y0+16.5
    footprints.append(f"""\t(footprint "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm" (layer "F.Cu") (uuid "{uid()}") (at {c1_x} {c1_y})
\t\t(property "Reference" "C1" (at 0 -4.5 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "470uF" (at 0 4.5 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" thru_hole rect (at -1.75 0) (size 1.8 1.8) (drill 0.9) (layers "*.Cu" "*.Mask") (net 2 "+12V"))
\t\t(pad "2" thru_hole circle (at 1.75 0) (size 1.8 1.8) (drill 0.9) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t)""")

    # U1: LM2596 Buck Module 4-Pin Header at (X0+7.5, Y0+26.0)
    u1_x, u1_y = X0+7.5, Y0+26.0
    footprints.append(f"""\t(footprint "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" (layer "F.Cu") (uuid "{uid()}") (at {u1_x} {u1_y})
\t\t(property "Reference" "U1" (at -2.5 0 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "LM2596_BUCK" (at 2.5 0 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" thru_hole rect (at 0 -3.81) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net 2 "+12V"))
\t\t(pad "2" thru_hole circle (at 0 -1.27) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t\t(pad "3" thru_hole circle (at 0 1.27) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net 3 "+5V_PRE"))
\t\t(pad "4" thru_hole circle (at 0 3.81) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t)""")

    # C2: 470uF Output Filter Cap at (X0+15.0, Y0+21.5)
    c2_x, c2_y = X0+15.0, Y0+21.5
    footprints.append(f"""\t(footprint "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm" (layer "F.Cu") (uuid "{uid()}") (at {c2_x} {c2_y})
\t\t(property "Reference" "C2" (at -4.8 0 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "470uF" (at 4.8 0 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" thru_hole rect (at -1.75 0) (size 1.8 1.8) (drill 0.9) (layers "*.Cu" "*.Mask") (net 3 "+5V_PRE"))
\t\t(pad "2" thru_hole circle (at 1.75 0) (size 1.8 1.8) (drill 0.9) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t)""")

    # C3: 100nF Ceramic Filter at (X0+15.0, Y0+27.5)
    c3_x, c3_y = X0+15.0, Y0+27.5
    footprints.append(f"""\t(footprint "Capacitor_SMD:C_0805_2012Metric" (layer "F.Cu") (uuid "{uid()}") (at {c3_x} {c3_y})
\t\t(property "Reference" "C3" (at 0 1.8 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "100nF" (at 0 -1.8 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" smd rect (at -0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 3 "+5V_PRE"))
\t\t(pad "2" smd rect (at 0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
\t)""")

    # J2: LiPo Battery Connector (JST-PH 2-Pin) at (X0+7.5, Y0+35.5)
    j2_x, j2_y = X0+7.5, Y0+35.5
    footprints.append(f"""\t(footprint "Connector_JST:JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal" (layer "F.Cu") (uuid "{uid()}") (at {j2_x} {j2_y})
\t\t(property "Reference" "J2" (at -3.5 0 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "LIPO_BAT" (at 0 3.5 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" thru_hole rect (at -1.0 0) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (net 4 "VBAT"))
\t\t(pad "2" thru_hole circle (at 1.0 0) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t)""")

    # C5: 100nF Battery Decoupling at (X0+15.0, Y0+35.5)
    c5_x, c5_y = X0+15.0, Y0+35.5
    footprints.append(f"""\t(footprint "Capacitor_SMD:C_0805_2012Metric" (layer "F.Cu") (uuid "{uid()}") (at {c5_x} {c5_y})
\t\t(property "Reference" "C5" (at 0 -1.8 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "100nF" (at 0 1.8 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" smd rect (at -0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 4 "VBAT"))
\t\t(pad "2" smd rect (at 0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
\t)""")

    # U2: IP5306 BMS Module 4-Pin Header at (X0+15.0, Y0+15.0)
    u2_x, u2_y = X0+15.0, Y0+15.0
    footprints.append(f"""\t(footprint "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" (layer "F.Cu") (uuid "{uid()}") (at {u2_x} {u2_y})
\t\t(property "Reference" "U2" (at 2.8 0 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "IP5306_BMS" (at -2.8 0 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" thru_hole rect (at 0 -3.81) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net 3 "+5V_PRE"))
\t\t(pad "2" thru_hole circle (at 0 -1.27) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net 4 "VBAT"))
\t\t(pad "3" thru_hole circle (at 0 1.27) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net 5 "+5V_SYS"))
\t\t(pad "4" thru_hole circle (at 0 3.81) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t)""")

    # R1: 100R Keep-Alive Resistor at (X0+20.0, Y0+38.0)
    r1_x, r1_y = X0+20.0, Y0+38.0
    footprints.append(f"""\t(footprint "Resistor_SMD:R_0805_2012Metric" (layer "F.Cu") (uuid "{uid()}") (at {r1_x} {r1_y})
\t\t(property "Reference" "R1" (at 0 -1.8 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "100R" (at 0 1.8 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" smd rect (at -0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 5 "+5V_SYS"))
\t\t(pad "2" smd rect (at 0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
\t)""")

    # C4: 100nF System Decoupling at (X0+25.0, Y0+38.0)
    c4_x, c4_y = X0+25.0, Y0+38.0
    footprints.append(f"""\t(footprint "Capacitor_SMD:C_0805_2012Metric" (layer "F.Cu") (uuid "{uid()}") (at {c4_x} {c4_y})
\t\t(property "Reference" "C4" (at 0 -1.8 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "100nF" (at 0 1.8 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" smd rect (at -0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 5 "+5V_SYS"))
\t\t(pad "2" smd rect (at 0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
\t)""")

    # J3: Luckfox Header Socket Left (8 pins) at X = X0 + 24.0, Y = Y0 + 22.0
    j3_x = X0 + 24.0
    j3_pads = [
        (1, 21, "UART2_TX"),
        (2, 22, "UART2_RX"),
        (3, 1,  "GND"),
        (4, 6,  "+3V3"),
        (5, 13, "I2C3_SCL"),
        (6, 14, "I2C3_SDA"),
        (7, 1,  "GND"),
        (8, 19, "STAT_LED")
    ]
    j3_str = []
    for idx, (p_num, net_id, net_name) in enumerate(j3_pads):
        p_y = -8.89 + idx * 2.54
        p_type = "rect" if p_num == 1 else "circle"
        j3_str.append(f'\t\t(pad "{p_num}" thru_hole {p_type} (at 0 {p_y}) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net {net_id} "{net_name}"))')

    nl = "\n"
    footprints.append(f"""\t(footprint "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical" (layer "F.Cu") (uuid "{uid()}") (at {j3_x} {Y0+22.0})
\t\t(property "Reference" "J3" (at 0 -11.2 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "LUCKFOX_J1" (at 2.8 0 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
{nl.join(j3_str)}
\t)""")

    # C7: 100nF on +3V3 at (X0+21.0, Y0+13.0)
    c7_x, c7_y = X0+21.0, Y0+13.0
    footprints.append(f"""\t(footprint "Capacitor_SMD:C_0805_2012Metric" (layer "F.Cu") (uuid "{uid()}") (at {c7_x} {c7_y})
\t\t(property "Reference" "C7" (at 0 -1.8 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "100nF" (at 0 1.8 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" smd rect (at -0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 6 "+3V3"))
\t\t(pad "2" smd rect (at 0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
\t)""")

    # J4: Luckfox Header Socket Right (8 pins) at X = X0 + 39.24 (15.24 mm spacing)
    j4_x = X0 + 39.24
    j4_pads = [
        (1, 5,  "+5V_SYS"),
        (2, 1,  "GND"),
        (3, 18, "USB_DM"),
        (4, 17, "USB_DP"),
        (5, 15, "CAM_RSTn"),
        (6, 16, "CAM_PDN"),
        (7, 20, "SW_SENSE"),
        (8, 1,  "GND")
    ]
    j4_str = []
    for idx, (p_num, net_id, net_name) in enumerate(j4_pads):
        p_y = -8.89 + idx * 2.54
        p_type = "rect" if p_num == 1 else "circle"
        j4_str.append(f'\t\t(pad "{p_num}" thru_hole {p_type} (at 0 {p_y}) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net {net_id} "{net_name}"))')

    footprints.append(f"""\t(footprint "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical" (layer "F.Cu") (uuid "{uid()}") (at {j4_x} {Y0+22.0})
\t\t(property "Reference" "J4" (at 0 -11.2 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "LUCKFOX_J2" (at -2.8 0 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
{nl.join(j4_str)}
\t)""")

    # C6: 100nF on +5V_SYS at (X0+42.5, Y0+13.0)
    c6_x, c6_y = X0+42.5, Y0+13.0
    footprints.append(f"""\t(footprint "Capacitor_SMD:C_0805_2012Metric" (layer "F.Cu") (uuid "{uid()}") (at {c6_x} {c6_y})
\t\t(property "Reference" "C6" (at 0 -1.8 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "100nF" (at 0 1.8 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" smd rect (at -0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 5 "+5V_SYS"))
\t\t(pad "2" smd rect (at 0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
\t)""")

    # J5: SmartSens SC3336 15-Pin FPC Connector at X = X0 + 31.5, Y = Y0 + 4.8
    j5_x, j5_y = X0 + 31.5, Y0 + 4.8
    cam_fpc_nets = [
        (1, 1,  "GND"),
        (2, 8,  "MIPI_D0_N"),
        (3, 7,  "MIPI_D0_P"),
        (4, 1,  "GND"),
        (5, 10, "MIPI_CLK_N"),
        (6, 9,  "MIPI_CLK_P"),
        (7, 1,  "GND"),
        (8, 12, "MIPI_D1_N"),
        (9, 11, "MIPI_D1_P"),
        (10, 1, "GND"),
        (11, 15,"CAM_RSTn"),
        (12, 16,"CAM_PDN"),
        (13, 13,"I2C3_SCL"),
        (14, 14,"I2C3_SDA"),
        (15, 6, "+3V3")
    ]
    j5_pads = []
    for p_num, net_id, net_name in cam_fpc_nets:
        p_x = -3.5 + (p_num - 1) * 0.5
        j5_pads.append(f'\t\t(pad "{p_num}" smd rect (at {p_x} -1.25) (size 0.3 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (net {net_id} "{net_name}"))')
    j5_pads.append(f'\t\t(pad "MP1" smd rect (at -4.5 0.5) (size 1.2 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))')
    j5_pads.append(f'\t\t(pad "MP2" smd rect (at 4.5 0.5) (size 1.2 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))')

    footprints.append(f"""\t(footprint "Connector_FFC-FPC:Hirose_FH12-15S-0.5SH_1x15-1MP_P0.50mm_Horizontal" (layer "F.Cu") (uuid "{uid()}") (at {j5_x} {j5_y})
\t\t(property "Reference" "J5" (at 0 2.8 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "SC3336_FPC" (at 0 -2.8 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
{nl.join(j5_pads)}
\t)""")

    # C8: 100nF on Camera +3V3 at (X0+40.0, Y0+4.8)
    c8_x, c8_y = X0+40.0, Y0+4.8
    footprints.append(f"""\t(footprint "Capacitor_SMD:C_0805_2012Metric" (layer "F.Cu") (uuid "{uid()}") (at {c8_x} {c8_y})
\t\t(property "Reference" "C8" (at 0 1.8 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "100nF" (at 0 -1.8 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" smd rect (at -0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 6 "+3V3"))
\t\t(pad "2" smd rect (at 0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
\t)""")

    # J7: USB-A Female Receptacle for Wi-Fi Dongle at (X0+57.0, Y0+28.0, rot 90)
    j7_x, j7_y = X0+57.0, Y0+28.0
    footprints.append(f"""\t(footprint "Connector_USB:USB_A_Molex_67643_Horizontal" (layer "F.Cu") (uuid "{uid()}") (at {j7_x} {j7_y} 90)
\t\t(property "Reference" "J7" (at 0 -4.5 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "USB_WIFI" (at 0 4.5 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" thru_hole rect (at -3.5 -1.0 90) (size 1.6 1.6) (drill 0.9) (layers "*.Cu" "*.Mask") (net 5 "+5V_SYS"))
\t\t(pad "2" thru_hole circle (at -1.0 -1.0 90) (size 1.6 1.6) (drill 0.9) (layers "*.Cu" "*.Mask") (net 18 "USB_DM"))
\t\t(pad "3" thru_hole circle (at 1.0 -1.0 90) (size 1.6 1.6) (drill 0.9) (layers "*.Cu" "*.Mask") (net 17 "USB_DP"))
\t\t(pad "4" thru_hole circle (at 3.5 -1.0 90) (size 1.6 1.6) (drill 0.9) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t\t(pad "SH" thru_hole circle (at -5.7 2.0 90) (size 3.0 3.0) (drill 2.3) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t\t(pad "SH" thru_hole circle (at 5.7 2.0 90) (size 3.0 3.0) (drill 2.3) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t)""")

    # C9: 100nF VBUS Decoupling Cap at (X0+48.0, Y0+28.0)
    c9_x, c9_y = X0+48.0, Y0+28.0
    footprints.append(f"""\t(footprint "Capacitor_SMD:C_0805_2012Metric" (layer "F.Cu") (uuid "{uid()}") (at {c9_x} {c9_y})
\t\t(property "Reference" "C9" (at 0 -1.8 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "100nF" (at 0 1.8 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" smd rect (at -0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 5 "+5V_SYS"))
\t\t(pad "2" smd rect (at 0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
\t)""")

    # SW1: Pushbutton Switch at (X0+49.0, Y0+7.5)
    sw1_x, sw1_y = X0+49.0, Y0+7.5
    footprints.append(f"""\t(footprint "Button_Switch_SMD:SW_Push_1P1T_NO_6x6mm_H9.5mm" (layer "F.Cu") (uuid "{uid()}") (at {sw1_x} {sw1_y})
\t\t(property "Reference" "SW1" (at 0 -4.2 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "PWR_BTN" (at 0 4.2 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" smd rect (at -3.25 0) (size 1.8 1.4) (layers "F.Cu" "F.Paste" "F.Mask") (net 20 "SW_SENSE"))
\t\t(pad "2" smd rect (at 3.25 0) (size 1.8 1.4) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
\t)""")

    # R2: 10k Pull-Up for SW1 at (X0+49.0, Y0+13.0)
    r2_x, r2_y = X0+49.0, Y0+13.0
    footprints.append(f"""\t(footprint "Resistor_SMD:R_0805_2012Metric" (layer "F.Cu") (uuid "{uid()}") (at {r2_x} {r2_y})
\t\t(property "Reference" "R2" (at 0 1.8 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "10k" (at 0 -1.8 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" smd rect (at -0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 6 "+3V3"))
\t\t(pad "2" smd rect (at 0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 20 "SW_SENSE"))
\t)""")

    # R3: 470R LED Resistor at (X0+56.0, Y0+7.5)
    r3_x, r3_y = X0+56.0, Y0+7.5
    footprints.append(f"""\t(footprint "Resistor_SMD:R_0805_2012Metric" (layer "F.Cu") (uuid "{uid()}") (at {r3_x} {r3_y})
\t\t(property "Reference" "R3" (at 0 -1.8 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "470R" (at 0 1.8 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" smd rect (at -0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 19 "STAT_LED"))
\t\t(pad "2" smd rect (at 0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 23 "Net-(D2-A)"))
\t)""")

    # D2: Status LED at (X0+59.5, Y0+7.5)
    d2_x, d2_y = X0+59.5, Y0+7.5
    footprints.append(f"""\t(footprint "LED_SMD:LED_0805_2012Metric" (layer "F.Cu") (uuid "{uid()}") (at {d2_x} {d2_y})
\t\t(property "Reference" "D2" (at 0 -1.8 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "STAT_LED" (at 0 1.8 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" smd rect (at -0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 23 "Net-(D2-A)"))
\t\t(pad "2" smd rect (at 0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
\t)""")

    # Ground Copper Zone on B.Cu (Used by Freerouting as Ground Plane)
    zone_pts = [
        f'(xy {x1} {y1})',
        f'(xy {x2} {y1})',
        f'(xy {x2} {y2})',
        f'(xy {x1} {y2})'
    ]
    zones = [
        f"""\t(zone (net "GND") (layer "B.Cu") (uuid "{uid()}")
\t\t(hatch edge 0.5)
\t\t(priority 0)
\t\t(connect_pads (clearance 0.25))
\t\t(min_thickness 0.2)
\t\t(filled_areas_thickness no)
\t\t(fill yes (thermal_gap 0.25) (thermal_bridge_width 0.35))
\t\t(polygon
\t\t\t(pts
\t\t\t\t{" ".join(zone_pts)}
\t\t\t)
\t\t)
\t)"""
    ]

    pcb_template = f"""(kicad_pcb
\t(version 20240108)
\t(generator "pcbnew")
\t(generator_version "10.0")
\t(general
\t\t(thickness 1.6)
\t\t(legacy_teardrops no)
\t)
\t(paper "A4")
\t(title_block
\t\t(title "DASHCAM CARRIER BOARD")
\t\t(date "2026-10-14")
\t\t(rev "1.4")
\t\t(company "DASHCAM PROTOTYPE PROJECT")
\t\t(comment 1 "Engineer: Souvik H | Regn: IN-ENG-2022-22824")
\t\t(comment 2 "Discipline: EMBEDDED SYSTEMS & HARDWARE")
\t\t(comment 3 "Luckfox Pico Mini B (RV1103) + SC3336 + IP5306 + RTL8188EUS")
\t\t(comment 4 "Status: RELEASED")
\t)
\t(layers
\t\t(0 "F.Cu" signal)
\t\t(31 "B.Cu" signal)
\t\t(32 "B.Adhes" user "B.Adhesive")
\t\t(33 "F.Adhes" user "F.Adhesive")
\t\t(34 "B.Paste" user)
\t\t(35 "F.Paste" user)
\t\t(36 "B.SilkS" user "B.Silkscreen")
\t\t(37 "F.SilkS" user "F.Silkscreen")
\t\t(38 "B.Mask" user)
\t\t(39 "F.Mask" user)
\t\t(40 "Dwgs.User" user "User.Drawings")
\t\t(41 "Cmts.User" user "User.Comments")
\t\t(42 "Eco1.User" user "User.Eco1")
\t\t(43 "Eco2.User" user "User.Eco2")
\t\t(44 "Edge.Cuts" user)
\t\t(45 "Margin" user)
\t\t(46 "B.CrtYd" user "B.Courtyard")
\t\t(47 "F.CrtYd" user "F.Courtyard")
\t\t(48 "B.Fab" user)
\t\t(49 "F.Fab" user)
\t)
\t(setup
\t\t(pad_to_mask_clearance 0.05)
\t\t(allow_soldermask_bridges_in_footprints no)
\t\t(pcbplotparams
\t\t\t(layerselection 0x00010fc_ffffffff)
\t\t\t(plot_on_all_layers_selection 0x0000000_00000000)
\t\t\t(disableapertmacros no)
\t\t\t(usegerberextensions yes)
\t\t\t(usegerberattributes yes)
\t\t\t(usegerberadvancedattributes yes)
\t\t\t(creategerberjobfile yes)
\t\t\t(dashed_line_dash_ratio 12.000000)
\t\t\t(dashed_line_gap_ratio 3.000000)
\t\t\t(svgprecision 4)
\t\t\t(plotframeref no)
\t\t\t(viasonmask no)
\t\t\t(mode 1)
\t\t\t(useauxorigin no)
\t\t\t(hpglpennumber 1)
\t\t\t(hpglpenspeed 20)
\t\t\t(hpglpendiameter 15.000000)
\t\t\t(pdf_front_fp_property_popups yes)
\t\t\t(pdf_back_fp_property_popups yes)
\t\t\t(dxfpolygonmode yes)
\t\t\t(dxfimperialunits no)
\t\t\t(dxfcontourmode no)
\t\t\t(psnegative no)
\t\t\t(psa4output no)
\t\t\t(plotreference yes)
\t\t\t(plotvalue yes)
\t\t\t(plotfptext yes)
\t\t\t(plotinvisibletext no)
\t\t\t(sketchpadsonfab no)
\t\t\t(subtractmaskfromsilk no)
\t\t\t(outputformat 1)
\t\t\t(mirror no)
\t\t\t(drillshape 1)
\t\t\t(scaleselection 1)
\t\t\t(outputdirectory "gerbers/")
\t\t)
\t)
{net_lines}
{nl.join(footprints)}
{nl.join(edge_cuts)}
{nl.join(silks)}
{nl.join(zones)}
)"""
    return pcb_template, net_map

def parse_ses_and_merge(pcb_content, ses_path, net_map):
    with open(ses_path, "r", encoding="utf-8") as f:
        ses_text = f.read()

    start_pos = ses_text.find("(network_out")
    if start_pos == -1:
        print("[WARN] Could not find network_out in SES file")
        return pcb_content

    net_parts = ses_text[start_pos:].split("(net ")
    track_lines = []
    via_lines = []

    for part in net_parts[1:]:
        part = part.strip()
        if part.startswith('"'):
            end_q = part.find('"', 1)
            net_name_clean = part[1:end_q]
            body = part[end_q+1:]
        else:
            tokens = part.split(None, 1)
            net_name_clean = tokens[0]
            body = tokens[1] if len(tokens) > 1 else ""

        net_id = net_map.get(net_name_clean, 0)
        if net_id == 0:
            continue

        # Parse wires
        wires = re.findall(r'\(path\s+([^\s]+)\s+(\d+)\s+([^\)]+)\)', body)
        for layer, width_str, pts_str in wires:
            width_mm = round(float(width_str) / 10000.0, 3)
            nums = [float(n) for n in pts_str.split()]
            pts = [(nums[i] / 10000.0, -nums[i+1] / 10000.0) for i in range(0, len(nums), 2)]
            for i in range(len(pts) - 1):
                sx, sy = round(pts[i][0], 3), round(pts[i][1], 3)
                ex, ey = round(pts[i+1][0], 3), round(pts[i+1][1], 3)
                if sx != ex or sy != ey:
                    track_lines.append(f'\t(segment (start {sx} {sy}) (end {ex} {ey}) (width {width_mm}) (layer "{layer}") (net {net_id}) (uuid "{uid()}"))')

        # Parse vias
        vias = re.findall(r'\(via\s+\"[^\"]+\"\s+([-\d]+)\s+([-\d]+)', body)
        for vx_str, vy_str in vias:
            vx = round(float(vx_str) / 10000.0, 3)
            vy = round(-float(vy_str) / 10000.0, 3)
            via_lines.append(f'\t(via (at {vx} {vy}) (size 0.6) (drill 0.3) (layers "F.Cu" "B.Cu") (net {net_id}) (uuid "{uid()}"))')

    print(f"[OK] Parsed from SES: {len(track_lines)} track segments, {len(via_lines)} vias.")

    # Direct stitch connection for C6 GND to J4 GND on F.Cu
    # C6 pad 2 is at (X0+43.45, Y0+13.0) = (143.45, 93.0)
    # J4 pad 2 is at (X0+39.24, Y0+15.65) = (139.24, 95.65)
    c6_gnd_x = X0 + 43.45
    c6_gnd_y = Y0 + 13.0
    j4_gnd_x = X0 + 39.24
    j4_gnd_y = Y0 + 15.65
    mid_x = c6_gnd_x
    mid_y = j4_gnd_y
    track_lines.append(f'\t(segment (start {c6_gnd_x} {c6_gnd_y}) (end {mid_x} {mid_y}) (width 0.25) (layer "F.Cu") (net 1) (uuid "{uid()}"))')
    track_lines.append(f'\t(segment (start {mid_x} {mid_y}) (end {j4_gnd_x} {j4_gnd_y}) (width 0.25) (layer "F.Cu") (net 1) (uuid "{uid()}"))')

    # Ground stitch via at (141.5, 95.65) to permanently tie B.Cu island around J4-2 to F.Cu GND plane
    via_lines.append(f'\t(via (at {141.5} {95.65}) (size 0.6) (drill 0.3) (layers "F.Cu" "B.Cu") (net 1) (uuid "{uid()}"))')

    # Add F.Cu GND Zone to the merged board
    x1, y1 = X0, Y0
    x2, y2 = X0 + BW, Y0 + BH
    zone_pts = [f'(xy {x1} {y1})', f'(xy {x2} {y1})', f'(xy {x2} {y2})', f'(xy {x1} {y2})']
    f_cu_zone = f"""\t(zone (net "GND") (layer "F.Cu") (uuid "{uid()}")
\t\t(hatch edge 0.5)
\t\t(priority 0)
\t\t(connect_pads (clearance 0.25))
\t\t(min_thickness 0.2)
\t\t(filled_areas_thickness no)
\t\t(fill yes (thermal_gap 0.25) (thermal_bridge_width 0.35))
\t\t(polygon
\t\t\t(pts
\t\t\t\t{" ".join(zone_pts)}
\t\t\t)
\t\t)
\t)"""

    # Insert tracks, vias, and F.Cu zone before the closing parenthesis
    idx = pcb_content.rfind(')')
    if idx != -1:
        routed_content = pcb_content[:idx] + "\n" + "\n".join(track_lines) + "\n" + "\n".join(via_lines) + "\n" + f_cu_zone + "\n)"
        return routed_content
    return pcb_content

def main():
    pcb_path = os.path.join(CARRIER_DIR, "carrier_board.kicad_pcb")
    dsn_path = os.path.join(CARRIER_DIR, "carrier_board.dsn")
    ses_path = os.path.join(CARRIER_DIR, "carrier_board.ses")

    # Step 1: Generate unrouted PCB with all components & ground plane
    print("[1/5] Generating pristine unrouted PCB layout...")
    pcb_template, net_map = generate_pcb()
    with open(pcb_path, "w", encoding="utf-8") as f:
        f.write(pcb_template)

    # Step 2: Export Specctra DSN using KiCad Python API
    print("[2/5] Exporting Specctra DSN file via pcbnew...")
    import pcbnew
    board = pcbnew.LoadBoard(pcb_path)
    if not pcbnew.ExportSpecctraDSN(board, dsn_path):
        raise RuntimeError("Failed to export Specctra DSN")
    print(f"[OK] Exported DSN to {dsn_path}")

    # Step 3: Run Freerouting autorouter
    print("[3/5] Launching Freerouting autorouter (Java 25 engine)...")
    cmd = [
        JAVA_EXE,
        "-jar", FREEROUTING_JAR,
        "-de", dsn_path,
        "-do", ses_path,
        "--gui.enabled=false",
        "-mp", "60"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    print("Freerouting completed with return code:", res.returncode)
    for line in res.stdout.splitlines()[-10:]:
        print("  [FR]", line)

    # Step 4: Parse SES and merge autorouted tracks into PCB
    print("[4/5] Merging autorouted tracks and vias into carrier_board.kicad_pcb...")
    routed_pcb = parse_ses_and_merge(pcb_template, ses_path, net_map)
    with open(pcb_path, "w", encoding="utf-8") as f:
        f.write(routed_pcb)

    # Step 5: Fill zones and save
    print("[5/5] Re-filling copper zones...")
    board = pcbnew.LoadBoard(pcb_path)
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    board.Save(pcb_path)
    print(f"[DONE] Complete Autorouted Carrier Board saved to {pcb_path}")

if __name__ == "__main__":
    main()
