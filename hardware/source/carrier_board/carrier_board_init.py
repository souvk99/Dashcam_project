import os
import uuid
import subprocess

BASE_DIR = r"C:\Users\souvk\Downloads\Dashcam_project"
CARRIER_DIR = os.path.join(BASE_DIR, "hardware", "source", "carrier_board")
KICAD_CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"

os.makedirs(CARRIER_DIR, exist_ok=True)

def uid():
    return str(uuid.uuid4())

# Create basic .kicad_pro
pro_content = """{
  "meta": {
    "filename": "carrier_board.kicad_pro",
    "version": 1
  },
  "schematic": {
    "annotate_start_num": 1,
    "drawing": {
      "dashed_lines_dash_length_ratio": 12.0,
      "dashed_lines_gap_length_ratio": 3.0,
      "default_line_thickness": 0.1524,
      "default_text_size": 1.27,
      "field_names": [],
      "pin_symbol_size": 0.0,
      "text_offset_ratio": 0.2
    }
  },
  "sheets": [
    [
      "965d9afc-0787-45ba-b7bc-21944b47b74d",
      ""
    ]
  ]
}
"""

with open(os.path.join(CARRIER_DIR, "carrier_board.kicad_pro"), "w", encoding="utf-8") as f:
    f.write(pro_content)

print("[OK] Created carrier_board.kicad_pro")
