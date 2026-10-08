import os
import subprocess

BASE_DIR = r"C:\Users\souvk\Downloads\Dashcam_project"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def get_sheet_html(title, doc_no, discipline, rev="1.4", date="2026-10-08", sheet_str="1 OF 1", content_html="", status="RELEASED"):
    return f"""
<div class="a4-sheet">
    <div class="outer-border">
        <!-- Coordinate Marks -->
        <div class="grid-mark grid-top-1">1</div>
        <div class="grid-mark grid-top-2">2</div>
        <div class="grid-mark grid-top-3">3</div>
        <div class="grid-mark grid-bottom-1">1</div>
        <div class="grid-mark grid-bottom-2">2</div>
        <div class="grid-mark grid-bottom-3">3</div>
        <div class="grid-mark grid-left-a">A</div>
        <div class="grid-mark grid-left-b">B</div>
        <div class="grid-mark grid-right-a">A</div>
        <div class="grid-mark grid-right-b">B</div>

        <div class="inner-border">
            <!-- Specification / Drawing Content Area -->
            <div class="drawing-canvas">
                {content_html}
            </div>

            <!-- Full Width Title Block Strip with ZERO GAP from lower margin -->
            <div class="title-block-group">
                <!-- Left Empty Space Box: Projection Symbol -->
                <div class="title-box-proj">
                    <svg class="proj-symbol" viewBox="0 0 100 36" preserveAspectRatio="xMidYMid meet">
                        <!-- Horizontal center line (ISO long-dash dot chain line) -->
                        <line x1="4" y1="18" x2="96" y2="18" stroke="#000000" stroke-width="0.7" stroke-dasharray="6,2,1.5,2" />
                        
                        <!-- Concentric circles (Third Angle: left side) -->
                        <circle cx="27" cy="18" r="11" fill="none" stroke="#000000" stroke-width="1.2" />
                        <circle cx="27" cy="18" r="5.5" fill="none" stroke="#000000" stroke-width="1.2" />
                        <!-- Vertical centerline through circles -->
                        <line x1="27" y1="4" x2="27" y2="32" stroke="#000000" stroke-width="0.7" stroke-dasharray="6,2,1.5,2" />

                        <!-- Truncated cone / Frustum (Third Angle: right side, small base left, large base right) -->
                        <polygon points="53,12.5 75,7 75,29 53,23.5" fill="none" stroke="#000000" stroke-width="1.2" stroke-linejoin="miter" />
                        <line x1="53" y1="12.5" x2="53" y2="23.5" stroke="#000000" stroke-width="1.2" />
                        <line x1="75" y1="7" x2="75" y2="29" stroke="#000000" stroke-width="1.2" />
                    </svg>
                </div>

                <!-- Adjacent Left Box: Organization, Project, Title, Rev -->
                <table class="title-box-left">
                    <tr>
                        <td style="width: 82%;">
                            <span class="field-label">Organization / Project</span>
                            <span class="field-val large">DASHCAM PROTOTYPE PROJECT</span>
                        </td>
                        <td style="width: 18%;">
                            <span class="field-label">Size</span>
                            <span class="field-val">A4</span>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="field-label">Document Title</span>
                            <span class="field-val large">{title}</span>
                        </td>
                        <td>
                            <span class="field-label">Rev</span>
                            <span class="field-val">{rev}</span>
                        </td>
                    </tr>
                </table>

                <!-- Original Legend Box: Document Control & Approvals -->
                <table class="title-box-right">
                    <tr>
                        <td style="width: 44%;">
                            <span class="field-label">Document Number</span>
                            <span class="field-val">{doc_no}</span>
                        </td>
                        <td style="width: 34%;">
                            <span class="field-label">Date</span>
                            <span class="field-val">{date}</span>
                        </td>
                        <td style="width: 22%;">
                            <span class="field-label">Sheet</span>
                            <span class="field-val">{sheet_str}</span>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="field-label">Design Engineer</span>
                            <span class="field-val">Souvik H</span>
                        </td>
                        <td colspan="2">
                            <span class="field-label">Engineer Registration No.</span>
                            <span class="field-val">IN-ENG-2022-22824</span>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="field-label">Engineering Discipline</span>
                            <span class="field-val">{discipline}</span>
                        </td>
                        <td colspan="2">
                            <span class="field-label">Status</span>
                            <span class="field-val">{status}</span>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</div>
"""

