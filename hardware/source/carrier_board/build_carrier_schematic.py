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
                   ref_hide=False, val_hide=False, pins=[]):
        s_uid = uid()
        rx, ry = round(x + ref_offset[0], 2), round(y + ref_offset[1], 2)
        vx, vy = round(x + val_offset[0], 2), round(y + val_offset[1], 2)
        ref_h = " (hide yes)" if ref_hide else ""
        val_h = " (hide yes)" if val_hide else ""
        
        lines = [
            f'\t(symbol (lib_id "{lib_id}") (at {x} {y} {rot}) (unit 1)',
            '\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)',
            f'\t\t(uuid "{s_uid}")',
            f'\t\t(property "Reference" "{ref}" (at {rx} {ry} {rot}) (effects (font (size 1.27 1.27))){ref_h})',
            f'\t\t(property "Value" "{val}" (at {vx} {vy} {rot}) (effects (font (size 1.27 1.27))){val_h})',
            f'\t\t(property "Footprint" "{footprint}" (at {x} {y} {rot}) (effects (font (size 1.27 1.27)) (hide yes)))'
        ]
        for p in pins:
            lines.append(f'\t\t(pin "{p}" (uuid "{uid()}"))')
        lines.append('\t)')
        self.symbols.append("\n".join(lines))

    def add_power_symbol(self, pwr_type, x, y):
        # Power symbols: Reference is always hidden, Value displayed neatly
        p_uid = uid()
        ref = f"#PWR_{uid()[:6]}"
        val = pwr_type
        if pwr_type == "GND":
            lib_id = "power:GND"
            vx, vy = x, round(y + 2.54, 2)
        elif pwr_type == "+5V":
            lib_id = "power:+5V"
            vx, vy = x, round(y - 2.54, 2)
        elif pwr_type == "+3V3":
            lib_id = "power:+3V3"
            vx, vy = x, round(y - 2.54, 2)
        elif pwr_type == "+12V":
            lib_id = "power:+12V"
            vx, vy = x, round(y - 2.54, 2)
        else:
            lib_id = f"power:{pwr_type}"
            vx, vy = x, round(y - 2.54, 2)

        lines = [
            f'\t(symbol (lib_id "{lib_id}") (at {x} {y} 0) (unit 1)',
            '\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)',
            f'\t\t(uuid "{p_uid}")',
            f'\t\t(property "Reference" "{ref}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))',
            f'\t\t(property "Value" "{val}" (at {vx} {vy} 0) (effects (font (size 1.27 1.27))))',
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

    def add_label(self, name, x, y, rot=0):
        x, y = round(x, 2), round(y, 2)
        self.labels.append(f'\t(label "{name}" (at {x} {y} {rot}) (effects (font (size 1.27 1.27))) (uuid "{uid()}"))')

    def add_text(self, txt, x, y, size=1.5, bold=True):
        b = "yes" if bold else "no"
        self.texts.append(f'\t(text "{txt}" (at {x} {y} 0) (effects (font (size {size} {size}) (bold {b}))) (uuid "{uid()}"))')

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
    sb.add_text("SECTION 1: AUTOMOTIVE 12V-24V INPUT & LM2596 BUCK PRE-REGULATOR", 25, 27, size=1.6)
    sb.add_text("Pre-regulates 12V automotive power to +5V_PRE (2A capacity)", 25, 33, size=1.1, bold=False)

    # J1: 12V Terminal Block (Conn_01x02) at (40, 55)
    # Pin 1 (12V): (34.92, 55.0) | Pin 2 (GND): (34.92, 57.54)
    sb.add_symbol("Connector_Generic:Conn_01x02", "J1", "12V_CAR_IN", 40, 55, 
                  footprint="TerminalBlock:TerminalBlock_bornier-2_P5.08mm",
                  ref_offset=(0, -5.0), val_offset=(0, 6.0), pins=["1", "2"])

    # D1: SMBJ5.0A TVS at (60, 65) - Pins at (60, 61.19) and (60, 68.81)
    sb.add_symbol("Device:D_TVS", "D1", "SMBJ5.0A", 60, 65,
                  footprint="Diode_SMD:D_SMB",
                  ref_offset=(4.5, -2.0), val_offset=(4.5, 2.0), pins=["1", "2"])

    # C1: 470uF/25V Polarized Cap at (75, 65) - Pins at (75, 61.19) and (75, 68.81)
    sb.add_symbol("Device:C_Polarized", "C1", "470uF/25V", 75, 65,
                  footprint="Capacitor_THT:CP_Radial_D8.0mm_P3.50mm",
                  ref_offset=(4.5, -2.0), val_offset=(4.5, 2.0), pins=["1", "2"])

    # U1: LM2596 Buck Module at (115, 65)
    # Pin 1 (IN+): (101.03, 62.46) | Pin 2 (IN-): (101.03, 67.54)
    # Pin 3 (OUT+): (128.97, 62.46) | Pin 4 (OUT-): (128.97, 67.54)
    sb.add_symbol("Module:LM2596_Module", "U1", "LM2596_BUCK", 115, 65,
                  footprint="Module:LM2596_Module",
                  ref_offset=(0, -8.0), val_offset=(0, 9.5), pins=["1", "2", "3", "4"])

    # C2: 470uF/25V Output Filter Cap at (150, 65)
    sb.add_symbol("Device:C_Polarized", "C2", "470uF/25V", 150, 65,
                  footprint="Capacitor_THT:CP_Radial_D8.0mm_P3.50mm",
                  ref_offset=(4.5, -2.0), val_offset=(4.5, 2.0), pins=["1", "2"])

    # C3: 100nF Ceramic Decoupling Cap at (165, 65)
    sb.add_symbol("Device:C", "C3", "100nF", 165, 65,
                  footprint="Capacitor_SMD:C_0805_2012Metric",
                  ref_offset=(4.5, -2.0), val_offset=(4.5, 2.0), pins=["1", "2"])

    # 12V In Rails & Wires (at Y = 50.0 for +12V Bus, Y = 78.0 for GND Bus)
    sb.add_wire(34.92, 55.0, 34.92, 50.0)
    sb.add_wire(34.92, 50.0, 60.0, 50.0)
    sb.add_junction(60.0, 50.0)
    sb.add_wire(60.0, 50.0, 75.0, 50.0)
    sb.add_junction(75.0, 50.0)
    sb.add_wire(75.0, 50.0, 101.03, 50.0)
    sb.add_wire(101.03, 50.0, 101.03, 62.46) # U1 Pin 1

    sb.add_wire(60.0, 50.0, 60.0, 61.19) # D1 Pin 1
    sb.add_wire(75.0, 50.0, 75.0, 61.19) # C1 Pin 1

    sb.add_power_symbol("+12V", 34.92, 46.0)
    sb.add_wire(34.92, 50.0, 34.92, 46.0)

    # Input GND Bus at Y = 78.0
    sb.add_wire(34.92, 57.54, 34.92, 78.0)
    sb.add_wire(34.92, 78.0, 60.0, 78.0)
    sb.add_junction(60.0, 78.0)
    sb.add_wire(60.0, 78.0, 75.0, 78.0)
    sb.add_junction(75.0, 78.0)
    sb.add_wire(75.0, 78.0, 101.03, 78.0)
    sb.add_wire(101.03, 78.0, 101.03, 67.54) # U1 Pin 2

    sb.add_wire(60.0, 68.81, 60.0, 78.0) # D1 Pin 2
    sb.add_wire(75.0, 68.81, 75.0, 78.0) # C1 Pin 2

    sb.add_power_symbol("GND", 60.0, 82.0)
    sb.add_wire(60.0, 78.0, 60.0, 82.0)

    # Output +5V_PRE Bus at Y = 50.0
    sb.add_wire(128.97, 62.46, 128.97, 50.0)
    sb.add_wire(128.97, 50.0, 150.0, 50.0)
    sb.add_junction(150.0, 50.0)
    sb.add_wire(150.0, 50.0, 165.0, 50.0)
    sb.add_junction(165.0, 50.0)
    sb.add_wire(165.0, 50.0, 185.0, 50.0)

    sb.add_wire(150.0, 50.0, 150.0, 61.19) # C2 Pin 1
    sb.add_wire(165.0, 50.0, 165.0, 61.19) # C3 Pin 1

    sb.add_label("+5V_PRE", 185.0, 50.0)

    # Output GND Bus at Y = 78.0
    sb.add_wire(128.97, 67.54, 128.97, 78.0)
    sb.add_wire(128.97, 78.0, 150.0, 78.0)
    sb.add_junction(150.0, 78.0)
    sb.add_wire(150.0, 78.0, 165.0, 78.0)
    sb.add_junction(165.0, 78.0)

    sb.add_wire(150.0, 68.81, 150.0, 78.0) # C2 Pin 2
    sb.add_wire(165.0, 68.81, 165.0, 78.0) # C3 Pin 2

    sb.add_power_symbol("GND", 150.0, 82.0)
    sb.add_wire(150.0, 78.0, 150.0, 82.0)


    # =========================================================================
    # ZONE 2: IP5306 BMS & 3.7V LIPO BATTERY BUFFER
    # X: 20 -> 195, Y: 115 -> 200
    # =========================================================================
    sb.add_box(20, 115, 195, 200)
    sb.add_text("SECTION 2: IP5306 BMS & 3.7V LIPO BATTERY BUFFER", 25, 122, size=1.6)
    sb.add_text("Seamless UPS power path: Charges 1000mAh LiPo & boosts to +5V_SYS", 25, 128, size=1.1, bold=False)

    # J2: JST-PH 2.0mm LiPo Connector at (40, 160)
    # Pin 1 (VBAT): (34.92, 160.0) | Pin 2 (GND): (34.92, 162.54)
    sb.add_symbol("Connector_Generic:Conn_01x02", "J2", "JST_PH_LIPO", 40, 160,
                  footprint="Connector_JST:JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal",
                  ref_offset=(0, -5.0), val_offset=(0, 6.0), pins=["1", "2"])

    # C5: 100nF Battery Bypass Cap at (60, 160)
    sb.add_symbol("Device:C", "C5", "100nF", 60, 160,
                  footprint="Capacitor_SMD:C_0805_2012Metric",
                  ref_offset=(4.5, -2.0), val_offset=(4.5, 2.0), pins=["1", "2"])

    # U2: IP5306 BMS Module at (105, 160)
    # Pin 1 (VIN): (91.03, 156.19) | Pin 2 (BAT+): (91.03, 161.27)
    # Pin 3 (VOUT_5V): (118.97, 156.19) | Pin 4 (GND): (105.0, 172.70)
    sb.add_symbol("Module:IP5306_BMS", "U2", "IP5306_BMS", 105, 160,
                  footprint="Module:IP5306_Module",
                  ref_offset=(0, -9.0), val_offset=(0, 16.0), pins=["1", "2", "3", "4"])

    # R1: 100R Keep-Alive Dummy Load at (145, 160)
    sb.add_symbol("Device:R", "R1", "100R_0.25W", 145, 160,
                  footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal",
                  ref_offset=(4.5, -2.0), val_offset=(4.5, 2.0), pins=["1", "2"])

    # C4: 100nF Output Decoupling Cap at (160, 160)
    sb.add_symbol("Device:C", "C4", "100nF", 160, 160,
                  footprint="Capacitor_SMD:C_0805_2012Metric",
                  ref_offset=(4.5, -2.0), val_offset=(4.5, 2.0), pins=["1", "2"])

    # U2 Input (+5V_PRE)
    sb.add_wire(91.03, 156.19, 75.0, 156.19)
    sb.add_wire(75.0, 156.19, 75.0, 140.0)
    sb.add_wire(75.0, 140.0, 30.0, 140.0)
    sb.add_label("+5V_PRE", 30.0, 140.0)

    # Battery VBAT Wire
    sb.add_wire(34.92, 160.0, 60.0, 160.0)
    sb.add_wire(60.0, 156.19, 60.0, 160.0) # C5 Pin 1
    sb.add_junction(60.0, 160.0)
    sb.add_wire(60.0, 160.0, 91.03, 160.0)
    sb.add_wire(91.03, 160.0, 91.03, 161.27) # U2 Pin 2 (BAT+)
    sb.add_label("VBAT", 45.0, 158.0)

    # Battery GND
    sb.add_wire(34.92, 162.54, 34.92, 175.0)
    sb.add_wire(34.92, 175.0, 60.0, 175.0)
    sb.add_wire(60.0, 163.81, 60.0, 175.0) # C5 Pin 2
    sb.add_power_symbol("GND", 45.0, 178.0)
    sb.add_wire(45.0, 175.0, 45.0, 178.0)

    # U2 GND Pin 4
    sb.add_power_symbol("GND", 105.0, 176.0)
    sb.add_wire(105.0, 172.70, 105.0, 176.0)

    # U2 Output (+5V_SYS) at Y = 145.0
    sb.add_wire(118.97, 156.19, 130.0, 156.19)
    sb.add_wire(130.0, 156.19, 130.0, 145.0)
    sb.add_wire(130.0, 145.0, 145.0, 145.0)
    sb.add_junction(145.0, 145.0)
    sb.add_wire(145.0, 145.0, 160.0, 145.0)
    sb.add_junction(160.0, 145.0)
    sb.add_wire(160.0, 145.0, 185.0, 145.0)

    sb.add_wire(145.0, 145.0, 145.0, 156.19) # R1 Pin 1
    sb.add_wire(160.0, 145.0, 160.0, 156.19) # C4 Pin 1

    sb.add_power_symbol("+5V", 185.0, 140.0)
    sb.add_wire(185.0, 145.0, 185.0, 140.0)
    sb.add_label("+5V_SYS", 185.0, 145.0)

    # Output GND Bus for R1 & C4 at Y = 175.0
    sb.add_wire(145.0, 163.81, 145.0, 175.0)
    sb.add_wire(145.0, 175.0, 160.0, 175.0)
    sb.add_wire(160.0, 163.81, 160.0, 175.0)
    sb.add_power_symbol("GND", 152.5, 178.0)
    sb.add_wire(152.5, 175.0, 152.5, 178.0)


    # =========================================================================
    # ZONE 4: USB 2.0 WI-FI INTERFACE & USER CONTROLS
    # X: 20 -> 195, Y: 205 -> 282
    # =========================================================================
    sb.add_box(20, 205, 195, 282)
    sb.add_text("SECTION 4: USB 2.0 WI-FI DONGLE PORT & USER CONTROLS", 25, 212, size=1.6)
    sb.add_text("Host port for RTL8188EUS Wi-Fi dongle, Mode Tactile Switch & Status LED", 25, 218, size=1.1, bold=False)

    # J7: USB-A Female at (55, 240)
    # Pin 1 (+5V): (49.92, 240.0)
    # Pin 2 (DM):  (49.92, 242.54)
    # Pin 3 (DP):  (49.92, 245.08)
    # Pin 4 (GND): (49.92, 247.62)
    sb.add_symbol("Connector_Generic:Conn_01x04", "J7", "USB_WIFI_PORT", 55, 240,
                  footprint="Connector_USB:USB_A_Molex_67643_Horizontal",
                  ref_offset=(0, -4.5), val_offset=(0, 12.0), pins=["1", "2", "3", "4"])

    # C9: 100nF VBUS Decoupling Cap at (75, 240)
    sb.add_symbol("Device:C", "C9", "100nF", 75, 240,
                  footprint="Capacitor_SMD:C_0805_2012Metric",
                  ref_offset=(4.5, -2.0), val_offset=(4.5, 2.0), pins=["1", "2"])

    # J7 Pin 1 VBUS
    sb.add_wire(49.92, 240.0, 35.0, 240.0)
    sb.add_label("+5V_SYS", 35.0, 240.0)
    sb.add_wire(49.92, 240.0, 75.0, 240.0)
    sb.add_wire(75.0, 240.0, 75.0, 236.19) # C9 Pin 1
    sb.add_power_symbol("GND", 75.0, 248.0)
    sb.add_wire(75.0, 243.81, 75.0, 248.0) # C9 Pin 2

    # J7 Pin 2 USB_DM & Pin 3 USB_DP
    sb.add_wire(49.92, 242.54, 35.0, 242.54)
    sb.add_label("USB_DM", 35.0, 242.54)

    sb.add_wire(49.92, 245.08, 35.0, 245.08)
    sb.add_label("USB_DP", 35.0, 245.08)

    # J7 Pin 4 GND
    sb.add_power_symbol("GND", 45.0, 252.0)
    sb.add_wire(49.92, 247.62, 45.0, 247.62)
    sb.add_wire(45.0, 247.62, 45.0, 252.0)

    # SW1: Mode Pushbutton at (115, 245)
    # Pin 1: (109.92, 245.0) | Pin 2: (120.08, 245.0)
    sb.add_symbol("Switch:SW_Push", "SW1", "MODE_SW", 115, 245,
                  footprint="Button_Switch_SMD:SW_Push_1P1T_NO_6x6mm_H9.5mm",
                  ref_offset=(0, -4.0), val_offset=(0, 4.0), pins=["1", "2"])

    # R2: 10k Pull-Up at (100, 245) - Pins at (100, 241.19) and (100, 248.81)
    sb.add_symbol("Device:R", "R2", "10k", 100, 245,
                  footprint="Resistor_SMD:R_0805_2012Metric",
                  ref_offset=(-4.5, -2.0), val_offset=(-4.5, 2.0), pins=["1", "2"])

    sb.add_power_symbol("+3V3", 100.0, 236.0)
    sb.add_wire(100.0, 241.19, 100.0, 236.0) # R2 Pin 1

    sb.add_wire(100.0, 248.81, 100.0, 255.0) # R2 Pin 2
    sb.add_wire(100.0, 255.0, 109.92, 255.0)
    sb.add_wire(109.92, 255.0, 109.92, 245.0) # Into SW1 Pin 1
    sb.add_junction(109.92, 255.0)
    sb.add_wire(109.92, 255.0, 95.0, 255.0)
    sb.add_label("SW_SENSE", 95.0, 255.0)

    sb.add_power_symbol("GND", 125.0, 250.0)
    sb.add_wire(120.08, 245.0, 125.0, 245.0)
    sb.add_wire(125.0, 245.0, 125.0, 250.0) # SW1 Pin 2

    # LED Indicator circuit: R3 at (155, 245) & D2 at (175, 245)
    sb.add_symbol("Device:R", "R3", "470R", 155, 245,
                  footprint="Resistor_SMD:R_0805_2012Metric",
                  ref_offset=(-4.5, -2.0), val_offset=(-4.5, 2.0), pins=["1", "2"])

    sb.add_symbol("Device:LED", "D2", "STAT_LED_GRN", 175, 245,
                  footprint="LED_SMD:LED_0805_2012Metric",
                  ref_offset=(4.5, -2.0), val_offset=(4.5, 2.0), pins=["1", "2"])

    sb.add_wire(155.0, 241.19, 140.0, 241.19)
    sb.add_label("STAT_LED", 140.0, 241.19)

    sb.add_wire(155.0, 248.81, 155.0, 255.0)
    sb.add_wire(155.0, 255.0, 175.0, 255.0)
    sb.add_wire(175.0, 255.0, 175.0, 241.19) # D2 Pin 1 (Anode)

    sb.add_power_symbol("GND", 175.0, 253.0)
    sb.add_wire(175.0, 248.81, 175.0, 253.0) # D2 Pin 2 (Cathode)


    # =========================================================================
    # ZONE 3: LUCKFOX PICO MINI B SBC PIN SOCKETS (40-PIN EXPANSION)
    # X: 205 -> 405, Y: 20 -> 125
    # =========================================================================
    sb.add_box(205, 20, 405, 125)
    sb.add_text("SECTION 3: LUCKFOX PICO MINI B (RV1103) SBC EXPANSION SOCKETS", 210, 27, size=1.6)
    sb.add_text("Dual 8-Pin 2.54mm pitch female header sockets (J3 Left / J4 Right)", 210, 33, size=1.1, bold=False)

    # J3: Left Socket at (270, 60)
    # Pins: Pin i at (264.92, 60.0 + (i-1)*2.54)
    sb.add_symbol("Connector_Generic:Conn_01x08", "J3", "LUCKFOX_J1_LEFT", 270, 60,
                  footprint="Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical",
                  ref_offset=(0, -4.5), val_offset=(0, 23.0), pins=[str(i) for i in range(1, 9)])

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
        sb.add_wire(264.92, p_y, 225.0, p_y)
        if p_net == "GND":
            sb.add_power_symbol("GND", 225.0, p_y)
        elif p_net == "+3V3":
            sb.add_power_symbol("+3V3", 225.0, p_y)
            sb.add_label("+3V3", 218.0, p_y)
        else:
            sb.add_label(p_net, 225.0, p_y)

    # C7: 100nF on +3V3 at (285, 70)
    sb.add_symbol("Device:C", "C7", "100nF", 285, 70,
                  footprint="Capacitor_SMD:C_0805_2012Metric",
                  ref_offset=(4.5, -2.0), val_offset=(4.5, 2.0), pins=["1", "2"])
    sb.add_power_symbol("+3V3", 285.0, 63.0)
    sb.add_wire(285.0, 66.19, 285.0, 63.0)
    sb.add_power_symbol("GND", 285.0, 78.0)
    sb.add_wire(285.0, 73.81, 285.0, 78.0)

    # J4: Right Socket at (360, 60)
    # Pins: Pin i at (354.92, 60.0 + (i-1)*2.54)
    sb.add_symbol("Connector_Generic:Conn_01x08", "J4", "LUCKFOX_J2_RIGHT", 360, 60,
                  footprint="Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical",
                  ref_offset=(0, -4.5), val_offset=(0, 23.0), pins=[str(i) for i in range(1, 9)])

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
        sb.add_wire(354.92, p_y, 315.0, p_y)
        if p_net == "GND":
            sb.add_power_symbol("GND", 315.0, p_y)
        elif p_net == "+5V_SYS":
            sb.add_power_symbol("+5V", 315.0, p_y)
            sb.add_label("+5V_SYS", 308.0, p_y)
        else:
            sb.add_label(p_net, 315.0, p_y)

    # C6: 100nF on +5V_SYS at (380, 70)
    sb.add_symbol("Device:C", "C6", "100nF", 380, 70,
                  footprint="Capacitor_SMD:C_0805_2012Metric",
                  ref_offset=(4.5, -2.0), val_offset=(4.5, 2.0), pins=["1", "2"])
    sb.add_power_symbol("+5V", 380.0, 63.0)
    sb.add_wire(380.0, 66.19, 380.0, 63.0)
    sb.add_power_symbol("GND", 380.0, 78.0)
    sb.add_wire(380.0, 73.81, 380.0, 78.0)


    # =========================================================================
    # ZONE 5: SMARTSENS SC3336 3MP CAMERA MIPI CSI-2 INTERFACE
    # X: 205 -> 295, Y: 135 -> 282
    # =========================================================================
    sb.add_box(205, 135, 295, 282)
    sb.add_text("SECTION 5: SC3336 CAMERA MIPI CSI-2", 210, 142, size=1.6)
    sb.add_text("15-Pin 0.5mm FPC (2-Lane MIPI + I2C)", 210, 148, size=1.1, bold=False)

    # J5: Conn_01x15 at (265, 165)
    # Pin i at (259.92, 165.0 + (i-1)*2.54)
    sb.add_symbol("Connector_Generic:Conn_01x15", "J5", "SC3336_MIPI_FPC", 265, 165,
                  footprint="Connector_FFC-FPC:Hirose_FH12-15S-0.5SH_1x15-1MP_P0.50mm_Horizontal",
                  ref_offset=(0, -4.5), val_offset=(0, 41.0), pins=[str(i) for i in range(1, 16)])

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
        p_y = 165.0 + idx * 2.54
        sb.add_wire(259.92, p_y, 220.0, p_y)
        if p_net == "GND":
            sb.add_power_symbol("GND", 220.0, p_y)
        elif p_net == "+3V3":
            sb.add_power_symbol("+3V3", 220.0, p_y)
            sb.add_label("+3V3", 213.0, p_y)
        else:
            sb.add_label(p_net, 220.0, p_y)

    # C8: 100nF on Camera +3V3 at (280, 205)
    sb.add_symbol("Device:C", "C8", "100nF", 280, 205,
                  footprint="Capacitor_SMD:C_0805_2012Metric",
                  ref_offset=(4.5, -2.0), val_offset=(4.5, 2.0), pins=["1", "2"])
    sb.add_power_symbol("+3V3", 280.0, 198.0)
    sb.add_wire(280.0, 201.19, 280.0, 198.0)
    sb.add_power_symbol("GND", 280.0, 213.0)
    sb.add_wire(280.0, 208.81, 280.0, 213.0)


    # =========================================================================
    # ZONE 6: TITLE BLOCK AREA (RESERVED)
    # X: 300 -> 405, Y: 220 -> 285
    # The title block is rendered automatically by KiCad eeschema inside this zone!
    # We add an architectural note box right above it:
    # =========================================================================
    sb.add_box(305, 135, 405, 215)
    sb.add_text("DASHCAM PROTOTYPE ARCHITECTURE SUMMARY", 310, 142, size=1.5)
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
        sb.add_text(n, 310, 150 + i * 7.5, size=1.05, bold=False)

    # Export
    sb.export_schematic("carrier_board.kicad_sch")

if __name__ == "__main__":
    build()
