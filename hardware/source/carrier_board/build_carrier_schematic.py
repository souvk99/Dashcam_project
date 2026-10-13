import os
import uuid
from sym_definitions import LIB_SYMBOLS

BASE_DIR = r"C:\Users\souvk\Downloads\Dashcam_project"
CARRIER_DIR = os.path.join(BASE_DIR, "hardware", "source", "carrier_board")

def uid():
    return str(uuid.uuid4())

class SchematicBuilder:
    def __init__(self):
        self.symbols = []
        self.wires = []
        self.junctions = []
        self.labels = []
        self.texts = []
        self.shapes = []

    def add_symbol(self, lib_id, ref, val, x, y, rot=0, footprint="", 
                   ref_offset=(0, -2.54), val_offset=(0, 2.54), 
                   ref_justify=None, val_justify=None,
                   ref_hide=False, val_hide=False, pins=[]):
        s_uid = uid()
        rx, ry = round(x + ref_offset[0], 2), round(y + ref_offset[1], 2)
        vx, vy = round(x + val_offset[0], 2), round(y + val_offset[1], 2)
        ref_h = " (hide yes)" if ref_hide else ""
        val_h = " (hide yes)" if val_hide else ""

        if ref_justify is None:
            if ref_offset[0] > 0:
                ref_justify = "left"
            elif ref_offset[0] < 0:
                ref_justify = "right"
            else:
                ref_justify = ""
        if val_justify is None:
            if val_offset[0] > 0:
                val_justify = "left"
            elif val_offset[0] < 0:
                val_justify = "right"
            else:
                val_justify = ""

        ref_j = f" (justify {ref_justify})" if ref_justify else ""
        val_j = f" (justify {val_justify})" if val_justify else ""
        
        lines = [
            f'\t(symbol (lib_id "{lib_id}") (at {x} {y} {rot}) (unit 1)',
            '\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)',
            f'\t\t(uuid "{s_uid}")',
            f'\t\t(property "Reference" "{ref}" (at {rx} {ry} 0) (effects (font (size 1.27 1.27)){ref_j}){ref_h})',
            f'\t\t(property "Value" "{val}" (at {vx} {vy} 0) (effects (font (size 1.27 1.27)){val_j}){val_h})',
            f'\t\t(property "Footprint" "{footprint}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))'
        ]
        for p in pins:
            lines.append(f'\t\t(pin "{p}" (uuid "{uid()}"))')
        lines.append('\t)')
        self.symbols.append("\n".join(lines))

    def add_power_symbol(self, pwr_type, x, y):
        # Power symbols: Reference is always hidden, Value displayed with clean clearance from arrow/triangle
        p_uid = uid()
        ref = f"#PWR_{uid()[:6]}"
        val = pwr_type
        if pwr_type == "GND":
            lib_id = "power:GND"
            vx, vy = round(x, 2), round(y + 4.2, 2)
        elif pwr_type == "+5V":
            lib_id = "power:+5V"
            vx, vy = round(x, 2), round(y - 4.0, 2)
        elif pwr_type == "+3V3":
            lib_id = "power:+3V3"
            vx, vy = round(x, 2), round(y - 4.0, 2)
        elif pwr_type == "+12V":
            lib_id = "power:+12V"
            vx, vy = round(x, 2), round(y - 4.0, 2)
        else:
            lib_id = f"power:{pwr_type}"
            vx, vy = round(x, 2), round(y - 4.0, 2)

        lines = [
            f'\t(symbol (lib_id "{lib_id}") (at {x} {y} 0) (unit 1)',
            '\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)',
            f'\t\t(uuid "{p_uid}")',
            f'\t\t(property "Reference" "{ref}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))',
            f'\t\t(property "Value" "{val}" (at {vx} {vy} 0) (effects (font (size 1.15 1.15))))',
            f'\t\t(property "Footprint" "" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))',
            f'\t\t(pin "1" (uuid "{uid()}"))',
            '\t)'
        ]
        self.symbols.append("\n".join(lines))

    def add_wire(self, x1, y1, x2, y2):
        x1, y1, x2, y2 = round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)
        if x1 == x2 and y1 == y2:
            return
        self.wires.append(f'\t(wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0) (type default)) (uuid "{uid()}"))')

    def add_junction(self, x, y):
        x, y = round(x, 2), round(y, 2)
        self.junctions.append(f'\t(junction (at {x} {y}) (diameter 0) (color 0 0 0 0) (uuid "{uid()}"))')

    def add_label(self, name, x, y, rot=0, justify="left bottom", size=1.15):
        x, y = round(x, 2), round(y, 2)
        j_str = f" (justify {justify})" if justify else ""
        self.labels.append(f'\t(label "{name}" (at {x} {y} {rot}) (effects (font (size {size} {size})){j_str}) (uuid "{uid()}"))')

    def add_text(self, txt, x, y, size=1.5, bold=True, justify="left"):
        b = "yes" if bold else "no"
        j_str = f" (justify {justify})" if justify else ""
        self.texts.append(f'\t(text "{txt}" (at {x} {y} 0) (effects (font (size {size} {size}) (bold {b})){j_str}) (uuid "{uid()}"))')

    def add_box(self, x1, y1, x2, y2):
        # Dashed border rectangle around functional blocks
        self.shapes.append(f'\t(polyline (pts (xy {x1} {y1}) (xy {x2} {y1}) (xy {x2} {y2}) (xy {x1} {y2}) (xy {x1} {y1})) (stroke (width 0.25) (type dash)) (fill (type none)) (uuid "{uid()}"))')

    def export_schematic(self, filename="carrier_board.kicad_sch"):
        sch_lines = [
            '(kicad_sch',
            '\t(version 20241209)',
            '\t(generator "eeschema")',
            '\t(generator_version "10.0")',
            f'\t(uuid "{uid()}")',
            '\t(paper "A3")',
            '\t(title_block',
            '\t\t(title "DASHCAM CARRIER BOARD SCHEMATIC")',
            '\t\t(date "2026-10-11")',
            '\t\t(rev "1.4")',
            '\t\t(company "DASHCAM PROTOTYPE PROJECT")',
            '\t\t(comment 1 "Engineer: Souvik H | Regn: IN-ENG-2022-22824")',
            '\t\t(comment 2 "Discipline: EMBEDDED SYSTEMS & HARDWARE")',
            '\t\t(comment 3 "Luckfox Pico Mini B (RV1103) + SC3336 + IP5306 + RTL8188EUS")',
            '\t\t(comment 4 "Status: RELEASED")',
            '\t)',
            LIB_SYMBOLS,
            "\n".join(self.shapes),
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
        print(f"[OK] Perfect Schematic written to {out_path}")
        return out_path

def build():
    sb = SchematicBuilder()

    # =========================================================================
    # ZONE 1: 12V AUTOMOTIVE INPUT & LM2596 BUCK PRE-REGULATOR
    # X: 20 -> 195, Y: 20 -> 108
    # =========================================================================
    sb.add_box(20, 20, 195, 108)
    sb.add_text("SECTION 1: AUTOMOTIVE 12V-24V INPUT & LM2596 BUCK PRE-REGULATOR", 24, 27, size=1.55)
    sb.add_text("Pre-regulates 12V automotive power to +5V_PRE (2A capacity)", 24, 33, size=1.1, bold=False)

    # J1: 12V Terminal Block (Conn_01x02) at (42, 62)
    # Pin 1 (12V): (36.92, 62.0) | Pin 2 (GND): (36.92, 64.54)
    sb.add_symbol("Connector_Generic:Conn_01x02", "J1", "12V_CAR_IN", 42, 62, 
                  footprint="TerminalBlock:TerminalBlock_bornier-2_P5.08mm",
                  ref_offset=(0, -4.5), val_offset=(0, 6.8), pins=["1", "2"])

    # D1: SMBJ5.0A TVS at (58, 64) - Pins at (58, 60.19) and (58, 67.81)
    sb.add_symbol("Device:D_TVS", "D1", "SMBJ5.0A", 58, 64,
                  footprint="Diode_SMD:D_SMB",
                  ref_offset=(2.5, -1.8), val_offset=(2.5, 1.8), pins=["1", "2"])

    # C1: 470uF/25V Polarized Cap at (78, 64) - Pins at (78, 60.19) and (78, 67.81)
    sb.add_symbol("Device:C_Polarized", "C1", "470uF/25V", 78, 64,
                  footprint="Capacitor_THT:CP_Radial_D8.0mm_P3.50mm",
                  ref_offset=(2.8, -1.8), val_offset=(2.8, 1.8), pins=["1", "2"])

    # U1: LM2596 Buck Module at (118, 64)
    # Pin 1 (IN+): (104.03, 61.46) | Pin 2 (IN-): (104.03, 66.54)
    # Pin 3 (OUT+): (131.97, 61.46) | Pin 4 (OUT-): (131.97, 66.54)
    sb.add_symbol("Module:LM2596_Module", "U1", "LM2596_BUCK", 118, 64,
                  footprint="Module:LM2596_Module",
                  ref_offset=(0, -8.2), val_offset=(0, 10.5), pins=["1", "2", "3", "4"])

    # C2: 470uF/25V Output Filter Cap at (148, 64)
    sb.add_symbol("Device:C_Polarized", "C2", "470uF/25V", 148, 64,
                  footprint="Capacitor_THT:CP_Radial_D8.0mm_P3.50mm",
                  ref_offset=(2.8, -1.8), val_offset=(2.8, 1.8), pins=["1", "2"])

    # C3: 100nF Ceramic Decoupling Cap at (168, 64)
    sb.add_symbol("Device:C", "C3", "100nF", 168, 64,
                  footprint="Capacitor_SMD:C_0805_2012Metric",
                  ref_offset=(2.8, -1.8), val_offset=(2.8, 1.8), pins=["1", "2"])

    # 12V In Rails & Wires (at Y = 48.0 for +12V Bus, Y = 80.0 for GND Bus)
    sb.add_wire(36.92, 62.0, 28.0, 62.0)
    sb.add_wire(28.0, 62.0, 28.0, 48.0)
    sb.add_junction(28.0, 48.0)
    sb.add_power_symbol("+12V", 28.0, 44.0)
    sb.add_wire(28.0, 48.0, 28.0, 44.0)

    sb.add_wire(28.0, 48.0, 58.0, 48.0)
    sb.add_junction(58.0, 48.0)
    sb.add_wire(58.0, 48.0, 78.0, 48.0)
    sb.add_junction(78.0, 48.0)
    sb.add_wire(78.0, 48.0, 97.0, 48.0)
    sb.add_wire(97.0, 48.0, 97.0, 61.46)
    sb.add_wire(97.0, 61.46, 104.03, 61.46) # U1 Pin 1

    sb.add_wire(58.0, 48.0, 58.0, 60.19) # D1 Pin 1
    sb.add_wire(78.0, 48.0, 78.0, 60.19) # C1 Pin 1

    # Input GND Bus at Y = 80.0
    sb.add_wire(36.92, 64.54, 32.0, 64.54)
    sb.add_wire(32.0, 64.54, 32.0, 80.0)
    sb.add_wire(32.0, 80.0, 58.0, 80.0)
    sb.add_junction(58.0, 80.0)
    sb.add_wire(58.0, 80.0, 78.0, 80.0)
    sb.add_junction(78.0, 80.0)
    sb.add_wire(78.0, 80.0, 97.0, 80.0)
    sb.add_wire(97.0, 80.0, 97.0, 66.54)
    sb.add_wire(97.0, 66.54, 104.03, 66.54) # U1 Pin 2

    sb.add_wire(58.0, 67.81, 58.0, 80.0) # D1 Pin 2
    sb.add_wire(78.0, 67.81, 78.0, 80.0) # C1 Pin 2

    sb.add_power_symbol("GND", 58.0, 84.0)
    sb.add_wire(58.0, 80.0, 58.0, 84.0)

    # Output +5V_PRE Bus at Y = 48.0
    sb.add_wire(131.97, 61.46, 138.0, 61.46)
    sb.add_wire(138.0, 61.46, 138.0, 48.0)
    sb.add_wire(138.0, 48.0, 148.0, 48.0)
    sb.add_junction(148.0, 48.0)
    sb.add_wire(148.0, 48.0, 168.0, 48.0)
    sb.add_junction(168.0, 48.0)
    sb.add_wire(168.0, 48.0, 188.0, 48.0)

    sb.add_wire(148.0, 48.0, 148.0, 60.19) # C2 Pin 1
    sb.add_wire(168.0, 48.0, 168.0, 60.19) # C3 Pin 1

    sb.add_label("+5V_PRE", 188.0, 48.0, justify="right bottom")

    # Output GND Bus at Y = 80.0
    sb.add_wire(131.97, 66.54, 138.0, 66.54)
    sb.add_wire(138.0, 66.54, 138.0, 80.0)
    sb.add_wire(138.0, 80.0, 148.0, 80.0)
    sb.add_junction(148.0, 80.0)
    sb.add_wire(148.0, 80.0, 168.0, 80.0)

    sb.add_wire(148.0, 67.81, 148.0, 80.0) # C2 Pin 2
    sb.add_wire(168.0, 67.81, 168.0, 80.0) # C3 Pin 2

    sb.add_power_symbol("GND", 148.0, 84.0)
    sb.add_wire(148.0, 80.0, 148.0, 84.0)


    # =========================================================================
    # ZONE 2: IP5306 BMS & 3.7V LIPO BATTERY BUFFER
    # X: 20 -> 195, Y: 115 -> 200
    # =========================================================================
    sb.add_box(20, 115, 195, 200)
    sb.add_text("SECTION 2: IP5306 BMS & 3.7V LIPO BATTERY BUFFER", 24, 122, size=1.55)
    sb.add_text("Seamless UPS power path: Charges 1000mAh LiPo & boosts to +5V_SYS", 24, 128, size=1.1, bold=False)

    # J2: JST-PH 2.0mm LiPo Connector at (42, 163)
    # Pin 1 (VBAT): (36.92, 163.0) | Pin 2 (GND): (36.92, 165.54)
    sb.add_symbol("Connector_Generic:Conn_01x02", "J2", "JST_PH_LIPO", 42, 163,
                  footprint="Connector_JST:JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal",
                  ref_offset=(0, -4.5), val_offset=(0, 6.8), pins=["1", "2"])

    # C5: 100nF Battery Bypass Cap at (62, 165) - Pins at (62, 161.19) and (62, 168.81)
    sb.add_symbol("Device:C", "C5", "100nF", 62, 165,
                  footprint="Capacitor_SMD:C_0805_2012Metric",
                  ref_offset=(2.8, -1.8), val_offset=(2.8, 1.8), pins=["1", "2"])

    # U2: IP5306 BMS Module at (105, 160)
    # Pin 1 (VIN): (91.03, 156.19) | Pin 2 (BAT+): (91.03, 161.27)
    # Pin 3 (VOUT_5V): (118.97, 156.19) | Pin 4 (GND): (105.0, 172.70)
    sb.add_symbol("Module:IP5306_BMS", "U2", "IP5306_BMS", 105, 160,
                  footprint="Module:IP5306_Module",
                  ref_offset=(0, -11.5), val_offset=(0, -8.5), pins=["1", "2", "3", "4"])

    # R1: 100R Keep-Alive Dummy Load at (140, 160)
    sb.add_symbol("Device:R", "R1", "100R_0.25W", 140, 160,
                  footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal",
                  ref_offset=(2.5, -1.8), val_offset=(2.5, 1.8), pins=["1", "2"])

    # C4: 100nF Output Decoupling Cap at (166, 160)
    sb.add_symbol("Device:C", "C4", "100nF", 166, 160,
                  footprint="Capacitor_SMD:C_0805_2012Metric",
                  ref_offset=(2.8, -1.8), val_offset=(2.8, 1.8), pins=["1", "2"])

    # U2 Input (+5V_PRE)
    sb.add_wire(91.03, 156.19, 80.0, 156.19)
    sb.add_wire(80.0, 156.19, 80.0, 141.0)
    sb.add_wire(80.0, 141.0, 28.0, 141.0)
    sb.add_label("+5V_PRE", 28.0, 141.0, justify="left bottom")

    # Battery VBAT Wire at Y = 152.0 (cleanly above J2 and C5)
    sb.add_wire(36.92, 163.0, 28.0, 163.0)
    sb.add_wire(28.0, 163.0, 28.0, 152.0)
    sb.add_wire(28.0, 152.0, 44.0, 152.0)
    sb.add_wire(44.0, 152.0, 62.0, 152.0)
    sb.add_junction(62.0, 152.0)
    sb.add_wire(62.0, 152.0, 62.0, 161.19) # C5 Pin 1
    sb.add_wire(62.0, 152.0, 84.0, 152.0)
    sb.add_wire(84.0, 152.0, 84.0, 161.27)
    sb.add_wire(84.0, 161.27, 91.03, 161.27) # U2 Pin 2 (BAT+)
    sb.add_label("VBAT", 44.0, 152.0, justify="left bottom")

    # Battery GND at Y = 178.0
    sb.add_wire(36.92, 165.54, 32.0, 165.54)
    sb.add_wire(32.0, 165.54, 32.0, 178.0)
    sb.add_wire(32.0, 178.0, 62.0, 178.0)
    sb.add_junction(62.0, 178.0)
    sb.add_wire(62.0, 168.81, 62.0, 178.0) # C5 Pin 2
    sb.add_power_symbol("GND", 62.0, 182.0)
    sb.add_wire(62.0, 178.0, 62.0, 182.0)

    # U2 GND Pin 4
    sb.add_power_symbol("GND", 105.0, 177.0)
    sb.add_wire(105.0, 172.70, 105.0, 177.0)

    # U2 Output (+5V_SYS) at Y = 145.0
    sb.add_wire(118.97, 156.19, 126.0, 156.19)
    sb.add_wire(126.0, 156.19, 126.0, 145.0)
    sb.add_wire(126.0, 145.0, 140.0, 145.0)
    sb.add_junction(140.0, 145.0)
    sb.add_wire(140.0, 145.0, 166.0, 145.0)
    sb.add_junction(166.0, 145.0)
    sb.add_wire(166.0, 145.0, 186.0, 145.0)

    sb.add_wire(140.0, 145.0, 140.0, 156.19) # R1 Pin 1
    sb.add_wire(166.0, 145.0, 166.0, 156.19) # C4 Pin 1

    sb.add_power_symbol("+5V", 186.0, 140.0)
    sb.add_wire(186.0, 145.0, 186.0, 140.0)
    sb.add_label("+5V_SYS", 186.0, 145.0, justify="right bottom")

    # Output GND Bus for R1 & C4 at Y = 178.0
    sb.add_wire(140.0, 163.81, 140.0, 178.0)
    sb.add_wire(140.0, 178.0, 153.0, 178.0)
    sb.add_junction(153.0, 178.0)
    sb.add_wire(153.0, 178.0, 166.0, 178.0)
    sb.add_wire(166.0, 163.81, 166.0, 178.0)
    sb.add_power_symbol("GND", 153.0, 182.0)
    sb.add_wire(153.0, 178.0, 153.0, 182.0)


    # =========================================================================
    # ZONE 4: USB 2.0 WI-FI INTERFACE & USER CONTROLS
    # X: 20 -> 195, Y: 205 -> 282
    # =========================================================================
    sb.add_box(20, 205, 195, 282)
    sb.add_text("SECTION 4: USB 2.0 WI-FI DONGLE PORT & USER CONTROLS", 24, 212, size=1.55)
    sb.add_text("Host port for RTL8188EUS Wi-Fi dongle, Mode Tactile Switch & Status LED", 24, 218, size=1.1, bold=False)

    # J7: USB-A Female at (62, 244)
    # Pin 1 (+5V): (56.92, 244.0)
    # Pin 2 (DM):  (56.92, 246.54)
    # Pin 3 (DP):  (56.92, 249.08)
    # Pin 4 (GND): (56.92, 251.62)
    sb.add_symbol("Connector_Generic:Conn_01x04", "J7", "USB_WIFI_PORT", 62, 244,
                  footprint="Connector_USB:USB_A_Molex_67643_Horizontal",
                  ref_offset=(0, -4.5), val_offset=(0, 12.0), pins=["1", "2", "3", "4"])

    # C9: 100nF VBUS Decoupling Cap at (80, 244)
    sb.add_symbol("Device:C", "C9", "100nF", 80, 244,
                  footprint="Capacitor_SMD:C_0805_2012Metric",
                  ref_offset=(2.8, -1.8), val_offset=(2.8, 1.8), pins=["1", "2"])

    # J7 Pin 1 VBUS (+5V_SYS) & C9 connection routed cleanly above J7
    sb.add_wire(56.92, 244.0, 50.0, 244.0)
    sb.add_junction(50.0, 244.0)
    sb.add_wire(50.0, 244.0, 28.0, 244.0)
    sb.add_label("+5V_SYS", 28.0, 244.0, justify="left bottom")

    sb.add_wire(50.0, 244.0, 50.0, 234.0)
    sb.add_wire(50.0, 234.0, 80.0, 234.0)
    sb.add_wire(80.0, 234.0, 80.0, 240.19) # C9 Pin 1
    sb.add_power_symbol("GND", 80.0, 252.0)
    sb.add_wire(80.0, 247.81, 80.0, 252.0) # C9 Pin 2

    # J7 Pin 2 USB_DM & Pin 3 USB_DP
    sb.add_wire(56.92, 246.54, 28.0, 246.54)
    sb.add_label("USB_DM", 28.0, 246.54, justify="left bottom")

    sb.add_wire(56.92, 249.08, 28.0, 249.08)
    sb.add_label("USB_DP", 28.0, 249.08, justify="left bottom")

    # J7 Pin 4 GND (routed left to X=44 to clear USB_WIFI_PORT label)
    sb.add_wire(56.92, 251.62, 44.0, 251.62)
    sb.add_wire(44.0, 251.62, 44.0, 258.0)
    sb.add_power_symbol("GND", 44.0, 258.0)

    # R2: 10k Pull-Up at (114, 239) - Pins at (114, 235.19) and (114, 242.81)
    sb.add_symbol("Device:R", "R2", "10k", 114, 239,
                  footprint="Resistor_SMD:R_0805_2012Metric",
                  ref_offset=(-2.5, -1.8), val_offset=(-2.5, 1.8), pins=["1", "2"])

    sb.add_power_symbol("+3V3", 114.0, 231.0)
    sb.add_wire(114.0, 235.19, 114.0, 231.0) # R2 Pin 1

    # SW1: Mode Pushbutton at (128, 252)
    # Pin 1: (122.92, 252.0) | Pin 2: (133.08, 252.0)
    sb.add_symbol("Switch:SW_Push", "SW1", "MODE_SW", 128, 252,
                  footprint="Button_Switch_SMD:SW_Push_1P1T_NO_6x6mm_H9.5mm",
                  ref_offset=(0, -4.2), val_offset=(0, 4.5), pins=["1", "2"])

    sb.add_wire(114.0, 242.81, 114.0, 252.0) # R2 Pin 2 down to node
    sb.add_junction(114.0, 252.0)
    sb.add_wire(114.0, 252.0, 122.92, 252.0) # Node right to SW1 Pin 1
    sb.add_wire(114.0, 252.0, 96.0, 252.0)   # Node left to SW_SENSE
    sb.add_label("SW_SENSE", 96.0, 252.0, justify="left bottom")

    sb.add_wire(133.08, 252.0, 138.0, 252.0)
    sb.add_wire(138.0, 252.0, 138.0, 258.0) # SW1 Pin 2 to GND
    sb.add_power_symbol("GND", 138.0, 258.0)

    # LED Indicator circuit: R3 at (160, 238) & D2 at (174, 250)
    # R3 Pins: (160, 234.19) and (160, 241.81)
    sb.add_symbol("Device:R", "R3", "470R", 160, 238,
                  footprint="Resistor_SMD:R_0805_2012Metric",
                  ref_offset=(-2.5, -1.8), val_offset=(-2.5, 1.8), pins=["1", "2"])

    # D2 Pins: Pin 1 Anode at (174, 246.19) | Pin 2 Cathode at (174, 253.81)
    sb.add_symbol("Device:LED", "D2", "STAT_LED_GRN", 174, 250,
                  footprint="LED_SMD:LED_0805_2012Metric",
                  ref_offset=(4.2, -1.8), val_offset=(4.2, 1.8), pins=["1", "2"])

    sb.add_wire(160.0, 234.19, 160.0, 232.0)
    sb.add_wire(160.0, 232.0, 144.0, 232.0)
    sb.add_label("STAT_LED", 144.0, 232.0, justify="left bottom")

    sb.add_wire(160.0, 241.81, 160.0, 244.0)
    sb.add_wire(160.0, 244.0, 174.0, 244.0)
    sb.add_wire(174.0, 244.0, 174.0, 246.19) # D2 Pin 1 (Anode - top)

    sb.add_wire(174.0, 253.81, 174.0, 258.0) # D2 Pin 2 (Cathode - bottom)
    sb.add_power_symbol("GND", 174.0, 258.0)


    # =========================================================================
    # ZONE 3: LUCKFOX PICO MINI B SBC PIN SOCKETS (40-PIN EXPANSION)
    # X: 205 -> 405, Y: 20 -> 125
    # =========================================================================
    sb.add_box(205, 20, 405, 125)
    sb.add_text("SECTION 3: LUCKFOX PICO MINI B (RV1103) SBC EXPANSION SOCKETS", 210, 27, size=1.55)
    sb.add_text("Dual 8-Pin 2.54mm pitch female header sockets (J3 Left / J4 Right)", 210, 33, size=1.1, bold=False)

    # J3: Left Socket at (268, 60)
    # Pins: Pin i at (262.92, 60.0 + (i-1)*2.54)
    sb.add_symbol("Connector_Generic:Conn_01x08", "J3", "LUCKFOX_J1_LEFT", 268, 60,
                  footprint="Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical",
                  ref_offset=(0, -4.5), val_offset=(0, 23.5), pins=[str(i) for i in range(1, 9)])

    j3_signals = [
        ("1", "UART2_TX", 60.0),
        ("2", "UART2_RX", 62.54),
        ("3", "GND",      65.08),
        ("4", "+3V3",     67.62),
        ("5", "I2C3_SCL", 70.16),
        ("6", "I2C3_SDA", 72.70),
        ("7", "GND",      75.24),
        ("8", "STAT_LED", 77.78)
    ]
    for p_num, p_net, p_y in j3_signals:
        if p_net == "GND":
            sb.add_wire(262.92, p_y, 220.0, p_y)
        else:
            sb.add_wire(262.92, p_y, 228.0, p_y)
            sb.add_label(p_net, 228.0, p_y, justify="left bottom", size=1.05)

    # Vertical GND bus for J3 Pins 3 & 7 (zero wire crossings!)
    sb.add_wire(220.0, 65.08, 220.0, 75.24)
    sb.add_junction(220.0, 75.24)
    sb.add_wire(220.0, 75.24, 220.0, 84.0)
    sb.add_power_symbol("GND", 220.0, 84.0)

    # C7: 100nF on +3V3 at (288, 68)
    sb.add_symbol("Device:C", "C7", "100nF", 288, 68,
                  footprint="Capacitor_SMD:C_0805_2012Metric",
                  ref_offset=(2.8, -1.8), val_offset=(2.8, 1.8), pins=["1", "2"])
    sb.add_power_symbol("+3V3", 288.0, 61.0)
    sb.add_wire(288.0, 64.19, 288.0, 61.0)
    sb.add_power_symbol("GND", 288.0, 76.0)
    sb.add_wire(288.0, 71.81, 288.0, 76.0)

    # J4: Right Socket at (358, 60)
    # Pins: Pin i at (352.92, 60.0 + (i-1)*2.54)
    sb.add_symbol("Connector_Generic:Conn_01x08", "J4", "LUCKFOX_J2_RIGHT", 358, 60,
                  footprint="Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical",
                  ref_offset=(0, -4.5), val_offset=(0, 23.5), pins=[str(i) for i in range(1, 9)])

    j4_signals = [
        ("1", "+5V_SYS",  60.0),
        ("2", "GND",      62.54),
        ("3", "USB_DM",   65.08),
        ("4", "USB_DP",   67.62),
        ("5", "CAM_RSTn", 70.16),
        ("6", "CAM_PDN",  72.70),
        ("7", "SW_SENSE", 75.24),
        ("8", "GND",      77.78)
    ]
    for p_num, p_net, p_y in j4_signals:
        if p_net == "GND":
            sb.add_wire(352.92, p_y, 312.0, p_y)
        else:
            sb.add_wire(352.92, p_y, 318.0, p_y)
            sb.add_label(p_net, 318.0, p_y, justify="left bottom", size=1.05)

    # Vertical GND bus for J4 Pins 2 & 8
    sb.add_wire(312.0, 62.54, 312.0, 77.78)
    sb.add_junction(312.0, 77.78)
    sb.add_wire(312.0, 77.78, 312.0, 84.0)
    sb.add_power_symbol("GND", 312.0, 84.0)

    # C6: 100nF on +5V_SYS at (378, 68)
    sb.add_symbol("Device:C", "C6", "100nF", 378, 68,
                  footprint="Capacitor_SMD:C_0805_2012Metric",
                  ref_offset=(2.8, -1.8), val_offset=(2.8, 1.8), pins=["1", "2"])
    sb.add_power_symbol("+5V", 378.0, 61.0)
    sb.add_wire(378.0, 64.19, 378.0, 61.0)
    sb.add_power_symbol("GND", 378.0, 76.0)
    sb.add_wire(378.0, 71.81, 378.0, 76.0)


    # =========================================================================
    # ZONE 5: SMARTSENS SC3336 3MP CAMERA MIPI CSI-2 INTERFACE
    # X: 205 -> 298, Y: 135 -> 282
    # =========================================================================
    sb.add_box(205, 135, 298, 282)
    sb.add_text("SECTION 5: SC3336 CAMERA MIPI CSI-2", 209, 142, size=1.45)
    sb.add_text("15-Pin 0.5mm FPC (2-Lane MIPI + I2C)", 209, 148, size=1.05, bold=False)

    # J5: Conn_01x15 at (260, 165)
    # Pin i at (254.92, 165.0 + (i-1)*2.54)
    sb.add_symbol("Connector_Generic:Conn_01x15", "J5", "SC3336_MIPI_FPC", 260, 165,
                  footprint="Connector_FFC-FPC:Hirose_FH12-15S-0.5SH_1x15-1MP_P0.50mm_Horizontal",
                  ref_offset=(0, -4.5), val_offset=(0, 41.5), pins=[str(i) for i in range(1, 16)])

    cam_signals = [
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
    for p_num, p_net in cam_signals:
        idx = int(p_num) - 1
        p_y = round(165.0 + idx * 2.54, 2)
        if p_net == "GND":
            sb.add_wire(254.92, p_y, 215.0, p_y)
        else:
            sb.add_wire(254.92, p_y, 223.0, p_y)
            sb.add_label(p_net, 223.0, p_y, justify="left bottom", size=1.0)

    # Vertical GND bus for J5 Pins 1, 4, 7, 10 (zero wire crossings!)
    sb.add_wire(215.0, 165.0, 215.0, 172.62)
    sb.add_junction(215.0, 172.62)
    sb.add_wire(215.0, 172.62, 215.0, 180.24)
    sb.add_junction(215.0, 180.24)
    sb.add_wire(215.0, 180.24, 215.0, 187.86)
    sb.add_junction(215.0, 187.86)
    sb.add_wire(215.0, 187.86, 215.0, 206.0)
    sb.add_power_symbol("GND", 215.0, 206.0)

    # C8: 100nF on Camera +3V3 at (278, 180) - well above SC3336_MIPI_FPC label
    sb.add_symbol("Device:C", "C8", "100nF", 278, 180,
                  footprint="Capacitor_SMD:C_0805_2012Metric",
                  ref_offset=(2.8, -1.8), val_offset=(2.8, 1.8), pins=["1", "2"])
    sb.add_power_symbol("+3V3", 278.0, 173.0)
    sb.add_wire(278.0, 176.19, 278.0, 173.0)
    sb.add_power_symbol("GND", 278.0, 188.0)
    sb.add_wire(278.0, 183.81, 278.0, 188.0)


    # =========================================================================
    # ZONE 6: TITLE BLOCK AREA (RESERVED)
    # X: 300 -> 405, Y: 220 -> 285
    # The title block is rendered automatically by KiCad eeschema inside this zone!
    # We add an architectural note box right above it:
    # =========================================================================
    sb.add_box(303, 135, 405, 215)
    sb.add_text("DASHCAM PROTOTYPE ARCHITECTURE SUMMARY", 307, 142, size=1.4)
    notes = [
        "- SoC: Rockchip RV1103 (Cortex-A7 @ 1.2GHz + 0.5TOPS NPU)",
        "- Sensor: SmartSens SC3336 3MP CMOS (2304x1296 @ 30fps)",
        "- Video: Hardware H.264/H.265 encoder via RTSP streaming",
        "- Power Input: 12V-24V Car Accessory Socket via LM2596 Buck",
        "- UPS Buffer: IP5306 + 3.7V 1000mAh LiPo (Safe shutdown)",
        "- Connectivity: RTL8188EUS 2.4GHz 802.11b/g/n USB Wi-Fi",
        "- PCB Spec: 2-Layer FR4, 1.6mm thickness, 1oz copper",
        "- Form Factor: 65.0 x 42.0 mm (Matching Luckfox Pico Mini B)"
    ]
    for i, n in enumerate(notes):
        sb.add_text(n, 307, 150 + i * 7.5, size=1.0, bold=False)

    # Export
    sb.export_schematic("carrier_board.kicad_sch")

if __name__ == "__main__":
    build()
