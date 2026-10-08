import os
import uuid
import subprocess
from sym_definitions import LIB_SYMBOLS

BASE_DIR = r"C:\Users\souvk\Downloads\Dashcam_project"
CARRIER_DIR = os.path.join(BASE_DIR, "hardware", "source", "carrier_board")
KICAD_CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"

def uid():
    return str(uuid.uuid4())

class SchematicBuilder:
    def __init__(self):
        self.symbols = []
        self.wires = []
        self.junctions = []
        self.labels = []
        self.texts = []

    def add_symbol(self, lib_id, ref, val, x, y, rot=0, footprint="", pins=[]):
        s_uid = uid()
        lines = []
        lines.append(f'\t(symbol (lib_id "{lib_id}") (at {x} {y} {rot}) (unit 1)')
        lines.append('\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)')
        lines.append(f'\t\t(uuid "{s_uid}")')
        lines.append(f'\t\t(property "Reference" "{ref}" (at {x} {y-2.54} {rot}) (effects (font (size 1.27 1.27))))')
        lines.append(f'\t\t(property "Value" "{val}" (at {x} {y+2.54} {rot}) (effects (font (size 1.27 1.27))))')
        lines.append(f'\t\t(property "Footprint" "{footprint}" (at {x} {y} {rot}) (effects (font (size 1.27 1.27)) (hide yes)))')
        for p in pins:
            lines.append(f'\t\t(pin "{p}" (uuid "{uid()}"))')
        lines.append('\t)')
        self.symbols.append("\n".join(lines))
        return {"lib_id": lib_id, "ref": ref, "val": val, "x": x, "y": y, "rot": rot}

    def add_wire(self, x1, y1, x2, y2):
        x1, y1, x2, y2 = round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)
        if x1 == x2 and y1 == y2:
            return
        self.wires.append(f'\t(wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0) (type default)) (uuid "{uid()}"))')

    def add_junction(self, x, y):
        x, y = round(x, 2), round(y, 2)
        self.junctions.append(f'\t(junction (at {x} {y}) (diameter 0) (color 0 0 0 0) (uuid "{uid()}"))')

    def add_label(self, name, x, y, rot=0):
        x, y = round(x, 2), round(y, 2)
        self.labels.append(f'\t(label "{name}" (at {x} {y} {rot}) (effects (font (size 1.27 1.27))) (uuid "{uid()}"))')

    def add_text(self, txt, x, y, size=1.5):
        self.texts.append(f'\t(text "{txt}" (at {x} {y} 0) (effects (font (size {size} {size}) (bold yes))) (uuid "{uid()}"))')

    def export_schematic(self, filename="carrier_board.kicad_sch"):
        sch_lines = [
            '(kicad_sch',
            '\t(version 20241209)',
            '\t(generator "eeschema")',
            '\t(generator_version "10.0")',
            f'\t(uuid "{uid()}")',
            '\t(paper "A4")',
            '\t(title_block',
            '\t\t(title "DASHCAM CARRIER BOARD SCHEMATIC")',
            '\t\t(date "2026-10-09")',
            '\t\t(rev "1.4")',
            '\t\t(company "DASHCAM PROTOTYPE PROJECT")',
            '\t\t(comment 1 "Engineer: Souvik H | Regn: IN-ENG-2022-22824")',
            '\t\t(comment 2 "Discipline: EMBEDDED SYSTEMS & HARDWARE")',
            '\t\t(comment 3 "Platform: Luckfox Pico Mini B (RV1103) + SC3336 + IP5306")',
            '\t\t(comment 4 "Status: RELEASED")',
            '\t)',
            LIB_SYMBOLS,
            "\n".join(self.texts),
            "\n".join(self.symbols),
            "\n".join(self.wires),
            "\n".join(self.junctions),
            "\n".join(self.labels),
            ')'
        ]
        out_path = os.path.join(CARRIER_DIR, filename)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(sch_lines))
        print(f"[OK] Schematic written to {out_path}")
        return out_path

