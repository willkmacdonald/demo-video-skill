#!/usr/bin/env python3
"""Example generator: writes src/partials/alarm_rows.html for the Line 3 HMI alarm table.
Pattern to reuse: generate long, repetitive, *deterministic* UI content (log rows, alarm lists,
inbox items) with a small script instead of hand-writing it. Never use randomness."""
from pathlib import Path

ALARMS = [
    ("CONV-03", "JAM_PE_12", "PHOTOEYE 12 BLOCKED > 5 S", "6.2 s", "5.0 s", 2),
    ("CNC-02", "COOLANT_LVL_LO", "COOLANT TANK LEVEL LOW", "18 %", "20 %", 3),
    ("PACK-01", "FILM_SPLICE", "FILM SPLICE DETECTED", "--", "--", 3),
    ("CNC-05", "DOOR_INTLK", "DOOR INTERLOCK OPEN", "OPEN", "CLOSED", 3),
    ("AIR-MAIN", "PRESS_LO", "PLANT AIR PRESSURE LOW", "5.9 bar", "6.0 bar", 2),
    ("WASH-1", "TANK_TEMP_HI", "WASH TANK TEMP HIGH", "63.4 C", "62.0 C", 3),
    ("CNC-08", "COMM_TIMEOUT", "PLC COMM TIMEOUT", "1250 ms", "1000 ms", 1),
    ("CMM-1", "PROBE_CAL_DUE", "PROBE CALIBRATION DUE", "0 d", "0 d", 3),
    ("CNC-01", "TOOL_LIFE_T12", "TOOL T12 LIFE > 90 %", "92 %", "90 %", 3),
    ("PACK-02", "SEAL_Z3_DEV", "SEALER ZONE 3 TEMP DEVIATION", "+4.1 C", "3.0 C", 2),
    ("CNC-04", "SPDL_LOAD_HI", "SPINDLE LOAD HIGH", "96 %", "95 %", 2),
    ("ROBOT-2", "GRIP_RETRY", "GRIPPER RETRY COUNT HIGH", "7", "5", 3),
    ("CNC-03", "CHIP_CONV_OL", "CHIP CONVEYOR OVERLOAD", "TRIP", "--", 2),
    ("CNC-06", "Z_FOLLOW_ERR", "Z AXIS FOLLOWING ERROR WARN", "0.021", "0.020", 2),
    ("HYD-04", "PRESS_DEV", "HYDRAULIC PRESSURE DEVIATION", "-2.1 bar", "2.0 bar", 2),
    ("PACK-01", "LABEL_LOW", "LABEL ROLL LOW", "8 %", "10 %", 3),
    ("CONV-01", "MTR_TEMP_HI", "CONVEYOR MOTOR TEMP HIGH", "81 C", "80 C", 3),
    ("CNC-02", "WAYLUBE_LO", "WAY LUBE LEVEL LOW", "LOW", "--", 3),
    ("CMM-1", "ROOM_TEMP", "ROOM TEMP DRIFT", "21.9 C", "21.5 C", 3),
    ("ESTOP-L3", "ESTOP_TEST", "E-STOP TEST OVERDUE", "31 d", "30 d", 3),
    ("CNC-05", "SPDL_TEMP", "SPINDLE TEMP HIGH", "41 C", "40 C", 2),
    ("VISION-1", "REJ_RATE", "VISION REJECT RATE HIGH", "1.2 %", "1.0 %", 2),
]
VIB = ("CNC-07", "SPDL_VIB_RMS", "SPINDLE VIBRATION HIGH", "7.8 mm/s", "4.5", 2)  # the buried alarm
N_ROWS, NEW_ROWS, VIB_INDEX = 60, 14, 17

out, secs = [], 8 * 3600 + 31
for i in range(N_ROWS):
    area, tag, desc, val, lim, pri = VIB if i == VIB_INDEX else ALARMS[(i * 7 + 3) % len(ALARMS)]
    secs -= 9 + (i * 13) % 37
    h, m, s = secs // 3600, secs % 3600 // 60, secs % 60
    cls = f"ar p{pri}" + (" new" if i < NEW_ROWS else "") + (" vib" if i == VIB_INDEX else "")
    out.append(f'<div class="{cls}"><span class="fl"></span><span class="c-time">{h:02d}:{m:02d}:{s:02d}</span>'
               f'<span class="c-pri">{pri}</span><span class="c-tag">{area}.{tag}</span><span class="c-desc">{desc}</span>'
               f'<span class="c-val">{val}</span><span class="c-lim">{lim}</span><span class="c-st">ACTIVE</span></div>')
dst = Path("src/partials/alarm_rows.html")
dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text("\n".join(out))
print("wrote", dst)