CSS_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Engineering Specification Sheet</title>
    <style>
        @page {
            size: A4 landscape;
            margin: 0;
        }
        * {
            box-sizing: border-box;
        }
        body {
            margin: 0;
            padding: 0;
            background: #ffffff;
            font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
            -webkit-print-color-adjust: exact;
        }
        .a4-sheet {
            width: 297mm;
            height: 210mm;
            position: relative;
            background: #ffffff;
            padding: 8mm;
            page-break-after: always;
            overflow: hidden;
        }
        .outer-border {
            width: 100%;
            height: 100%;
            border: 2px solid #000000;
            position: relative;
            padding: 4mm;
        }
        .inner-border {
            width: 100%;
            height: 100%;
            border: 1px solid #000000;
            position: relative;
        }
        .grid-mark {
            position: absolute;
            font-size: 8pt;
            font-weight: bold;
            color: #000000;
            line-height: 1;
        }
        .grid-top-1 { top: 1mm; left: 25%; }
        .grid-top-2 { top: 1mm; left: 50%; }
        .grid-top-3 { top: 1mm; left: 75%; }
        .grid-bottom-1 { bottom: 1mm; left: 25%; }
        .grid-bottom-2 { bottom: 1mm; left: 50%; }
        .grid-bottom-3 { bottom: 1mm; left: 75%; }
        .grid-left-a { left: 1.2mm; top: 25%; }
        .grid-left-b { left: 1.2mm; top: 75%; }
        .grid-right-a { right: 1.2mm; top: 25%; }
        .grid-right-b { right: 1.2mm; top: 75%; }

        .drawing-canvas {
            position: absolute;
            top: 5mm;
            left: 7mm;
            right: 7mm;
            bottom: 26mm;
            overflow: hidden;
            font-size: 8pt;
            line-height: 1.35;
            color: #111111;
        }
        .drawing-canvas h1 {
            font-size: 11pt;
            margin: 0 0 2mm 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 1.5px solid #000000;
            padding-bottom: 1mm;
        }
        .drawing-canvas h2 {
            font-size: 9pt;
            margin: 2mm 0 1mm 0;
            text-transform: uppercase;
            border-bottom: 1px solid #666;
            padding-bottom: 0.5mm;
        }
        .drawing-canvas p {
            margin: 1mm 0;
        }
        .drawing-canvas table.tech-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 7.2pt;
            margin: 1.5mm 0;
        }
        .drawing-canvas table.tech-table th,
        .drawing-canvas table.tech-table td {
            border: 1px solid #333333;
            padding: 1mm 1.5mm;
            text-align: left;
        }
        .drawing-canvas table.tech-table th {
            background-color: #f2f2f2;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 6.8pt;
        }
        .code-box {
            background: #fafafa;
            border: 1px solid #999;
            padding: 1.5mm;
            font-family: "Courier New", Courier, monospace;
            font-size: 6.8pt;
            line-height: 1.2;
            white-space: pre;
            margin: 1.5mm 0;
        }

        /* Title block strip spanning full bottom width */
        .title-block-group {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            display: flex;
            align-items: flex-end;
            height: 23mm;
            z-index: 10;
        }

        /* Left Empty Space Box: Projection Symbol */
        .title-box-proj {
            flex: 1;
            height: 11.5mm;
            border-top: 1px solid #000000;
            border-right: 1.5px solid #000000;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #ffffff;
            padding: 0.5mm 1mm;
        }
        .proj-symbol {
            width: 100%;
            height: 100%;
            max-height: 9.5mm;
            display: block;
        }

        .title-box-left {
            width: 115mm;
            height: 23mm;
            border-collapse: collapse;
            background: #ffffff;
            border-top: 1.5px solid #000000;
            border-left: none;
            border-right: none;
            border-bottom: none;
            table-layout: fixed;
        }
        .title-box-left tr {
            height: 11.5mm;
        }
        .title-box-left td {
            border-top: 1px solid #000000;
            border-left: 1px solid #000000;
            border-right: none;
            border-bottom: none;
            padding: 1.2mm 2.2mm;
            vertical-align: top;
            font-family: "Courier New", Courier, monospace, Arial, sans-serif;
        }
        .title-box-right {
            width: 125mm;
            height: 23mm;
            border-collapse: collapse;
            background: #ffffff;
            border-top: 1.5px solid #000000;
            border-left: 1.5px solid #000000;
            border-right: none;
            border-bottom: none;
            table-layout: fixed;
        }
        .title-box-right tr {
            height: 7.66mm;
        }
        .title-box-right td {
            border-top: 1px solid #000000;
            border-left: 1px solid #000000;
            border-right: none;
            border-bottom: none;
            padding: 1mm 2mm;
            vertical-align: top;
            font-family: "Courier New", Courier, monospace, Arial, sans-serif;
        }
        .field-label {
            font-size: 5.5pt;
            font-weight: bold;
            text-transform: uppercase;
            color: #555555;
            display: block;
            margin-bottom: 0.3mm;
            font-family: Arial, sans-serif;
            line-height: 1;
        }
        .field-val {
            font-size: 7pt;
            font-weight: bold;
            color: #000000;
            line-height: 1.1;
            display: block;
        }
        .field-val.large {
            font-size: 8.5pt;
        }
        @media print {
            body { background: none; }
            .a4-sheet { box-shadow: none; padding: 8mm; }
        }
    </style>
</head>
<body>
"""

CSS_FOOTER = """
</body>
</html>
"""

print("Template builder ready with test_sheet.html engineering bottom format.")