def generate():
    sb = SchematicBuilder()

    # Section Headers
    sb.add_text("1. AUTOMOTIVE 12V INPUT & LM2596 BUCK PRE-REGULATOR", 25, 22)
    sb.add_text("2. IP5306 BMS & 3.7V LIPO BATTERY BUFFER", 25, 105)
    sb.add_text("3. LUCKFOX PICO MINI B SBC SOCKETS", 145, 22)
    sb.add_text("4. USB WI-FI PORT & USER INTERFACE", 145, 105)
    sb.add_text("5. SMARTSENS SC3336 3MP CAMERA 15-PIN FPC", 225, 22)

    # -----------------------------------------------------------------
    # BLOCK 1: 12V INPUT & LM2596
    # -----------------------------------------------------------------
    # J1: 12V IN
    sb.add_symbol("Connector_Generic:Conn_01x02", "J1", "12V_CAR_IN", 40, 45, footprint="TerminalBlock:TerminalBlock_bornier-2_P5.08mm", pins=["1","2"])
    # J1 Pin 1: (34.92, 45.0) | Pin 2: (34.92, 47.54)

    # D1: SMBJ5.0A TVS (center at 55, 45) -> Pin 1: (55, 41.19), Pin 2: (55, 48.81)
    sb.add_symbol("Device:D_TVS", "D1", "SMBJ5.0A", 55, 45, footprint="Diode_SMD:D_SMB", pins=["1","2"])

    # C1: 470uF/25V (center at 68, 45) -> Pin 1: (68, 41.19), Pin 2: (68, 48.81)
    sb.add_symbol("Device:C_Polarized", "C1", "470uF/25V", 68, 45, footprint="Capacitor_THT:CP_Radial_D8.0mm_P3.50mm", pins=["1","2"])

    # U1: LM2596 (center at 95, 50)
    # Pin 1 (IN+): (81.03, 47.46) | Pin 2 (IN-): (81.03, 52.54)
    # Pin 3 (OUT+): (108.97, 47.46) | Pin 4 (OUT-): (108.97, 52.54)
    sb.add_symbol("Module:LM2596_Module", "U1", "LM2596_BUCK", 95, 50, footprint="Module:LM2596_Module", pins=["1","2","3","4"])

    # C2: 470uF/25V (center at 120, 45) -> Pin 1: (120, 41.19), Pin 2: (120, 48.81)
    sb.add_symbol("Device:C_Polarized", "C2", "470uF/25V", 120, 45, footprint="Capacitor_THT:CP_Radial_D8.0mm_P3.50mm", pins=["1","2"])

    # C3: 100nF (center at 130, 45) -> Pin 1: (130, 41.19), Pin 2: (130, 48.81)
    sb.add_symbol("Device:C", "C3", "100nF", 130, 45, footprint="Capacitor_SMD:C_0805_2012Metric", pins=["1","2"])

    # 12V In Wire & Bus
    sb.add_wire(34.92, 45.0, 34.92, 41.19)
    sb.add_wire(34.92, 41.19, 55.0, 41.19)
    sb.add_junction(55.0, 41.19)
    sb.add_wire(55.0, 41.19, 68.0, 41.19)
    sb.add_junction(68.0, 41.19)
    sb.add_wire(68.0, 41.19, 81.03, 41.19)
    sb.add_wire(81.03, 41.19, 81.03, 47.46) # Into U1 Pin 1
    sb.add_symbol("power:+12V", "#PWR101", "+12V", 34.92, 38.0, pins=["1"])
    sb.add_wire(34.92, 41.19, 34.92, 38.0)

    # Input Ground Bus (at Y=52.54)
    sb.add_wire(34.92, 47.54, 34.92, 52.54)
    sb.add_wire(34.92, 52.54, 55.0, 52.54)
    sb.add_wire(55.0, 48.81, 55.0, 52.54)
    sb.add_junction(55.0, 52.54)
    sb.add_wire(55.0, 52.54, 68.0, 52.54)
    sb.add_wire(68.0, 48.81, 68.0, 52.54)
    sb.add_junction(68.0, 52.54)
    sb.add_wire(68.0, 52.54, 81.03, 52.54) # Into U1 Pin 2
    sb.add_symbol("power:GND", "#PWR102", "GND", 55.0, 55.0, pins=["1"])
    sb.add_wire(55.0, 52.54, 55.0, 55.0)

    # Output +5V_PRE Bus (at Y=41.19)
    sb.add_wire(108.97, 47.46, 108.97, 41.19)
    sb.add_wire(108.97, 41.19, 120.0, 41.19) # Into C2 Pin 1
    sb.add_junction(120.0, 41.19)
    sb.add_wire(120.0, 41.19, 130.0, 41.19) # Into C3 Pin 1
    sb.add_junction(130.0, 41.19)
    sb.add_wire(130.0, 41.19, 138.0, 41.19)
    sb.add_label("+5V_PRE", 138.0, 41.19)

    # Output Ground Bus (at Y=52.54)
    sb.add_wire(108.97, 52.54, 120.0, 52.54)
    sb.add_wire(120.0, 48.81, 120.0, 52.54)
    sb.add_junction(120.0, 52.54)
    sb.add_wire(120.0, 52.54, 130.0, 52.54)
    sb.add_wire(130.0, 48.81, 130.0, 52.54)
    sb.add_junction(130.0, 52.54)
    sb.add_symbol("power:GND", "#PWR103", "GND", 120.0, 55.0, pins=["1"])
    sb.add_wire(120.0, 52.54, 120.0, 55.0)

    # -----------------------------------------------------------------
    # BLOCK 2: BMS & LIPO CHARGER/BOOST (IP5306)
    # -----------------------------------------------------------------
    # J2: JST-PH 2.0mm LiPo Connector (center at 40, 135)
    # Pin 1: (34.92, 135.0) | Pin 2: (34.92, 137.54)
    sb.add_symbol("Connector_Generic:Conn_01x02", "J2", "JST_PH_LIPO", 40, 135, footprint="Connector_JST:JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal", pins=["1","2"])

    # C5: 100nF Battery bypass (center at 55, 135) -> Pin 1: (55, 131.19), Pin 2: (55, 138.81)
    sb.add_symbol("Device:C", "C5", "100nF", 55, 135, footprint="Capacitor_SMD:C_0805_2012Metric", pins=["1","2"])

    # U2: IP5306 BMS (center at 85, 135)
    # Pin 1 (VIN): (71.03, 131.19) | Pin 2 (BAT+): (71.03, 136.27)
    # Pin 3 (VOUT_5V): (98.97, 131.19) | Pin 4 (GND): (85.0, 147.70)
    sb.add_symbol("Module:IP5306_BMS", "U2", "IP5306_BMS", 85, 135, footprint="Module:IP5306_Module", pins=["1","2","3","4"])

    # R1: 100R Keep-Alive Dummy Load (center at 115, 135) -> Pin 1: (115, 131.19), Pin 2: (115, 138.81)
    sb.add_symbol("Device:R", "R1", "100R_0.25W", 115, 135, footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal", pins=["1","2"])

    # C4: 100nF Decoupling (center at 125, 135) -> Pin 1: (125, 131.19), Pin 2: (125, 138.81)
    sb.add_symbol("Device:C", "C4", "100nF", 125, 135, footprint="Capacitor_SMD:C_0805_2012Metric", pins=["1","2"])

    # LiPo Battery VBAT Rail
    sb.add_wire(34.92, 135.0, 55.0, 135.0)
    sb.add_wire(55.0, 131.19, 55.0, 135.0)
    sb.add_junction(55.0, 135.0)
    sb.add_wire(55.0, 135.0, 71.03, 135.0)
    sb.add_wire(71.03, 135.0, 71.03, 136.27) # Into U2 Pin 2 (BAT+)
    sb.add_label("VBAT", 42.0, 133.0)

    # Battery Ground
    sb.add_wire(34.92, 137.54, 34.92, 142.0)
    sb.add_wire(55.0, 138.81, 55.0, 142.0)
    sb.add_wire(34.92, 142.0, 55.0, 142.0)
    sb.add_symbol("power:GND", "#PWR201", "GND", 45.0, 144.0, pins=["1"])
    sb.add_wire(45.0, 142.0, 45.0, 144.0)

    # U2 Input (+5V_PRE)
    sb.add_wire(71.03, 131.19, 62.0, 131.19)
    sb.add_label("+5V_PRE", 62.0, 131.19)

    # U2 GND (Pin 4)
    sb.add_symbol("power:GND", "#PWR202", "GND", 85.0, 150.0, pins=["1"])
    sb.add_wire(85.0, 147.70, 85.0, 150.0)

    # U2 Output (+5V_SYS) Bus (at Y=131.19)
    sb.add_wire(98.97, 131.19, 115.0, 131.19) # Into R1 Pin 1
    sb.add_junction(115.0, 131.19)
    sb.add_wire(115.0, 131.19, 125.0, 131.19) # Into C4 Pin 1
    sb.add_junction(125.0, 131.19)
    sb.add_wire(125.0, 131.19, 135.0, 131.19)
    sb.add_symbol("power:+5V", "#PWR203", "+5V", 135.0, 128.0, pins=["1"])
    sb.add_wire(135.0, 131.19, 135.0, 128.0)
    sb.add_label("+5V_SYS", 135.0, 131.19)

    # Output Ground
    sb.add_wire(115.0, 138.81, 125.0, 138.81)
    sb.add_symbol("power:GND", "#PWR204", "GND", 120.0, 142.0, pins=["1"])
    sb.add_wire(120.0, 138.81, 120.0, 142.0)

    # -----------------------------------------------------------------
    # BLOCK 3: LUCKFOX PICO MINI B SBC SOCKETS
    # -----------------------------------------------------------------
    # J3: Left Socket (center at 165, 55)
    # Pins: Pin 1 at (159.92, 55.0), Pin 2 at (159.92, 57.54), ..., Pin 8 at (159.92, 72.78)
    sb.add_symbol("Connector_Generic:Conn_01x08", "J3", "LUCKFOX_J1_LEFT", 165, 55, footprint="Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical", pins=[str(i) for i in range(1,9)])
    j3_pins = [
        ("1", "UART2_TX", 55.0),
        ("2", "UART2_RX", 57.54),
        ("3", "GND",      60.08),
        ("4", "+3V3",     62.62),
        ("5", "I2C3_SCL", 65.16),
        ("6", "I2C3_SDA", 67.70),
        ("7", "GND",      70.24),
        ("8", "STAT_LED", 72.78)
    ]
    for p_num, p_net, p_y in j3_pins:
        sb.add_wire(159.92, p_y, 150.0, p_y)
        if p_net == "GND":
            sb.add_symbol("power:GND", f"#PWR3_{p_num}", "GND", 150.0, p_y+2.0, pins=["1"])
            sb.add_wire(150.0, p_y, 150.0, p_y+2.0)
        elif p_net == "+3V3":
            sb.add_symbol("power:+3V3", f"#PWR3_{p_num}", "+3V3", 150.0, p_y-2.0, pins=["1"])
            sb.add_wire(150.0, p_y, 150.0, p_y-2.0)
            sb.add_label("+3V3", 146.0, p_y)
        else:
            sb.add_label(p_net, 150.0, p_y)

    # C7: 100nF on +3V3 (center at 145, 75)
    sb.add_symbol("Device:C", "C7", "100nF", 145, 75, footprint="Capacitor_SMD:C_0805_2012Metric", pins=["1","2"])
    sb.add_wire(145.0, 71.19, 145.0, 68.0)
    sb.add_symbol("power:+3V3", "#PWR3_C7", "+3V3", 145.0, 68.0, pins=["1"])
    sb.add_symbol("power:GND", "#PWR3_C7_GND", "GND", 145.0, 81.0, pins=["1"])
    sb.add_wire(145.0, 78.81, 145.0, 81.0)

    # J4: Right Socket (center at 205, 55)
    sb.add_symbol("Connector_Generic:Conn_01x08", "J4", "LUCKFOX_J2_RIGHT", 205, 55, footprint="Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical", pins=[str(i) for i in range(1,9)])
    j4_pins = [
        ("1", "+5V_SYS",  55.0),
        ("2", "GND",      57.54),
        ("3", "USB_DM",   60.08),
        ("4", "USB_DP",   62.62),
        ("5", "CAM_RSTn", 65.16),
        ("6", "CAM_PDN",  67.70),
        ("7", "SW_SENSE", 70.24),
        ("8", "GND",      72.78)
    ]
    for p_num, p_net, p_y in j4_pins:
        sb.add_wire(199.92, p_y, 190.0, p_y)
        if p_net == "GND":
            sb.add_symbol("power:GND", f"#PWR4_{p_num}", "GND", 190.0, p_y+2.0, pins=["1"])
            sb.add_wire(190.0, p_y, 190.0, p_y+2.0)
        elif p_net == "+5V_SYS":
            sb.add_symbol("power:+5V", f"#PWR4_{p_num}", "+5V", 190.0, p_y-2.0, pins=["1"])
            sb.add_wire(190.0, p_y, 190.0, p_y-2.0)
            sb.add_label("+5V_SYS", 185.0, p_y)
        else:
            sb.add_label(p_net, 190.0, p_y)

    # C6: 100nF on +5V_SYS (center at 215, 75)
    sb.add_symbol("Device:C", "C6", "100nF", 215, 75, footprint="Capacitor_SMD:C_0805_2012Metric", pins=["1","2"])
    sb.add_wire(215.0, 71.19, 215.0, 68.0)
    sb.add_symbol("power:+5V", "#PWR3_C6", "+5V", 215.0, 68.0, pins=["1"])
    sb.add_symbol("power:GND", "#PWR3_C6_GND", "GND", 215.0, 81.0, pins=["1"])
    sb.add_wire(215.0, 78.81, 215.0, 81.0)

    # -----------------------------------------------------------------
    # BLOCK 4: USB WI-FI PORT & USER INTERFACE
    # -----------------------------------------------------------------
    # J7: USB-A Female (center at 165, 130)
    # Pins: Pin 1 at (159.92, 130.0), Pin 2 at (159.92, 132.54), Pin 3 at (159.92, 135.08), Pin 4 at (159.92, 137.62)
    sb.add_symbol("Connector_Generic:Conn_01x04", "J7", "USB_WIFI_PORT", 165, 130, footprint="Connector_USB:USB_A_Molex_67643_Horizontal", pins=["1","2","3","4"])
    sb.add_wire(159.92, 130.0, 150.0, 130.0)
    sb.add_symbol("power:+5V", "#PWR4_USB", "+5V", 150.0, 127.0, pins=["1"])
    sb.add_wire(150.0, 130.0, 150.0, 127.0)
    sb.add_label("+5V_SYS", 146.0, 130.0)

    sb.add_wire(159.92, 132.54, 150.0, 132.54)
    sb.add_label("USB_DM", 150.0, 132.54)

    sb.add_wire(159.92, 135.08, 150.0, 135.08)
    sb.add_label("USB_DP", 150.0, 135.08)

    sb.add_wire(159.92, 137.62, 150.0, 137.62)
    sb.add_symbol("power:GND", "#PWR4_USB_GND", "GND", 150.0, 140.0, pins=["1"])
    sb.add_wire(150.0, 137.62, 150.0, 140.0)

    # C9: 100nF on USB VBUS (center at 178, 130)
    sb.add_symbol("Device:C", "C9", "100nF", 178, 130, footprint="Capacitor_SMD:C_0805_2012Metric", pins=["1","2"])
    sb.add_wire(178.0, 126.19, 178.0, 123.0)
    sb.add_symbol("power:+5V", "#PWR4_C9", "+5V", 178.0, 123.0, pins=["1"])
    sb.add_symbol("power:GND", "#PWR4_C9_GND", "GND", 178.0, 136.0, pins=["1"])
    sb.add_wire(178.0, 133.81, 178.0, 136.0)

    # SW1: Pushbutton (center at 165, 160)
    # Pin 1: (159.92, 160.0) | Pin 2: (170.08, 160.0)
    sb.add_symbol("Switch:SW_Push", "SW1", "MODE_SW", 165, 160, footprint="Button_Switch_SMD:SW_Push_1P1T_NO_6x6mm_H9.5mm", pins=["1","2"])
    sb.add_wire(159.92, 160.0, 150.0, 160.0)
    sb.add_label("SW_SENSE", 150.0, 160.0)

    sb.add_wire(170.08, 160.0, 175.0, 160.0)
    sb.add_symbol("power:GND", "#PWR4_SW", "GND", 175.0, 163.0, pins=["1"])
    sb.add_wire(175.0, 160.0, 175.0, 163.0)

    # R2: 10k Pull-Up (center at 145, 160)
    sb.add_symbol("Device:R", "R2", "10k", 145, 160, footprint="Resistor_SMD:R_0805_2012Metric", pins=["1","2"])
    sb.add_wire(145.0, 156.19, 145.0, 153.0)
    sb.add_symbol("power:+3V3", "#PWR4_R2", "+3V3", 145.0, 153.0, pins=["1"])
    sb.add_wire(145.0, 163.81, 145.0, 160.0)
    sb.add_wire(145.0, 160.0, 150.0, 160.0)
    sb.add_junction(150.0, 160.0)

    # D2: Status LED (center at 205, 160) & R3 (center at 190, 160)
    # R3: Pin 1: (190, 156.19), Pin 2: (190, 163.81)
    sb.add_symbol("Device:R", "R3", "470R", 190, 160, footprint="Resistor_SMD:R_0805_2012Metric", pins=["1","2"])
    sb.add_wire(190.0, 156.19, 185.0, 156.19)
    sb.add_label("STAT_LED", 185.0, 156.19)

    # D2: Pin 1: (205, 156.19), Pin 2: (205, 163.81)
    sb.add_symbol("Device:LED", "D2", "STAT_LED_GRN", 205, 160, footprint="LED_SMD:LED_0805_2012Metric", pins=["1","2"])
    sb.add_wire(190.0, 163.81, 205.0, 156.19)
    sb.add_symbol("power:GND", "#PWR4_D2", "GND", 205.0, 167.0, pins=["1"])
    sb.add_wire(205.0, 163.81, 205.0, 167.0)

    # -----------------------------------------------------------------
    # BLOCK 5: SC3336 CAMERA MIPI CSI-2 15-PIN FPC
    # -----------------------------------------------------------------
    # J5: 15-Pin 0.5mm FPC Connector (center at 255, 60)
    # Pins: Pin i at (249.92, 60.0 + (i-1)*2.54)
    sb.add_symbol("Connector_Generic:Conn_01x15", "J5", "SC3336_MIPI_FPC", 255, 60, footprint="Connector_FFC-FPC:Hirose_FH12-15S-0.5SH_1x15-1MP_P0.50mm_Horizontal", pins=[str(i) for i in range(1,16)])
    cam_schedule = [
        ("1",  "GND"),
        ("2",  "MIPI_D0_N"),
        ("3",  "MIPI_D0_P"),
        ("4",  "GND"),
        ("5",  "MIPI_CLK_N"),
        ("6",  "MIPI_CLK_P"),
        ("7",  "GND"),
        ("8",  "MIPI_D1_N"),
        ("9",  "MIPI_D1_P"),
        ("10", "GND"),
        ("11", "CAM_RSTn"),
        ("12", "CAM_PDN"),
        ("13", "I2C3_SCL"),
        ("14", "I2C3_SDA"),
        ("15", "+3V3")
    ]
    for p_num, p_net in cam_schedule:
        idx = int(p_num) - 1
        p_y = 60.0 + idx * 2.54
        sb.add_wire(249.92, p_y, 240.0, p_y)
        if p_net == "GND":
            sb.add_symbol("power:GND", f"#PWR5_{p_num}", "GND", 240.0, p_y+2.0, pins=["1"])
            sb.add_wire(240.0, p_y, 240.0, p_y+2.0)
        elif p_net == "+3V3":
            sb.add_symbol("power:+3V3", f"#PWR5_{p_num}", "+3V3", 240.0, p_y-2.0, pins=["1"])
            sb.add_wire(240.0, p_y, 240.0, p_y-2.0)
            sb.add_label("+3V3", 235.0, p_y)
        else:
            sb.add_label(p_net, 240.0, p_y)

    # C8: 100nF on Camera +3V3 (center at 270, 75)
    sb.add_symbol("Device:C", "C8", "100nF", 270, 75, footprint="Capacitor_SMD:C_0805_2012Metric", pins=["1","2"])
    sb.add_wire(270.0, 71.19, 270.0, 68.0)
    sb.add_symbol("power:+3V3", "#PWR5_C8", "+3V3", 270.0, 68.0, pins=["1"])
    sb.add_symbol("power:GND", "#PWR5_C8_GND", "GND", 270.0, 81.0, pins=["1"])
    sb.add_wire(270.0, 78.81, 270.0, 81.0)

    # Export Schematic
    sb.export_schematic("carrier_board.kicad_sch")

if __name__ == "__main__":
    generate()
