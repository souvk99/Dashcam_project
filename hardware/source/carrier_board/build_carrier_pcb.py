import os
import uuid
import subprocess

BASE_DIR = r"C:\Users\souvk\Downloads\Dashcam_project"
CARRIER_DIR = os.path.join(BASE_DIR, "hardware", "source", "carrier_board")
KICAD_CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"

def uid():
    return str(uuid.uuid4())

# Board offset on sheet: Origin (X0, Y0) = (100.0, 80.0)
X0 = 100.0
Y0 = 80.0
BW = 60.0 # Board Width 60 mm
BH = 38.0 # Board Height 38 mm

def build_pcb():
    # Net definitions
    nets = [
        (0, ""),
        (1, "GND"),
        (2, "+12V_IN"),
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
        (22, "UART2_RX")
    ]

    net_lines = "\n".join([f'\t(net {nid} "{nname}")' for nid, nname in nets])

    # Board Outline (Edge.Cuts) with rounded corners (r=2.0 mm)
    r = 2.0
    x1, y1 = X0, Y0
    x2, y2 = X0 + BW, Y0 + BH
    edge_cuts = [
        f'\t(gr_line (start {x1+r} {y1}) (end {x2-r} {y1}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{uid()}"))',
        f'\t(gr_line (start {x2} {y1+r}) (end {x2} {y2-r}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{uid()}"))',
        f'\t(gr_line (start {x2-r} {y2}) (end {x1+r} {y2}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{uid()}"))',
        f'\t(gr_line (start {x1} {y2-r}) (end {x1} {y1+r}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{uid()}"))',
        # Corner arcs
        f'\t(gr_arc (start {x1+r} {y1}) (mid {x1+0.58} {y1+0.58}) (end {x1} {y1+r}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{uid()}"))',
        f'\t(gr_arc (start {x2} {y1+r}) (mid {x2-0.58} {y1+0.58}) (end {x2-r} {y1}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{uid()}"))',
        f'\t(gr_arc (start {x2-r} {y2}) (mid {x2-0.58} {y2-0.58}) (end {x2} {y2-r}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{uid()}"))',
        f'\t(gr_arc (start {x1} {y2-r}) (mid {x1+0.58} {y2-0.58}) (end {x1+r} {y2}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{uid()}"))',
    ]

    # Silkscreen graphics & text on F.SilkS
    silks = [
        f'\t(gr_text "DASHCAM CARRIER BOARD V1.4" (at {X0+BW/2} {Y0+16.0} 0) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 1.2 1.2) (thickness 0.2) (bold yes))))',
        f'\t(gr_text "SOUVIK H | IN-ENG-2022-22824" (at {X0+BW/2} {Y0+18.5} 0) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 0.9 0.9) (thickness 0.15))))',
        f'\t(gr_text "SC3336 CAMERA [15P FPC]" (at {X0+30.0} {Y0+2.5} 0) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 0.8 0.8) (thickness 0.15))))',
        f'\t(gr_text "LUCKFOX PICO MINI B" (at {X0+30.0} {Y0+33.0} 0) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 1.0 1.0) (thickness 0.18))))',
        f'\t(gr_text "USB WI-FI" (at {X0+53.0} {Y0+18.0} 0) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 0.8 0.8) (thickness 0.15))))',
        f'\t(gr_text "12V IN" (at {X0+8.0} {Y0+2.5} 0) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 0.8 0.8) (thickness 0.15))))',
        f'\t(gr_text "LIPO 3.7V" (at {X0+8.0} {Y0+35.5} 0) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 0.8 0.8) (thickness 0.15))))',
        f'\t(gr_text "IP5306 BMS" (at {X0+12.0} {Y0+25.0} 0) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 0.8 0.8) (thickness 0.15))))',
        # SBC Outline box on silkscreen
        f'\t(gr_rect (start {X0+19.5} {Y0+7.0}) (end {X0+40.5} {Y0+32.0}) (stroke (width 0.15) (type dash)) (layer "F.SilkS") (uuid "{uid()}"))'
    ]

    footprints = []
    tracks = []
    vias = []

    # Helper function for M2.5 mounting holes
    def add_mounting_hole(x, y):
        return f"""\t(footprint "MountingHole:MountingHole_2.7mm_M2.5_Pad" (layer "F.Cu") (uuid "{uid()}") (at {x} {y})
\t\t(pad "1" thru_hole circle (at 0 0) (size 4.5 4.5) (drill 2.7) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t)"""

    footprints.append(add_mounting_hole(X0+3.5, Y0+3.5))
    footprints.append(add_mounting_hole(X0+BW-3.5, Y0+3.5))
    footprints.append(add_mounting_hole(X0+3.5, Y0+BH-3.5))
    footprints.append(add_mounting_hole(X0+BW-3.5, Y0+BH-3.5))

    # Helper function for tracks
    def add_track(x1, y1, x2, y2, width, net_id, layer="F.Cu"):
        x1, y1, x2, y2 = round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)
        if x1 == x2 and y1 == y2: return
        tracks.append(f'\t(segment (start {x1} {y1}) (end {x2} {y2}) (width {width}) (layer "{layer}") (net {net_id}) (uuid "{uid()}"))')

    def add_via(x, y, net_id):
        x, y = round(x, 2), round(y, 2)
        vias.append(f'\t(via (at {x} {y}) (size 0.6) (drill 0.3) (layers "F.Cu" "B.Cu") (net {net_id}) (uuid "{uid()}"))')

    # J1 (12V IN)
    j1_x, j1_y = X0+8.0, Y0+8.0
    footprints.append(f"""\t(footprint "TerminalBlock:TerminalBlock_bornier-2_P5.08mm" (layer "F.Cu") (uuid "{uid()}") (at {j1_x} {j1_y})
\t\t(property "Reference" "J1" (at 0 -3.5 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "12V_IN" (at 0 3.5 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" thru_hole rect (at -2.54 0) (size 2.5 2.5) (drill 1.3) (layers "*.Cu" "*.Mask") (net 2 "+12V_IN"))
\t\t(pad "2" thru_hole circle (at 2.54 0) (size 2.5 2.5) (drill 1.3) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t)""")

    # D1 (TVS Diode) SMB
    d1_x, d1_y = X0+15.0, Y0+8.0
    footprints.append(f"""\t(footprint "Diode_SMD:D_SMB" (layer "F.Cu") (uuid "{uid()}") (at {d1_x} {d1_y})
\t\t(property "Reference" "D1" (at 0 -2.5 0) (layer "F.SilkS") (effects (font (size 0.7 0.7) (thickness 0.1))))
\t\t(property "Value" "SMBJ5.0A" (at 0 2.5 0) (layer "F.Fab") (effects (font (size 0.7 0.7) (thickness 0.1))))
\t\t(pad "1" smd rect (at -2.15 0) (size 2.2 2.1) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "+12V_IN"))
\t\t(pad "2" smd rect (at 2.15 0) (size 2.2 2.1) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
\t)""")

    # C1 (470uF / 25V Electrolytic)
    c1_x, c1_y = X0+8.0, Y0+15.5
    footprints.append(f"""\t(footprint "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm" (layer "F.Cu") (uuid "{uid()}") (at {c1_x} {c1_y})
\t\t(property "Reference" "C1" (at 0 -4.5 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "470uF" (at 0 4.5 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" thru_hole rect (at -1.75 0) (size 1.8 1.8) (drill 0.9) (layers "*.Cu" "*.Mask") (net 2 "+12V_IN"))
\t\t(pad "2" thru_hole circle (at 1.75 0) (size 1.8 1.8) (drill 0.9) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t)""")

    # U1 (LM2596 Module 4-Pin Header)
    u1_x, u1_y = X0+8.0, Y0+24.0
    footprints.append(f"""\t(footprint "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" (layer "F.Cu") (uuid "{uid()}") (at {u1_x} {u1_y})
\t\t(property "Reference" "U1" (at -2.5 0 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "LM2596_BUCK" (at 2.5 0 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" thru_hole rect (at 0 -3.81) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net 2 "+12V_IN"))
\t\t(pad "2" thru_hole circle (at 0 -1.27) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t\t(pad "3" thru_hole circle (at 0 1.27) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net 3 "+5V_PRE"))
\t\t(pad "4" thru_hole circle (at 0 3.81) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t)""")

    # J2 (LiPo Battery Connector JST-PH 2-Pin)
    j2_x, j2_y = X0+8.0, Y0+32.0
    footprints.append(f"""\t(footprint "Connector_JST:JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal" (layer "F.Cu") (uuid "{uid()}") (at {j2_x} {j2_y})
\t\t(property "Reference" "J2" (at 0 -3.5 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "LIPO_BAT" (at 0 3.5 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" thru_hole rect (at -1.0 0) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (net 4 "VBAT"))
\t\t(pad "2" thru_hole circle (at 1.0 0) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t)""")

    # U2 (IP5306 BMS Module 4-Pin Header)
    u2_x, u2_y = X0+15.0, Y0+24.0
    footprints.append(f"""\t(footprint "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" (layer "F.Cu") (uuid "{uid()}") (at {u2_x} {u2_y})
\t\t(property "Reference" "U2" (at 2.5 0 90) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(property "Value" "IP5306_BMS" (at -2.5 0 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
\t\t(pad "1" thru_hole rect (at 0 -3.81) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net 3 "+5V_PRE"))
\t\t(pad "2" thru_hole circle (at 0 -1.27) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net 4 "VBAT"))
\t\t(pad "3" thru_hole circle (at 0 1.27) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net 5 "+5V_SYS"))
\t\t(pad "4" thru_hole circle (at 0 3.81) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (net 1 "GND"))
\t)""")

    # R1 (Keep-Alive 100 Ohm Resistor)
    r1_x, r1_y = X0+15.0, Y0+32.0
    footprints.append(f"""\t(footprint "Resistor_SMD:R_0805_2012Metric" (layer "F.Cu") (uuid "{uid()}") (at {r1_x} {r1_y})
\t\t(property "Reference" "R1" (at 0 -1.5 0) (layer "F.SilkS") (effects (font (size 0.7 0.7) (thickness 0.1))))
\t\t(property "Value" "100R" (at 0 1.5 0) (layer "F.Fab") (effects (font (size 0.7 0.7) (thickness 0.1))))
\t\t(pad "1" smd rect (at -0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 5 "+5V_SYS"))
\t\t(pad "2" smd rect (at 0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
\t)""")

    # J3 (Luckfox Header Socket Left, 8 pins) at X = X0 + 22.38
    j3_x = X0 + 22.38
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

    footprints.append(f"""\t(footprint "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical" (layer "F.Cu") (uuid "{uid()}") (at {j3_x} {Y0+20.0})
\t\t(property "Reference" "J3" (at -2.5 0 90) (layer "F.SilkS") (effects (font (size 0.9 0.9) (thickness 0.12))))
\t\t(property "Value" "LUCKFOX_J1" (at 2.5 0 90) (layer "F.Fab") (effects (font (size 0.9 0.9) (thickness 0.12))))
{"\n".join(j3_str)}
\t)""")

    # J4 (Luckfox Header Socket Right, 8 pins) at X = X0 + 37.62 (15.24 mm row spacing)
    j4_x = X0 + 37.62
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

    footprints.append(f"""\t(footprint "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical" (layer "F.Cu") (uuid "{uid()}") (at {j4_x} {Y0+20.0})
\t\t(property "Reference" "J4" (at 2.5 0 90) (layer "F.SilkS") (effects (font (size 0.9 0.9) (thickness 0.12))))
\t\t(property "Value" "LUCKFOX_J2" (at -2.5 0 90) (layer "F.Fab") (effects (font (size 0.9 0.9) (thickness 0.12))))
{"\n".join(j4_str)}
\t)""")

    # J5 (SmartSens SC3336 15-Pin 0.5mm FPC Connector) centered at X = X0 + 30.0, Y = Y0 + 4.5
    j5_x, j5_y = X0 + 30.0, Y0 + 4.5
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
    # Mounting retention tabs
    j5_pads.append(f'\t\t(pad "MP1" smd rect (at -4.5 0.5) (size 1.2 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))')
    j5_pads.append(f'\t\t(pad "MP2" smd rect (at 4.5 0.5) (size 1.2 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))')

    footprints.append(f"""\t(footprint "Connector_FFC-FPC:Hirose_FH12-15S-0.5SH_1x15-1MP_P0.50mm_Horizontal" (layer "F.Cu") (uuid "{uid()}") (at {j5_x} {j5_y})
\t\t(property "Reference" "J5" (at 0 2.2 0) (layer "F.SilkS") (effects (font (size 0.7 0.7) (thickness 0.1))))
\t\t(property "Value" "SC3336_FPC" (at 0 3.5 0) (layer "F.Fab") (effects (font (size 0.7 0.7) (thickness 0.1))))
{"\n".join(j5_pads)}
\t)""")

    # J7 (USB-A Female Receptacle for Wi-Fi Dongle) at East edge (X = X0 + 53.0, Y = Y0 + 26.0)
    j7_x, j7_y = X0 + 53.0, Y0 + 26.0
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

    # SW1 (Pushbutton Switch) at X = X0 + 46.0, Y = Y0 + 6.0
    sw1_x, sw1_y = X0 + 46.0, Y0 + 6.0
    footprints.append(f"""\t(footprint "Button_Switch_SMD:SW_Push_1P1T_NO_6x6mm_H9.5mm" (layer "F.Cu") (uuid "{uid()}") (at {sw1_x} {sw1_y})
\t\t(property "Reference" "SW1" (at 0 -4.0 0) (layer "F.SilkS") (effects (font (size 0.7 0.7) (thickness 0.1))))
\t\t(property "Value" "PWR_BTN" (at 0 4.0 0) (layer "F.Fab") (effects (font (size 0.7 0.7) (thickness 0.1))))
\t\t(pad "1" smd rect (at -3.25 0) (size 1.8 1.4) (layers "F.Cu" "F.Paste" "F.Mask") (net 20 "SW_SENSE"))
\t\t(pad "2" smd rect (at 3.25 0) (size 1.8 1.4) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
\t)""")

    # D2 (Status LED 0805) at X = X0 + 53.0, Y = Y0 + 6.0
    d2_x, d2_y = X0 + 53.0, Y0 + 6.0
    footprints.append(f"""\t(footprint "LED_SMD:LED_0805_2012Metric" (layer "F.Cu") (uuid "{uid()}") (at {d2_x} {d2_y})
\t\t(property "Reference" "D2" (at 0 -1.5 0) (layer "F.SilkS") (effects (font (size 0.7 0.7) (thickness 0.1))))
\t\t(property "Value" "STAT_LED" (at 0 1.5 0) (layer "F.Fab") (effects (font (size 0.7 0.7) (thickness 0.1))))
\t\t(pad "1" smd rect (at -0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 19 "STAT_LED"))
\t\t(pad "2" smd rect (at 0.95 0) (size 1.0 1.3) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))
\t)""")

    # -------------------------------------------------------------
    # ORTHOGONAL & SEPARATED TRACK ROUTING
    # -------------------------------------------------------------
    # 1. 12V IN: J1 Pin 1 (-2.54, 0) -> D1 Pin 1 (-2.15, 0) -> C1 Pin 1 (-1.75, 0) -> U1 Pin 1 (0, -3.81)
    add_track(j1_x-2.54, j1_y, d1_x-2.15, d1_y, 0.8, 2)
    add_track(j1_x-2.54, j1_y, c1_x-1.75, c1_y, 0.8, 2)
    add_track(c1_x-1.75, c1_y, u1_x, u1_y-3.81, 0.8, 2)

    # 2. +5V_PRE: U1 Pin 3 (0, +1.27) -> U2 Pin 1 (0, -3.81)
    add_track(u1_x, u1_y+1.27, u1_x+3.5, u1_y+1.27, 0.8, 3)
    add_track(u1_x+3.5, u1_y+1.27, u2_x, u2_y-3.81, 0.8, 3)

    # 3. VBAT: J2 Pin 1 (-1.0, 0) -> U2 Pin 2 (0, -1.27)
    add_track(j2_x-1.0, j2_y, u2_x-3.0, j2_y, 0.8, 4)
    add_track(u2_x-3.0, j2_y, u2_x, u2_y-1.27, 0.8, 4)

    # 4. +5V_SYS Main Power: U2 Pin 3 (0, 1.27) -> R1 Pin 1 (-0.95, 0)
    add_track(u2_x, u2_y+1.27, r1_x-0.95, r1_y, 0.8, 5)
    # Route +5V_SYS around south edge to J4 Pin 1 and J7 Pin 1
    add_track(r1_x-0.95, r1_y, r1_x-0.95, Y0+35.0, 1.0, 5)
    add_track(r1_x-0.95, Y0+35.0, X0+42.0, Y0+35.0, 1.0, 5)
    add_track(X0+42.0, Y0+35.0, X0+42.0, Y0+10.0, 1.0, 5)
    add_track(X0+42.0, Y0+10.0, j4_x, Y0+11.11, 1.0, 5) # To J4 Pin 1 (+5V_SYS)
    add_track(X0+42.0, Y0+22.5, j7_x+1.0, j7_y-3.5, 1.0, 5) # To J7 Pin 1 (USB VBUS)

    # 5. +3V3 Rail: J3 Pin 4 (0, -1.27) -> J5 Pin 15 (+3.5, -1.25)
    # Route around north-west of J3
    add_track(j3_x, Y0+20.0-1.27, j3_x-3.0, Y0+20.0-1.27, 0.6, 6)
    add_track(j3_x-3.0, Y0+20.0-1.27, j3_x-3.0, Y0+6.5, 0.6, 6)
    add_track(j3_x-3.0, Y0+6.5, j5_x+3.5, Y0+6.5, 0.6, 6)
    add_track(j5_x+3.5, Y0+6.5, j5_x+3.5, j5_y-1.25, 0.6, 6)

    # 6. USB Differential Pair (J4 Pins 3, 4 -> J7 Pins 2, 3)
    # J4 Pin 3 (USB_DM): Y = Y0+20.0-8.89+2*2.54 = Y0+16.19
    # J4 Pin 4 (USB_DP): Y = Y0+20.0-8.89+3*2.54 = Y0+18.73
    # J7 Pin 2 (USB_DM): (154.0, 105.0) | J7 Pin 3 (USB_DP): (154.0, 107.0)
    add_track(j4_x, Y0+16.19, j4_x+7.0, Y0+16.19, 0.3, 18)
    add_track(j4_x+7.0, Y0+16.19, j7_x+1.0, j7_y-1.0, 0.3, 18)

    add_track(j4_x, Y0+18.73, j4_x+6.0, Y0+18.73, 0.3, 17)
    add_track(j4_x+6.0, Y0+18.73, j7_x+1.0, j7_y+1.0, 0.3, 17)

    # 7. MIPI CSI-2 Differential Pairs (J5 FPC -> South direction)
    add_track(j5_x-3.0, j5_y-1.25, j5_x-3.0, j5_y+2.0, 0.25, 8)  # D0_N
    add_track(j5_x-2.5, j5_y-1.25, j5_x-2.5, j5_y+2.0, 0.25, 7)  # D0_P
    add_track(j5_x-1.5, j5_y-1.25, j5_x-1.5, j5_y+2.0, 0.25, 10) # CLK_N
    add_track(j5_x-1.0, j5_y-1.25, j5_x-1.0, j5_y+2.0, 0.25, 9)  # CLK_P
    add_track(j5_x, j5_y-1.25, j5_x, j5_y+2.0, 0.25, 12)        # D1_N
    add_track(j5_x+0.5, j5_y-1.25, j5_x+0.5, j5_y+2.0, 0.25, 11)  # D1_P

    # 8. SW_SENSE on B.Cu (via transition to avoid crossing)
    # J4 Pin 7 at (j4_x, Y0+26.35) -> SW1 Pin 1 at (sw1_x-3.25, sw1_y)
    add_track(j4_x, Y0+26.35, j4_x+2.0, Y0+26.35, 0.25, 20, "F.Cu")
    add_via(j4_x+2.0, Y0+26.35, 20)
    add_track(j4_x+2.0, Y0+26.35, sw1_x-3.25, Y0+26.35, 0.25, 20, "B.Cu")
    add_track(sw1_x-3.25, Y0+26.35, sw1_x-3.25, sw1_y+2.0, 0.25, 20, "B.Cu")
    add_via(sw1_x-3.25, sw1_y+2.0, 20)
    add_track(sw1_x-3.25, sw1_y+2.0, sw1_x-3.25, sw1_y, 0.25, 20, "F.Cu")

    # 9. STAT_LED on B.Cu
    # J3 Pin 8 at (j3_x, Y0+28.89) -> D2 Pin 1 at (d2_x-0.95, d2_y)
    add_track(j3_x, Y0+28.89, j3_x+2.0, Y0+28.89, 0.25, 19, "F.Cu")
    add_via(j3_x+2.0, Y0+28.89, 19)
    add_track(j3_x+2.0, Y0+28.89, d2_x-0.95, Y0+28.89, 0.25, 19, "B.Cu")
    add_track(d2_x-0.95, Y0+28.89, d2_x-0.95, d2_y+2.0, 0.25, 19, "B.Cu")
    add_via(d2_x-0.95, d2_y+2.0, 19)
    add_track(d2_x-0.95, d2_y+2.0, d2_x-0.95, d2_y, 0.25, 19, "F.Cu")

    # Ground vias connecting ground pads to B.Cu Ground Pour
    add_via(j1_x+2.54, j1_y+2.5, 1)
    add_via(c1_x+1.75, c1_y+2.5, 1)
    add_via(j2_x+1.0, j2_y+2.0, 1)
    add_via(r1_x+0.95, r1_y+1.5, 1)
    add_via(j3_x-2.0, Y0+16.19, 1)
    add_via(j4_x+2.0, Y0+13.65, 1)
    add_via(j7_x-2.0, j7_y+3.5, 1)
    add_via(sw1_x+3.25, sw1_y+2.0, 1)
    add_via(d2_x+0.95, d2_y+2.0, 1)

    # -------------------------------------------------------------
    # LAYER 2 (B.Cu): SOLID GROUND COPPER POUR ZONE
    # -------------------------------------------------------------
    gnd_zone = f"""\t(zone (net 1) (net_name "GND") (layers "B.Cu") (uuid "{uid()}")
\t\t(hatch edge 0.5)
\t\t(connect_pads (clearance 0.3))
\t\t(min_thickness 0.2)
\t\t(filled_areas_thickness no)
\t\t(fill (thermal_gap 0.3) (thermal_bridge_width 0.4))
\t\t(polygon (pts
\t\t\t(xy {X0} {Y0})
\t\t\t(xy {X0+BW} {Y0})
\t\t\t(xy {X0+BW} {Y0+BH})
\t\t\t(xy {X0} {Y0+BH})
\t\t))
\t)"""

    # Assemble complete .kicad_pcb
    pcb_content = [
        '(kicad_pcb',
        '\t(version 20241229)',
        '\t(generator "pcbnew")',
        '\t(generator_version "10.0")',
        '\t(general',
        '\t\t(thickness 1.6)',
        '\t\t(legacy_teardrops no)',
        '\t)',
        '\t(paper "A4")',
        '\t(title_block',
        '\t\t(title "DASHCAM CARRIER BOARD 2-LAYER PCB")',
        '\t\t(date "2026-10-09")',
        '\t\t(rev "1.4")',
        '\t\t(company "DASHCAM PROTOTYPE PROJECT")',
        '\t\t(comment 1 "Engineer: Souvik H | Regn: IN-ENG-2022-22824")',
        '\t\t(comment 2 "Discipline: EMBEDDED HARDWARE & PCB DESIGN")',
        '\t\t(comment 3 "Dimensions: 60.0 x 38.0 mm | 2-Layer FR4 1.6mm 1oz")',
        '\t\t(comment 4 "Status: RELEASED")',
        '\t)',
        '\t(layers',
        '\t\t(0 "F.Cu" signal)',
        '\t\t(2 "B.Cu" signal)',
        '\t\t(5 "F.SilkS" user "F.Silkscreen")',
        '\t\t(7 "B.SilkS" user "B.Silkscreen")',
        '\t\t(1 "F.Mask" user)',
        '\t\t(3 "B.Mask" user)',
        '\t\t(25 "Edge.Cuts" user)',
        '\t\t(31 "F.CrtYd" user "F.Courtyard")',
        '\t\t(35 "F.Fab" user)',
        '\t)',
        '\t(setup',
        '\t\t(pad_to_mask_clearance 0.05)',
        '\t\t(allow_soldermask_bridges_in_footprints no)',
        '\t\t(pcbplotparams',
        '\t\t\t(layerselection 0x00000000_00000000_55555555_555555f5)',
        '\t\t\t(plot_on_all_layers_selection 0x00000000_00000000_00000000_00000000)',
        '\t\t\t(usegerberextensions yes)',
        '\t\t\t(usegerberattributes yes)',
        '\t\t\t(usegerberadvancedattributes yes)',
        '\t\t\t(creategerberjobfile yes)',
        '\t\t)',
        '\t)',
        net_lines,
        "\n".join(edge_cuts),
        "\n".join(silks),
        "\n".join(footprints),
        "\n".join(tracks),
        "\n".join(vias),
        gnd_zone,
        ')'
    ]

    out_file = os.path.join(CARRIER_DIR, "carrier_board.kicad_pcb")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(pcb_content))
    print(f"[OK] Generated {out_file} (60.0 x 38.0 mm 2-Layer PCB)")
    return out_file

if __name__ == "__main__":
    build_pcb()
