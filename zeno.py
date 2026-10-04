#!/usr/bin/env python3
"""
Zeno - dark flat hub UI (PyQt6).
Run:  pip install PyQt6  &&  python zeno.py
Demo: python zeno.py --demo-shot ./shots
"""
import ctypes
import ctypes
import ctypes.wintypes
import json
import math
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PyQt6.QtCore import Qt, QUrl, QSize, QRegularExpression, QThread, pyqtSignal, QRectF, QPointF
from PyQt6.QtGui import (QColor, QDesktopServices, QFont, QFontDatabase, QFontMetricsF,
                         QIcon, QPen, QPainter, QPainterPath, QPixmap,
                         QSyntaxHighlighter, QTextCharFormat)
from PyQt6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QDialog, QFileDialog, QFrame,
                             QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox,
                             QPushButton, QScrollArea, QSpinBox, QStackedWidget,
                             QVBoxLayout, QWidget, QPlainTextEdit)

# ============================================================================ INJECTION LOGIC
LUAU_STRING_LEN = 2147483647

PROCESS_VM_WRITE = 0x0020
PROCESS_VM_OPERATION = 0x0008
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_CREATE_THREAD = 0x0002
PROCESS_VM_READ = 0x0010
PROCESS_ALL_ACCESS = 0x1F0FFF

MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
MEM_COMMIT_RESERVE = 0x3000
MEM_RELEASE = 0x8000

PAGE_READWRITE = 0x04
PAGE_EXECUTE_READWRITE = 0x40
PAGE_EXECUTE_READ = 0x20

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

kernel32.OpenProcess.argtypes = [ctypes.wintypes.DWORD, ctypes.wintypes.BOOL, ctypes.wintypes.DWORD]
kernel32.OpenProcess.restype = ctypes.wintypes.HANDLE

kernel32.VirtualAllocEx.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.LPVOID, ctypes.c_size_t, ctypes.wintypes.DWORD, ctypes.wintypes.DWORD]
kernel32.VirtualAllocEx.restype = ctypes.wintypes.LPVOID

kernel32.VirtualFreeEx.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.LPVOID, ctypes.c_size_t, ctypes.wintypes.DWORD]
kernel32.VirtualFreeEx.restype = ctypes.wintypes.BOOL

kernel32.WriteProcessMemory.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.LPVOID, ctypes.wintypes.LPCVOID, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
kernel32.WriteProcessMemory.restype = ctypes.wintypes.BOOL

kernel32.GetModuleHandleA.argtypes = [ctypes.wintypes.LPCSTR]
kernel32.GetModuleHandleA.restype = ctypes.wintypes.HMODULE

kernel32.CreateRemoteThread.argtypes = [ctypes.wintypes.HANDLE, ctypes.c_void_p, ctypes.c_size_t, ctypes.wintypes.LPVOID, ctypes.wintypes.LPVOID, ctypes.wintypes.DWORD, ctypes.POINTER(ctypes.wintypes.DWORD)]
kernel32.CreateRemoteThread.restype = ctypes.wintypes.HANDLE

kernel32.WaitForSingleObject.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD]
kernel32.WaitForSingleObject.restype = ctypes.wintypes.DWORD

kernel32.GetExitCodeThread.argtypes = [ctypes.wintypes.HANDLE, ctypes.POINTER(ctypes.wintypes.DWORD)]
kernel32.GetExitCodeThread.restype = ctypes.wintypes.BOOL

kernel32.CloseHandle.argtypes = [ctypes.wintypes.HANDLE]
kernel32.CloseHandle.restype = ctypes.wintypes.BOOL

# ============================================================================ INJECTION LOGIC
LUAU_STRING_LEN = 2147483647

PROCESS_VM_WRITE = 0x0020
PROCESS_VM_OPERATION = 0x0008
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_CREATE_THREAD = 0x0002
PROCESS_VM_READ = 0x0010
PROCESS_ALL_ACCESS = 0x1F0FFF

MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
MEM_COMMIT_RESERVE = 0x3000
MEM_RELEASE = 0x8000

PAGE_READWRITE = 0x04
PAGE_EXECUTE_READWRITE = 0x40
PAGE_EXECUTE_READ = 0x20

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

kernel32.OpenProcess.argtypes = [ctypes.wintypes.DWORD, ctypes.wintypes.BOOL, ctypes.wintypes.DWORD]
kernel32.OpenProcess.restype = ctypes.wintypes.HANDLE

kernel32.VirtualAllocEx.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.LPVOID, ctypes.c_size_t, ctypes.wintypes.DWORD, ctypes.wintypes.DWORD]
kernel32.VirtualAllocEx.restype = ctypes.wintypes.LPVOID

kernel32.VirtualFreeEx.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.LPVOID, ctypes.c_size_t, ctypes.wintypes.DWORD]
kernel32.VirtualFreeEx.restype = ctypes.wintypes.BOOL

kernel32.WriteProcessMemory.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.LPVOID, ctypes.wintypes.LPCVOID, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
kernel32.WriteProcessMemory.restype = ctypes.wintypes.BOOL

kernel32.GetModuleHandleA.argtypes = [ctypes.wintypes.LPCSTR]
kernel32.GetModuleHandleA.restype = ctypes.wintypes.HMODULE

kernel32.CreateRemoteThread.argtypes = [ctypes.wintypes.HANDLE, ctypes.c_void_p, ctypes.c_size_t, ctypes.wintypes.LPVOID, ctypes.wintypes.LPVOID, ctypes.wintypes.DWORD, ctypes.POINTER(ctypes.wintypes.DWORD)]
kernel32.CreateRemoteThread.restype = ctypes.wintypes.HANDLE

kernel32.WaitForSingleObject.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD]
kernel32.WaitForSingleObject.restype = ctypes.wintypes.DWORD

kernel32.GetExitCodeThread.argtypes = [ctypes.wintypes.HANDLE, ctypes.POINTER(ctypes.wintypes.DWORD)]
kernel32.GetExitCodeThread.restype = ctypes.wintypes.BOOL

kernel32.CloseHandle.argtypes = [ctypes.wintypes.HANDLE]
kernel32.CloseHandle.restype = ctypes.wintypes.BOOL

class RobloxInjector:
    """Injects Lua scripts into running Roblox processes using WeAreDevs DLL."""

    def __init__(self):
        self.roblox_process = None
        self.injected = False
        self.handle = None
        self.dll_path = None
        self.dll_handle = None

    def set_target_pid(self, pid):
        """Set a specific PID to inject into (skip auto-detection)."""
        self.roblox_process = int(pid)
        print("Set target PID: {}".format(self.roblox_process))

    def load_wearedevs_dll(self):
        """Load the WeAreDevs exploit API DLL."""
        # Check if DLL exists in the same directory as the script
        script_dir = Path(__file__).parent
        dll_path = script_dir / "wearedevs_exploit_api.dll"

        if not dll_path.exists():
            # Try looking in Downloads/New folder
            alt_path = Path.home() / "Downloads" / "New folder" / "wearedevs_exploit_api.dll"
            if alt_path.exists():
                dll_path = alt_path
            else:
                return False, "wearedevs_exploit_api.dll not found. Please place it in the same directory as zeno.py"

        try:
            self.dll_handle = ctypes.windll.LoadLibrary(str(dll_path))
            self.dll_path = str(dll_path)
            print("[OK] Loaded WeAreDevs DLL from: {}".format(dll_path))
            return True, "DLL loaded"
        except Exception as e:
            return False, "Failed to load DLL: {}".format(str(e))

    def launch_exploit(self):
        """Initialize the WeAreDevs exploit."""
        if not self.dll_handle:
            success, msg = self.load_wearedevs_dll()
            if not success:
                return False, msg

        try:
            # WeAreDevs API: launch() function
            launch_func = self.dll_handle.launch
            launch_func.argtypes = []
            launch_func.restype = ctypes.c_bool
            result = launch_func()
            if result:
                print("[OK] Exploit launched successfully")
                return True, "Exploit launched"
            else:
                return False, "Exploit launch failed"
        except Exception as e:
            return False, "Launch error: {}".format(str(e))

    def check_attached(self):
        """Check if attached to Roblox."""
        if not self.dll_handle:
            return False, "DLL not loaded"

        try:
            # WeAreDevs API: isattached() function
            attached_func = self.dll_handle.isattached
            attached_func.argtypes = []
            attached_func.restype = ctypes.c_bool
            result = attached_func()
            return result, "Attached" if result else "Not attached"
        except Exception as e:
            return False, "Check error: {}".format(str(e))

    def execute_script(self, script):
        """Execute a Lua script via WeAreDevs API."""
        if not self.dll_handle:
            success, msg = self.load_wearedevs_dll()
            if not success:
                return False, msg

        try:
            # WeAreDevs API: execute() function
            execute_func = self.dll_handle.execute
            execute_func.argtypes = [ctypes.c_char_p]
            execute_func.restype = ctypes.c_bool
            result = execute_func(script.encode('utf-8'))
            if result:
                print("[OK] Script executed successfully")
                return True, "Script executed"
            else:
                return False, "Script execution failed"
        except Exception as e:
            return False, "Execute error: {}".format(str(e))

    def find_roblox_process(self) -> tuple[bool, str]:
        """Find a running Roblox process by name or window title."""
        try:
            # Use simplified CSV parsing like Client Manager
            result = subprocess.run(
                ["tasklist", "/FO", "CSV", "/NH"],
                capture_output=True,
                text=True,
                timeout=10
            )

            lines = result.stdout.strip().split("\n")
            for line in lines:
                parts = line.split('","')
                if len(parts) >= 2:
                    name = parts[0].strip('"')
                    pid = parts[1].strip('"')
                    if "roblox" in name.lower():
                        self.roblox_process = int(pid)
                        print("Found Roblox process: PID {} ({})".format(pid, name))
                        return True, "PID {}".format(pid)

            return False, "No Roblox process found. Make sure Roblox is running."

        except FileNotFoundError:
            return False, "tasklist command not found. Make sure you're running as Administrator."
        except subprocess.TimeoutExpired:
            return False, "Timeout waiting for process list."
        except Exception as e:
            return False, "Error finding Roblox process: {}".format(str(e))

    def get_process_handle(self, pid: int) -> tuple[bool, str]:
        """Open a handle to the target process."""
        try:
            handle = kernel32.OpenProcess(
                PROCESS_VM_WRITE | PROCESS_VM_OPERATION | PROCESS_QUERY_INFORMATION,
                False,
                pid
            )

            if not handle:
                error_code = ctypes.get_last_error()
                return False, "Failed to open process (Error {})".format(error_code)

            print("[OK] Successfully opened process handle for PID {}".format(pid))
            self.handle = int(handle)
            return True, str(self.handle)

        except Exception as e:
            return False, "Error opening process: {}".format(str(e))

    def inject_script_content(self, script_content):
        """Inject a Lua script using WeAreDevs API (bypasses Hyperion)."""
        # Launch the exploit first
        success, msg = self.launch_exploit()
        if not success:
            return False, msg

        # Check if attached
        attached, msg = self.check_attached()
        if not attached:
            print("[WARN] Not attached to Roblox: {}".format(msg))
            # Try to attach by launching again
            success, msg = self.launch_exploit()
            if not success:
                return False, "Failed to attach: {}".format(msg)

        # Execute the script
        success, msg = self.execute_script(script_content)
        if success:
            return True, "Script executed via WeAreDevs API"
        else:
            return False, msg

# ============================================================================ END INJECTION LOGIC

# ------------------------------------------------------------------ config
APP_NAME = "Zeno"
VERSION = "v1.0.0"
DATA_DIR = Path.home() / ".zeno-hub"
SETTINGS_FILE = DATA_DIR / "settings.json"

# Put your real links here (buttons stay quiet while empty).
LINKS = {"website": "", "download": "", "discord": ""}

UPDATES = [
    "Initial release - v1.0.0",
    "Roblox Lua script injection support",
    "Dark-themed GUI with script editor",
    "Tab management for multiple scripts",
    "Kill Roblox functionality",
]
CREDITS = [("Devin", "Integration"), ("User", "GUI Design")]

BG      = "#0d0d0e"
CARD    = "#151516"
BORDER  = "#242426"
HAIR    = "#232326"
TEXT    = "#ececec"
MUTED   = "#8b8b8b"
GOLD    = "#e8c15a"   # ring colour - tweak to taste

_QSS = """
QWidget { color: @TEXT@; font-size: 13px; background: transparent; }
QLabel#Muted { color: @MUTED@; }
QLabel#Empty { color: #7a7a7a; }
QLabel#Brand { font-size: 18px; font-weight: 700; color: #ffffff; }
QLabel#CardTitle { font-size: 15px; font-weight: 700; }
QLabel#CardHead { font-size: 16px; font-weight: 700; }
QLabel#RowTitle { font-size: 13px; font-weight: 700; }
QLabel#SectionHeader { font-size: 11px; font-weight: 700; color: @MUTED@; letter-spacing: 1px; }
QLabel#Count { color: #cfcfcf; font-weight: 600; }
QLabel#Ver { color: #5f5f63; font-size: 11px; }
QFrame#Card { background: @CARD@; border: 1px solid @BORDER@; border-radius: 10px; }
QFrame#Hair { background: @HAIR@; min-height: 1px; max-height: 1px; border: none; }
QFrame#Sidebar { border-right: 1px solid #1f1f22; }
QPushButton {
    background: #1b1b1d; border: 1px solid #2c2c2f; border-radius: 7px;
    padding: 8px 14px; color: #e4e4e4; font-weight: 600;
}
QPushButton:hover { background: #232326; border-color: #3a3a3e; }
QPushButton:pressed { background: #171719; }
QPushButton:disabled { color: #6d6d6d; }
QPushButton#Nav {
    background: transparent; border: none; border-radius: 0;
    padding: 12px 16px; text-align: left; color: #a8a8ad; font-weight: 600;
}
QPushButton#Nav:hover { background: #161618; color: #e8e8e8; }
QPushButton#Nav:checked { background: #1c1c1f; color: #ffffff; }
QPushButton#Ghost { background: transparent; border: none; border-radius: 6px; padding: 4px; }
QPushButton#Ghost:hover { background: #202024; }
QPushButton#TitleBtn { background: transparent; border: none; border-radius: 6px; padding: 0; }
QPushButton#TitleBtn:hover { background: #202024; }
QPushButton#CloseBtn:hover { background: #b3261e; }
QPushButton#Tab {
    background: #141416; border: 1px solid #2a2a2d; border-radius: 9px;
    padding: 10px 34px 10px 22px; min-width: 150px; text-align: left; color: #c9c9ce;
}
QPushButton#Tab:checked {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #232326, stop:1 #18181a);
    border: 1px solid #4b4b50; color: #ffffff;
}
QPushButton#TabClose { background: transparent; border: none; border-radius: 6px; padding: 0; }
QPushButton#TabClose:hover { background: rgba(255,255,255,0.14); }
QPushButton#IconSq { min-width: 38px; max-width: 38px; min-height: 38px; max-height: 38px; padding: 0; }
QLineEdit {
    background: #141416; border: 1px solid #2a2a2d; border-radius: 8px;
    padding: 9px 12px; selection-background-color: #3a3a40;
}
QLineEdit:focus { border-color: #4b4b50; }
QPlainTextEdit#Code { background: transparent; border: none; padding: 6px 8px;
                      selection-background-color: #333338; }
QCheckBox { spacing: 10px; color: #d6d6d6; }
QCheckBox::indicator { width: 16px; height: 16px; border-radius: 4px;
                       border: 1px solid #3a3a3e; background: #141416; }
QCheckBox::indicator:hover { border-color: #4b4b50; }
QCheckBox::indicator:checked { background: #e6e6e6; border-color: #e6e6e6; }
QScrollArea { border: none; }
QScrollBar:vertical { background: transparent; width: 8px; margin: 2px; }
QScrollBar::handle:vertical { background: #2e2e32; border-radius: 4px; min-height: 28px; }
QScrollBar::handle:vertical:hover { background: #3a3a3f; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: transparent; height: 8px; }
QScrollBar::handle:horizontal { background: #2e2e32; border-radius: 4px; min-width: 28px; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QSpinBox { background: #141416; border: 1px solid #2a2a2d; border-radius: 7px;
           padding: 6px 8px; }
QSpinBox::up-button, QSpinBox::down-button { width: 0; border: none; }
QToolTip { background: #1c1c1f; color: #eee; border: 1px solid #333336; padding: 6px 8px; }
QDialog, QMessageBox { background: #141416; }
QStackedWidget { background: transparent; }
"""
QSS = (_QSS.replace("@TEXT@", TEXT).replace("@MUTED@", MUTED)
           .replace("@CARD@", CARD).replace("@BORDER@", BORDER)
           .replace("@HAIR@", HAIR))

# ------------------------------------------------------------------- icons
_ICON_CACHE = {}

def _pt(r, fx, fy):
    return QPointF(r.x() + r.width() * fx, r.y() + r.height() * fy)

def _poly(p, r, pts):
    p.drawPolyline([_pt(r, x, y) for x, y in pts])

def _i_dashboard(p, r):
    g = 0.14; s = (1 - g) / 2
    for x, y in [(0, 0), (s + g, 0), (0, s + g), (s + g, s + g)]:
        p.drawRoundedRect(QRectF(r.x() + r.width() * x, r.y() + r.height() * y,
                                 r.width() * s, r.height() * s), 2, 2)

def _i_code(p, r):
    _poly(p, r, [(0.35, 0.22), (0.10, 0.50), (0.35, 0.78)])
    _poly(p, r, [(0.65, 0.22), (0.90, 0.50), (0.65, 0.78)])

def _i_book(p, r):
    p.drawRoundedRect(r, 3, 3)
    p.drawLine(_pt(r, 0.32, 0.12), _pt(r, 0.32, 0.88))

def _i_users(p, r):
    p.drawEllipse(QRectF(r.x() + r.width() * 0.14, r.y() + r.height() * 0.16,
                         r.width() * 0.34, r.height() * 0.34))
    p.drawArc(QRectF(r.x() + r.width() * 0.06, r.y() + r.height() * 0.56,
                     r.width() * 0.50, r.height() * 0.44), 0, 180 * 16)
    p.drawEllipse(QRectF(r.x() + r.width() * 0.60, r.y() + r.height() * 0.22,
                         r.width() * 0.26, r.height() * 0.26))
    p.drawArc(QRectF(r.x() + r.width() * 0.56, r.y() + r.height() * 0.60,
                     r.width() * 0.40, r.height() * 0.40), 0, 180 * 16)

def _i_gear(p, r):
    p.drawEllipse(QRectF(r.x() + r.width() * 0.30, r.y() + r.height() * 0.30,
                         r.width() * 0.40, r.height() * 0.40))
    c = _pt(r, 0.5, 0.5)
    for a in range(0, 360, 45):
        t = math.radians(a)
        p1 = QPointF(c.x() + math.cos(t) * r.width() * 0.20, c.y() - math.sin(t) * r.height() * 0.20)
        p2 = QPointF(c.x() + math.cos(t) * r.width() * 0.42, c.y() - math.sin(t) * r.height() * 0.42)
        p.drawLine(p1, p2)

def _i_monitor(p, r):
    p.drawRoundedRect(QRectF(r.x() + r.width() * 0.06, r.y() + r.height() * 0.14,
                             r.width() * 0.88, r.height() * 0.56), 3, 3)
    p.drawLine(_pt(r, 0.5, 0.70), _pt(r, 0.5, 0.86))
    p.drawLine(_pt(r, 0.30, 0.88), _pt(r, 0.70, 0.88))

def _i_box(p, r):
    _poly(p, r, [(0.5, 0.06), (0.9, 0.28), (0.5, 0.50), (0.1, 0.28), (0.5, 0.06)])
    _poly(p, r, [(0.1, 0.28), (0.1, 0.70), (0.5, 0.92), (0.9, 0.70), (0.9, 0.28)])
    p.drawLine(_pt(r, 0.5, 0.50), _pt(r, 0.5, 0.92))

def _i_trend(p, r):
    _poly(p, r, [(0.06, 0.78), (0.36, 0.46), (0.54, 0.62), (0.92, 0.24)])
    _poly(p, r, [(0.70, 0.24), (0.92, 0.24), (0.92, 0.46)])

def _i_award(p, r):
    p.drawEllipse(QRectF(r.x() + r.width() * 0.30, r.y() + r.height() * 0.10,
                         r.width() * 0.40, r.height() * 0.40))
    _poly(p, r, [(0.38, 0.48), (0.34, 0.90), (0.50, 0.76), (0.66, 0.90), (0.62, 0.48)])

def _i_crown(p, r):
    _poly(p, r, [(0.10, 0.78), (0.10, 0.34), (0.32, 0.52), (0.50, 0.26),
                 (0.68, 0.52), (0.90, 0.34), (0.90, 0.78), (0.10, 0.78)])

def _i_link(p, r):
    p.drawArc(QRectF(r.x() + r.width() * 0.06, r.y() + r.height() * 0.28,
                     r.width() * 0.44, r.height() * 0.44), 90 * 16, 180 * 16)
    p.drawArc(QRectF(r.x() + r.width() * 0.50, r.y() + r.height() * 0.28,
                     r.width() * 0.44, r.height() * 0.44), 270 * 16, 180 * 16)
    p.drawLine(_pt(r, 0.35, 0.50), _pt(r, 0.65, 0.50))

def _i_play(p, r):
    _poly(p, r, [(0.30, 0.18), (0.82, 0.50), (0.30, 0.82), (0.30, 0.18)])

def _i_trash(p, r):
    p.drawLine(_pt(r, 0.18, 0.26), _pt(r, 0.82, 0.26))
    _poly(p, r, [(0.40, 0.26), (0.40, 0.14), (0.60, 0.14), (0.60, 0.26)])
    _poly(p, r, [(0.26, 0.26), (0.30, 0.88), (0.70, 0.88), (0.74, 0.26)])
    p.drawLine(_pt(r, 0.43, 0.40), _pt(r, 0.43, 0.72))
    p.drawLine(_pt(r, 0.57, 0.40), _pt(r, 0.57, 0.72))

def _i_power(p, r):
    p.drawArc(QRectF(r.x() + r.width() * 0.16, r.y() + r.height() * 0.22,
                     r.width() * 0.68, r.height() * 0.68), 120 * 16, 300 * 16)
    p.drawLine(_pt(r, 0.5, 0.08), _pt(r, 0.5, 0.42))

def _i_save(p, r):
    p.drawRoundedRect(QRectF(r.x() + r.width() * 0.14, r.y() + r.height() * 0.14,
                             r.width() * 0.72, r.height() * 0.72), 3, 3)
    _poly(p, r, [(0.32, 0.14), (0.32, 0.42), (0.68, 0.42), (0.68, 0.14)])
    p.drawRect(QRectF(r.x() + r.width() * 0.32, r.y() + r.height() * 0.60,
                      r.width() * 0.36, r.height() * 0.26))

def _i_folder(p, r):
    _poly(p, r, [(0.08, 0.78), (0.08, 0.26), (0.34, 0.26), (0.44, 0.38),
                 (0.92, 0.38), (0.92, 0.78), (0.08, 0.78)])

def _i_plus(p, r):
    p.drawLine(_pt(r, 0.5, 0.2), _pt(r, 0.5, 0.8))
    p.drawLine(_pt(r, 0.2, 0.5), _pt(r, 0.8, 0.5))

def _i_chev_l(p, r):
    _poly(p, r, [(0.62, 0.18), (0.34, 0.50), (0.62, 0.82)])

def _i_chev_r(p, r):
    _poly(p, r, [(0.38, 0.18), (0.66, 0.50), (0.38, 0.82)])

def _i_min(p, r):
    p.drawLine(_pt(r, 0.22, 0.5), _pt(r, 0.78, 0.5))

def _i_expand(p, r):
    p.drawLine(_pt(r, 0.58, 0.42), _pt(r, 0.86, 0.14))
    _poly(p, r, [(0.64, 0.14), (0.86, 0.14), (0.86, 0.36)])
    p.drawLine(_pt(r, 0.42, 0.58), _pt(r, 0.14, 0.86))
    _poly(p, r, [(0.14, 0.64), (0.14, 0.86), (0.36, 0.86)])

def _i_restore(p, r):
    p.drawRect(QRectF(r.x() + r.width() * 0.14, r.y() + r.height() * 0.30,
                      r.width() * 0.56, r.height() * 0.56))
    _poly(p, r, [(0.34, 0.30), (0.34, 0.14), (0.86, 0.14), (0.86, 0.66), (0.70, 0.66)])

def _i_close(p, r):
    p.drawLine(_pt(r, 0.24, 0.24), _pt(r, 0.76, 0.76))
    p.drawLine(_pt(r, 0.76, 0.24), _pt(r, 0.24, 0.76))

def _i_search(p, r):
    p.drawEllipse(QRectF(r.x() + r.width() * 0.14, r.y() + r.height() * 0.14,
                         r.width() * 0.48, r.height() * 0.48))
    p.drawLine(_pt(r, 0.52, 0.52), _pt(r, 0.86, 0.86))

def _i_refresh(p, r):
    p.drawArc(QRectF(r.x() + r.width() * 0.14, r.y() + r.height() * 0.14,
                     r.width() * 0.72, r.height() * 0.72), 40 * 16, 280 * 16)
    _poly(p, r, [(0.90, 0.14), (0.90, 0.40), (0.64, 0.40)])

def _i_copy(p, r):
    p.drawRoundedRect(QRectF(r.x() + r.width() * 0.32, r.y() + r.height() * 0.12,
                             r.width() * 0.54, r.height() * 0.58), 2, 2)
    _poly(p, r, [(0.32, 0.88), (0.14, 0.88), (0.14, 0.34)])

def _i_planet(p, r):
    # planet body keeps the requested icon colour (white in the UI)
    p.setBrush(p.pen().color())
    p.drawEllipse(QRectF(r.x() + r.width() * 0.26, r.y() + r.height() * 0.26,
                         r.width() * 0.48, r.height() * 0.48))
    p.setBrush(Qt.BrushStyle.NoBrush)
    # ring stroked in gold
    ring = QPen(QColor(GOLD))
    ring.setWidthF(p.pen().widthF())
    ring.setCapStyle(Qt.PenCapStyle.RoundCap)
    ring.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    p.setPen(ring)
    p.save()
    c = _pt(r, 0.5, 0.5)
    p.translate(c); p.rotate(-18); p.translate(-c)
    p.drawEllipse(QRectF(r.x() - r.width() * 0.02, r.y() + r.height() * 0.38,
                         r.width() * 1.04, r.height() * 0.24))
    p.restore()

ICONS = {
    "dashboard": _i_dashboard, "code": _i_code, "book": _i_book, "users": _i_users,
    "gear": _i_gear, "monitor": _i_monitor, "box": _i_box, "trend": _i_trend,
    "award": _i_award, "crown": _i_crown, "link": _i_link, "play": _i_play,
    "trash": _i_trash, "power": _i_power, "save": _i_save, "folder": _i_folder,
    "plus": _i_plus, "chev_l": _i_chev_l, "chev_r": _i_chev_r, "min": _i_min,
    "expand": _i_expand, "restore": _i_restore, "close": _i_close,
    "search": _i_search, "refresh": _i_refresh, "copy": _i_copy, "planet": _i_planet,
}

def icon(name, size=16, color="#c9c9ce", weight=1.6):
    key = (name, size, color, weight)
    if key in _ICON_CACHE:
        return _ICON_CACHE[key]
    dpr = 2
    pm = QPixmap(size * dpr, size * dpr)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(QColor(color))
    pen.setWidthF(weight * dpr)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)
    m = weight * dpr + 1
    ICONS[name](p, QRectF(m, m, pm.width() - 2 * m, pm.height() - 2 * m))
    p.end()
    pm.setDevicePixelRatio(dpr)
    _ICON_CACHE[key] = pm
    return pm

def brand_pixmap(size=32):
    """App logo: logo.png next to the script, else the drawn planet mark."""
    try:
        p = Path(__file__).resolve().parent / "logo.png"
        if p.exists():
            pm = QPixmap(str(p))
            if not pm.isNull():
                return pm.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio,
                                 Qt.TransformationMode.SmoothTransformation)
    except Exception:
        pass
    return icon("planet", size, "#f2f2f2", 1.8)

def icon_btn(name, text="", size=16, tip=""):
    b = QPushButton(text)
    b.setIcon(QIcon(icon(name, size)))
    b.setIconSize(QSize(size, size))
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    if tip:
        b.setToolTip(tip)
    return b

def hair():
    f = QFrame()
    f.setObjectName("Hair")
    return f

def centered_label(pixmap):
    l = QLabel()
    l.setPixmap(pixmap)
    l.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return l

# ------------------------------------------------------------------ storage
class Store:
    DEFAULTS = {
        "editor_word_wrap": False,
        "editor_line_numbers": True,
        "always_on_top": False,
        "lock_window_size": False,
        "window_size_autosave": True,
        "window_size": None,
        "sidebar_width": 250,
        "sidebar_collapsed": False,
    }

    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        saved = {}
        try:
            saved = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
        self.settings = {**self.DEFAULTS, **saved}

    def save(self):
        SETTINGS_FILE.write_text(json.dumps(self.settings, indent=2), encoding="utf-8")

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()

# -------------------------------------------------------------- roblox procs
def find_roblox_pids():
    """List running Roblox client processes (pid, name). Detection only."""
    names = ("RobloxWindows.exe", "RobloxPlayerBeta.exe")
    out = []
    try:
        if os.name == "nt":
            res = subprocess.run(["tasklist", "/FO", "CSV", "/NH"],
                                 capture_output=True, text=True, timeout=5)
            for line in res.stdout.splitlines():
                parts = line.split('","')
                if len(parts) >= 2 and parts[0].strip('"') in names:
                    out.append((parts[1].strip('"'), parts[0].strip('"')))
        else:
            res = subprocess.run(["pgrep", "-x", "RobloxPlayerBeta"],
                                 capture_output=True, text=True, timeout=5)
            out += [(pid, "RobloxPlayerBeta") for pid in res.stdout.split()]
    except Exception:
        pass
    return out

def kill_roblox(parent):
    pids = find_roblox_pids()
    if not pids:
        QMessageBox.information(parent, APP_NAME, "No running Roblox process found.")
        return
    r = QMessageBox.question(parent, APP_NAME,
                             f"Terminate {len(pids)} Roblox process(es)?",
                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    if r != QMessageBox.StandardButton.Yes:
        return
    for pid, _ in pids:
        try:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", pid, "/F"], capture_output=True)
            else:
                subprocess.run(["kill", "-9", pid], capture_output=True)
        except Exception:
            pass

# --------------------------------------------------------------- title bar
class TitleBar(QWidget):
    def __init__(self, win):
        super().__init__(win)
        self.win = win
        self.setFixedHeight(38)
        h = QHBoxLayout(self)
        h.setContentsMargins(10, 2, 6, 2)
        h.setSpacing(2)
        h.addStretch(1)
        self.min_b = QPushButton()
        self.min_b.setObjectName("TitleBtn")
        self.min_b.setFixedSize(42, 30)
        self.min_b.setIcon(QIcon(icon("min", 12)))
        self.min_b.clicked.connect(win.showMinimized)
        self.max_b = QPushButton()
        self.max_b.setObjectName("TitleBtn")
        self.max_b.setFixedSize(42, 30)
        self.max_b.setIcon(QIcon(icon("expand", 12)))
        self.max_b.clicked.connect(win.toggle_max)
        self.close_b = QPushButton()
        self.close_b.setObjectName("CloseBtn")
        self.close_b.setStyleSheet("QPushButton{background:transparent;border:none;border-radius:6px;}"
                                   "QPushButton:hover{background:#b3261e;}")
        self.close_b.setFixedSize(42, 30)
        self.close_b.setIcon(QIcon(icon("close", 12)))
        self.close_b.clicked.connect(win.close)
        for b in (self.min_b, self.max_b, self.close_b):
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            h.addWidget(b)
        self._drag = None

    def sync_max_icon(self):
        self.max_b.setIcon(QIcon(icon("restore" if self.win.isMaximized() else "expand", 12)))

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag = e.globalPosition().toPoint() - self.win.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self._drag and not self.win.isMaximized():
            self.win.move(e.globalPosition().toPoint() - self._drag)

    def mouseReleaseEvent(self, e):
        self._drag = None

    def mouseDoubleClickEvent(self, e):
        self.win.toggle_max()

# ------------------------------------------------------------------- widgets
class NavButton(QPushButton):
    def __init__(self, icon_name, title):
        super().__init__()
        self.setObjectName("Nav")
        self.icon_name = icon_name
        self.title = title
        self.setCheckable(True)
        self.setFixedHeight(46)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setIconSize(QSize(17, 17))
        self.setText(title)
        self.toggled.connect(self._sync)
        self._sync(False)

    def _sync(self, on):
        self.setIcon(QIcon(icon(self.icon_name, 17, "#ffffff" if on else "#a8a8ad")))

    def set_collapsed(self, on):
        self.setText("" if on else self.title)

    def paintEvent(self, e):
        super().paintEvent(e)
        if self.isChecked():
            p = QPainter(self)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor("#f2f2f2"))
            p.drawRect(0, 0, 3, self.height())
            p.end()

class TabButton(QPushButton):
    middle_closed = pyqtSignal()
    close_clicked = pyqtSignal()

    def __init__(self, name=""):
        super().__init__(name)
        self.close_b = QPushButton(self)
        self.close_b.setObjectName("TabClose")
        self.close_b.setIcon(QIcon(icon("close", 10, "#8b8b8b")))
        self.close_b.setIconSize(QSize(10, 10))
        self.close_b.setFixedSize(22, 22)
        self.close_b.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_b.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.close_b.setToolTip("Close tab")
        self.close_b.clicked.connect(lambda: self.close_clicked.emit())

    def resizeEvent(self, e):
        super().resizeEvent(e)
        m = 6
        self.close_b.move(self.width() - self.close_b.width() - m,
                          (self.height() - self.close_b.height()) // 2)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.MiddleButton:
            self.middle_closed.emit()
        else:
            super().mousePressEvent(e)

class ToggleSwitch(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, checked=False):
        super().__init__()
        self._on = checked
        self.setFixedSize(46, 24)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def isChecked(self):
        return self._on

    def setChecked(self, on):
        if on != self._on:
            self._on = on
            self.update()
            self.toggled.emit(on)

    def mousePressEvent(self, e):
        self.setChecked(not self._on)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#e6e6e6") if self._on else QColor("#2a2a2d"))
        p.drawRoundedRect(0, 0, 46, 24, 12, 12)
        p.setBrush(QColor("#111113") if self._on else QColor("#8a8a8f"))
        x = 26 if self._on else 4
        p.drawEllipse(x, 4, 16, 16)
        p.end()

# -------------------------------------------------------------- code editor
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, doc):
        super().__init__(doc)
        self.rules = []
        kw = QTextCharFormat(); kw.setForeground(QColor("#c792ea")); kw.setFontWeight(QFont.Weight.Bold)
        for w in ("and as assert break class continue def del elif else except finally for "
                  "from global if import in is lambda nonlocal not or pass raise return try "
                  "while with yield True False None async await").split():
            self.rules.append((QRegularExpression(r"\b" + w + r"\b"), kw))
        st = QTextCharFormat(); st.setForeground(QColor("#9ece6a"))
        self.rules.append((QRegularExpression(r'"[^"]*"|\'[^\']*\''), st))
        cm = QTextCharFormat(); cm.setForeground(QColor("#565660")); cm.setFontItalic(True)
        self.rules.append((QRegularExpression(r"#[^\n]*|--[^\n]*"), cm))
        nu = QTextCharFormat(); nu.setForeground(QColor("#ff9e64"))
        self.rules.append((QRegularExpression(r"\b\d+(\.\d+)?\b"), nu))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                m = it.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), fmt)

class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setObjectName("Code")
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.update_line_number_area_width(0)
        font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        font.setPointSize(11)
        self.setFont(font)
        self.highlighter = PythonHighlighter(self.document())
        self.setTabStopDistance(QFontMetricsF(font).horizontalAdvance(" ") * 4)

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        return 14 + self.fontMetrics().horizontalAdvance("9") * digits

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(cr.left(), cr.top(),
                                          self.line_number_area_width(), cr.height())

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.setPen(QColor("#6a6a70"))
        block = self.firstVisibleBlock()
        block_num = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.drawText(0, int(top), self.line_number_area.width() - 8,
                                 self.fontMetrics().height(), Qt.AlignmentFlag.AlignRight,
                                 str(block_num + 1))
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_num += 1

    def set_line_numbers_visible(self, on):
        self.line_number_area.setVisible(on)
        if on:
            self.update_line_number_area_width(0)
        else:
            self.setViewportMargins(0, 0, 0, 0)

class RunWorker(QThread):
    done = pyqtSignal(str, bool)

    def __init__(self, code, target_pid=None):
        super().__init__()
        self.code = code
        self.target_pid = target_pid

    def run(self):
        try:
            injector = RobloxInjector()
            if self.target_pid:
                injector.set_target_pid(int(self.target_pid))
            success, msg = injector.inject_script_content(self.code)
            if success:
                self.done.emit(msg, True)
            else:
                self.done.emit("Injection failed: {}".format(msg), False)
        except Exception as e:  # noqa: BLE001
            self.done.emit("Error: {}".format(e), False)

# ------------------------------------------------------------------- pages
class DashboardPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QWidget()
        v = QVBoxLayout(inner)
        v.setContentsMargins(26, 22, 26, 26)
        v.setSpacing(22)

        card = QFrame(); card.setObjectName("Card")
        h = QHBoxLayout(card)
        h.setContentsMargins(24, 22, 24, 22)
        h.setSpacing(10)
        quick = [("monitor", "Visit Our Website", "Open Website", "website"),
                 ("box", f"Version: {VERSION}", "Download Latest", "download"),
                 ("users", "Join Our Community", "Join Discord", "discord")]
        for ic, title, btxt, key in quick:
            col = QVBoxLayout()
            col.setSpacing(12)
            col.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col.addWidget(centered_label(icon(ic, 22, "#f2f2f2", 1.8)))
            t = QLabel(title); t.setObjectName("CardTitle")
            t.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col.addWidget(t)
            b = icon_btn("link", " " + btxt, 13)
            b.clicked.connect(lambda _=False, k=key: main.open_link(k))
            col.addWidget(b, 0, Qt.AlignmentFlag.AlignHCenter)
            h.addLayout(col, 1)
        v.addWidget(card)

        ucard = QFrame(); ucard.setObjectName("Card")
        uv = QVBoxLayout(ucard)
        uv.setContentsMargins(24, 22, 24, 16)
        uv.setSpacing(6)
        uv.addWidget(centered_label(icon("trend", 20, "#f2f2f2", 1.8)))
        t = QLabel("Latest Updates"); t.setObjectName("CardHead")
        t.setAlignment(Qt.AlignmentFlag.AlignCenter)
        uv.addWidget(t)
        s = QLabel("Stay updated with the latest features and improvements")
        s.setObjectName("Muted"); s.setAlignment(Qt.AlignmentFlag.AlignCenter)
        uv.addWidget(s)
        uv.addSpacing(12)
        uscroll = QScrollArea(); uscroll.setWidgetResizable(True)
        uscroll.setFixedHeight(300)
        uinner = QWidget()
        ul = QVBoxLayout(uinner)
        ul.setContentsMargins(4, 4, 4, 4)
        ul.setSpacing(0)
        for i, line in enumerate(UPDATES):
            lab = QLabel(line)
            lab.setWordWrap(True)
            lab.setContentsMargins(4, 10, 4, 10)
            ul.addWidget(lab)
            if i < len(UPDATES) - 1:
                ul.addWidget(hair())
        ul.addStretch(1)
        uscroll.setWidget(uinner)
        uv.addWidget(uscroll)
        v.addWidget(ucard)

        ccard = QFrame(); ccard.setObjectName("Card")
        cv = QVBoxLayout(ccard)
        cv.setContentsMargins(24, 22, 24, 18)
        cv.setSpacing(6)
        cv.addWidget(centered_label(icon("award", 20, "#f2f2f2", 1.8)))
        t = QLabel("Credits"); t.setObjectName("CardHead")
        t.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cv.addWidget(t)
        s = QLabel("Thanks to our contributors")
        s.setObjectName("Muted"); s.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cv.addWidget(s)
        cv.addSpacing(12)
        for name, role in CREDITS:
            row = QHBoxLayout()
            row.setSpacing(10)
            row.addWidget(centered_label(icon("crown", 15, "#e8e8e8")))
            n = QLabel(name); n.setObjectName("RowTitle")
            row.addWidget(n)
            r = QLabel(f"- {role}"); r.setObjectName("Muted")
            row.addWidget(r)
            row.addStretch(1)
            b = icon_btn("link", " Visit", 13)
            b.clicked.connect(lambda _=False: main.open_link("website"))
            row.addWidget(b)
            cv.addLayout(row)
        v.addWidget(ccard)
        v.addStretch(1)
        scroll.setWidget(inner)
        outer.addWidget(scroll)

    def refresh(self):
        pass

class ExecutorPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.worker = None
        self.scripts = {"Script 1": ""}
        self.current = "Script 1"
        self.target_pid = None  # Will be set from Client Manager
        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 20, 24, 24)
        lay.setSpacing(12)

        self.tab_bar = QHBoxLayout()
        self.tab_bar.setSpacing(8)
        self.tab_group = QButtonGroup(self)
        self.tab_group.setExclusive(True)
        lay.addLayout(self.tab_bar)
        self._rebuild_tabs()

        tb = QHBoxLayout()
        tb.setSpacing(10)
        self.exec_b = icon_btn("play", " Execute", 14)
        self.exec_b.clicked.connect(self.run_code)
        self.clear_b = icon_btn("trash", " Clear", 14)
        self.clear_b.clicked.connect(lambda: self.editor.clear())
        self.kill_b = icon_btn("power", " Kill Roblox", 14)
        self.kill_b.clicked.connect(lambda: kill_roblox(self.main))
        self.save_b = icon_btn("save", " Save", 14)
        self.save_b.clicked.connect(self.save_script)
        self.open_b = icon_btn("folder", " Open", 14)
        self.open_b.clicked.connect(self.open_script)
        for b in (self.exec_b, self.clear_b, self.kill_b, self.save_b, self.open_b):
            tb.addWidget(b)
        tb.addStretch(1)
        lay.addLayout(tb)
        lay.addWidget(hair())

        self.editor = CodeEditor()
        self.editor.setPlaceholderText("-- Write your Lua script here...")
        lay.addWidget(self.editor, 1)

    def _rebuild_tabs(self):
        while self.tab_bar.count():
            item = self.tab_bar.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for name in self.scripts:
            b = TabButton(name)
            b.setObjectName("Tab")
            b.setCheckable(True)
            b.setChecked(name == self.current)
            b.clicked.connect(lambda _=False, n=name: self._switch(n))
            b.middle_closed.connect(lambda n=name: self._close_tab(n))
            b.close_clicked.connect(lambda n=name: self._close_tab(n))
            self.tab_group.addButton(b)
            self.tab_bar.addWidget(b)
        add = QPushButton()
        add.setObjectName("IconSq")
        add.setIcon(QIcon(icon("plus", 14)))
        add.setCursor(Qt.CursorShape.PointingHandCursor)
        add.clicked.connect(self._add_tab)
        self.tab_bar.addWidget(add)
        self.tab_bar.addStretch(1)

    def _switch(self, name):
        if name == self.current:
            return
        self.scripts[self.current] = self.editor.toPlainText()
        self.current = name
        self.editor.setPlainText(self.scripts[name])

    def _add_tab(self):
        n = len(self.scripts) + 1
        while f"Script {n}" in self.scripts:
            n += 1
        self.scripts[self.current] = self.editor.toPlainText()
        self.scripts[f"Script {n}"] = ""
        self.current = f"Script {n}"
        self.editor.setPlainText("")
        self._rebuild_tabs()

    def _close_tab(self, name):
        if len(self.scripts) <= 1 or name not in self.scripts:
            return
        del self.scripts[name]
        if self.current == name:
            self.current = next(iter(self.scripts))
            self.editor.setPlainText(self.scripts[self.current])
        self._rebuild_tabs()

    def run_code(self):
        code = self.editor.toPlainText()
        if not code.strip():
            return
        
        # Get PID from Client Manager if available
        if self.main.clients and self.main.clients.clients:
            self.target_pid = self.main.clients.clients[0][0]  # Use first attached client
        
        self.exec_b.setEnabled(False)
        self.exec_b.setText(" Injecting...")
        self.worker = RunWorker(code, self.target_pid)
        self.worker.done.connect(self.on_done)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.start()

    def on_done(self, text, success):
        self.exec_b.setEnabled(True)
        self.exec_b.setText(" Execute")
        if success:
            print("--- Injection Successful ---\n" + text)
        else:
            print("--- Injection Failed ---\n" + text)

    def save_script(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save script", "", "Scripts (*.lua *.txt);;All files (*)")
        if path:
            Path(path).write_text(self.editor.toPlainText(), encoding="utf-8")

    def open_script(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open script", "", "Scripts (*.lua *.txt);;All files (*)")
        if path:
            self.editor.setPlainText(Path(path).read_text(encoding="utf-8", errors="replace"))

    def refresh(self):
        s = self.main.store.settings
        self.editor.setLineWrapMode(
            QPlainTextEdit.LineWrapMode.WidgetWidth if s.get("editor_word_wrap")
            else QPlainTextEdit.LineWrapMode.NoWrap)
        self.editor.set_line_numbers_visible(bool(s.get("editor_line_numbers", True)))

class ScriptBloxWorker(QThread):
    ok = pyqtSignal(list)
    failed = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            req = urllib.request.Request(self.url, headers={"User-Agent": "Zeno/1.3.60"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8", "replace"))
            scripts = (data.get("result") or {}).get("scripts") or []
            self.ok.emit(scripts)
        except Exception as e:  # noqa: BLE001
            self.failed.emit(str(e))


class ScriptViewDialog(QDialog):
    def __init__(self, parent, script, main):
        super().__init__(parent)
        self.script = script
        self.main = main
        self.setWindowTitle(script.get("title") or "Script")
        self.resize(680, 520)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(18, 16, 18, 16)
        lay.setSpacing(10)
        head = QLabel(script.get("title") or "Untitled")
        head.setObjectName("CardHead")
        head.setWordWrap(True)
        lay.addWidget(head)
        game = (script.get("game") or {}).get("name")
        if game:
            g = QLabel(game)
            g.setObjectName("Muted")
            lay.addWidget(g)
        self.code = QPlainTextEdit()
        self.code.setReadOnly(True)
        self.code.setPlainText(script.get("script") or "-- no source returned")
        font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        font.setPointSize(11)
        self.code.setFont(font)
        lay.addWidget(self.code, 1)
        row = QHBoxLayout()
        row.setSpacing(10)
        row.addStretch(1)
        cp = icon_btn("copy", " Copy", 13)
        cp.clicked.connect(self.copy_code)
        row.addWidget(cp)
        send = icon_btn("code", " Send to Editor", 13)
        send.clicked.connect(self.send_to_editor)
        row.addWidget(send)
        close = QPushButton("Close")
        close.clicked.connect(self.accept)
        row.addWidget(close)
        lay.addLayout(row)

    def copy_code(self):
        QApplication.clipboard().setText(self.code.toPlainText())
        self.sender().setText(" Copied!")

    def send_to_editor(self):
        ex = self.main.executor
        ex._add_tab()
        ex.scripts[ex.current] = self.script.get("script") or ""
        ex.editor.setPlainText(ex.scripts[ex.current])
        self.main.show_page(1)
        self.accept()


class ScripthubPage(QWidget):
    API = "https://scriptblox.com/api/script"

    def __init__(self, main):
        super().__init__()
        self.main = main
        self.worker = None
        lay = QVBoxLayout(self)
        lay.setContentsMargins(26, 22, 26, 26)
        lay.setSpacing(12)
        bar = QFrame(); bar.setObjectName("Card")
        h = QHBoxLayout(bar)
        h.setContentsMargins(14, 12, 14, 12)
        h.setSpacing(10)
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search scripts... (Enter to search)")
        self.search.setClearButtonEnabled(True)
        self.search.returnPressed.connect(self.do_search)
        h.addWidget(self.search, 1)
        go = icon_btn("search", " Search", 14)
        go.clicked.connect(self.do_search)
        h.addWidget(go)
        latest = icon_btn("refresh", " Latest", 14)
        latest.clicked.connect(self.do_latest)
        h.addWidget(latest)
        lay.addWidget(bar)

        attr = QLabel('Powered by <a href="https://scriptblox.com" style="color:#8b8b8b;">ScriptBlox</a>')
        attr.setObjectName("Muted")
        attr.setOpenExternalLinks(True)
        attr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(attr)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QWidget()
        self.list = QVBoxLayout(inner)
        self.list.setContentsMargins(2, 2, 2, 2)
        self.list.setSpacing(10)
        scroll.setWidget(inner)
        lay.addWidget(scroll, 1)
        self.show_status("Search for a game or script above,\nor hit Latest for fresh uploads.")

    def show_status(self, text):
        self.clear_list()
        lab = QLabel(text)
        lab.setObjectName("Empty")
        lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.list.addWidget(lab)
        self.list.addStretch(1)

    def clear_list(self):
        while self.list.count():
            item = self.list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def do_search(self):
        q = self.search.text().strip()
        if not q:
            self.do_latest()
            return
        self.fetch(f"{self.API}/search?q={urllib.parse.quote(q)}&max=20",
                   f'Searching for "{q}"...')

    def do_latest(self):
        self.fetch(f"{self.API}/fetch", "Loading latest scripts...")

    def fetch(self, url, loading_text):
        if self.worker is not None:
            return  # a request is already in flight
        self.show_status(loading_text)
        self.worker = ScriptBloxWorker(url)
        self.worker.ok.connect(self.show_results)
        self.worker.failed.connect(self.show_error)
        self.worker.finished.connect(self._worker_done)
        self.worker.start()

    def _worker_done(self):
        w = self.sender()
        if self.worker is w:
            self.worker = None
        w.deleteLater()

    def show_error(self, msg):
        self.show_status(f"Couldn't reach ScriptBlox.\n{msg}")

    def show_results(self, scripts):
        self.clear_list()
        if not scripts:
            self.show_status("No scripts found.")
            return
        for s in scripts:
            self.list.addWidget(self.make_row(s))
        self.list.addStretch(1)

    def make_row(self, s):
        f = QFrame()
        f.setObjectName("Card")
        h = QHBoxLayout(f)
        h.setContentsMargins(16, 12, 16, 12)
        h.setSpacing(12)
        v = QVBoxLayout()
        v.setSpacing(3)
        title = QLabel(s.get("title") or "Untitled")
        title.setObjectName("RowTitle")
        title.setWordWrap(True)
        v.addWidget(title)
        game = (s.get("game") or {}).get("name")
        if not game:
            game = "Universal" if s.get("isUniversal") else "--"
        g = QLabel(game)
        g.setObjectName("Muted")
        v.addWidget(g)
        meta = []
        if s.get("verified"):
            meta.append("Verified")
        meta.append("Keyless" if not s.get("key") else "Key required")
        if s.get("isPatched"):
            meta.append("Patched")
        views = s.get("views")
        if isinstance(views, int):
            meta.append(f"{views:,} views")
        m = QLabel("   \u2022   ".join(meta))
        m.setObjectName("Muted")
        v.addWidget(m)
        h.addLayout(v, 1)
        b = icon_btn("code", " View", 13)
        b.clicked.connect(lambda _=False, d=s: self.view_script(d))
        h.addWidget(b, 0, Qt.AlignmentFlag.AlignVCenter)
        return f

    def view_script(self, s):
        ScriptViewDialog(self, s, self.main).exec()

    def refresh(self):
        pass

class ClientManagerPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.clients = []
        lay = QVBoxLayout(self)
        lay.setContentsMargins(26, 22, 26, 26)
        lay.setSpacing(16)
        bar = QFrame(); bar.setObjectName("Card")
        h = QHBoxLayout(bar)
        h.setContentsMargins(14, 12, 14, 12)
        h.setSpacing(10)
        sel = QPushButton("Select All"); sel.clicked.connect(lambda: self._set_all(True))
        des = QPushButton("Deselect All"); des.clicked.connect(lambda: self._set_all(False))
        h.addWidget(sel); h.addWidget(des)
        h.addStretch(1)
        att = icon_btn("link", " Attach", 14)
        att.clicked.connect(self.attach)
        h.addWidget(att)
        h.addWidget(centered_label(icon("users", 14, "#cfcfcf")))
        self.count = QLabel("0 of 0 selected")
        self.count.setObjectName("Count")
        h.addWidget(self.count)
        lay.addWidget(bar)

        self.list_wrap = QVBoxLayout()
        self.list_wrap.setSpacing(10)
        lay.addLayout(self.list_wrap)
        self.empty = QLabel("No clients found. (Press Attach with Roblox Open)")
        self.empty.setObjectName("Empty")
        self.empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.empty, 1)

    def attach(self):
        for pid, name in find_roblox_pids():
            if pid not in [c[0] for c in self.clients]:
                self.clients.append((pid, name))
        self._rebuild()

    def _rebuild(self):
        while self.list_wrap.count():
            item = self.list_wrap.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for pid, name in self.clients:
            row = QFrame(); row.setObjectName("Card")
            h = QHBoxLayout(row)
            h.setContentsMargins(16, 12, 16, 12)
            cb = QCheckBox()
            cb.toggled.connect(self._update_count)
            h.addWidget(cb)
            t = QLabel(name); t.setObjectName("RowTitle")
            h.addWidget(t)
            m = QLabel(f"PID {pid}"); m.setObjectName("Muted")
            h.addWidget(m)
            h.addStretch(1)
            st = QLabel("Detached"); st.setObjectName("Muted")
            h.addWidget(st)
            self.list_wrap.addWidget(row)
        self.empty.setVisible(not self.clients)
        self._update_count()

    def _set_all(self, on):
        for i in range(self.list_wrap.count()):
            w = self.list_wrap.itemAt(i).widget()
            if w:
                cb = w.findChild(QCheckBox)
                if cb:
                    cb.setChecked(on)

    def _update_count(self, _=None):
        boxes = [self.list_wrap.itemAt(i).widget().findChild(QCheckBox)
                 for i in range(self.list_wrap.count())
                 if self.list_wrap.itemAt(i).widget()]
        boxes = [b for b in boxes if b]
        self.count.setText(f"{sum(b.isChecked() for b in boxes)} of {len(boxes)} selected")

    def refresh(self):
        pass

class SettingsPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.store = main.store
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        inner = QWidget()
        v = QVBoxLayout(inner)
        v.setContentsMargins(26, 22, 26, 26)
        v.setSpacing(10)
        v.setAlignment(Qt.AlignmentFlag.AlignTop)

        v.addWidget(self._header("EDITOR"))
        self.wrap_t = ToggleSwitch(bool(self.store.get("editor_word_wrap")))
        self.wrap_t.toggled.connect(lambda on: (self.store.set("editor_word_wrap", on), main.refresh_all()))
        v.addWidget(self._row("Word Wrap", "Wrap long lines in the editor", self.wrap_t))
        self.ln_t = ToggleSwitch(bool(self.store.get("editor_line_numbers")))
        self.ln_t.toggled.connect(lambda on: (self.store.set("editor_line_numbers", on), main.refresh_all()))
        v.addWidget(self._row("Line Numbers", "Show line numbers in the editor", self.ln_t))

        v.addWidget(self._header("WINDOW"))
        self.lock_t = ToggleSwitch(bool(self.store.get("lock_window_size")))
        self.lock_t.toggled.connect(lambda on: (self.store.set("lock_window_size", on), main.apply_window_lock()))
        v.addWidget(self._row("Lock Window Size", "Disable resizing from window borders", self.lock_t))
        self.autosave_t = ToggleSwitch(bool(self.store.get("window_size_autosave")))
        self.autosave_t.toggled.connect(lambda on: self.store.set("window_size_autosave", on))
        v.addWidget(self._row("Auto-save Window Size", "Remember the window size between restarts", self.autosave_t))
        wh = QHBoxLayout(); wh.setSpacing(8)
        self.win_w = QSpinBox(); self.win_w.setRange(640, 3840); self.win_w.setSuffix(" px")
        self.win_h = QSpinBox(); self.win_h.setRange(400, 2160); self.win_h.setSuffix(" px")
        up = QPushButton("Update"); up.clicked.connect(
            lambda: main.apply_window_size(self.win_w.value(), self.win_h.value()))
        rst = QPushButton("Reset"); rst.clicked.connect(
            lambda: main.apply_window_size(1280, 800))
        for w in (self.win_w, QLabel("x"), self.win_h, up, rst):
            wh.addWidget(w)
        v.addWidget(self._row("Window Size", "Set an exact window size", wh))
        sh = QHBoxLayout(); sh.setSpacing(8)
        self.side_w = QSpinBox(); self.side_w.setRange(160, 420); self.side_w.setSuffix(" px")
        upw = QPushButton("Update"); upw.clicked.connect(
            lambda: main.apply_sidebar_width(self.side_w.value()))
        rstw = QPushButton("Reset"); rstw.clicked.connect(lambda: main.apply_sidebar_width(250))
        for w in (self.side_w, upw, rstw):
            sh.addWidget(w)
        v.addWidget(self._row("Sidebar Width", "Width of the navigation sidebar", sh))

        v.addWidget(self._header("APP"))
        self.top_t = ToggleSwitch(bool(self.store.get("always_on_top")))
        self.top_t.toggled.connect(lambda on: (self.store.set("always_on_top", on), main.apply_always_on_top()))
        v.addWidget(self._row("Always on Top", "Keep Zeno above other applications", self.top_t))
        res = QPushButton("Restart"); res.clicked.connect(main.restart_app)
        v.addWidget(self._row("Restart App", "Restart Zeno to apply changes", res))
        dh = QHBoxLayout(); dh.setSpacing(8)
        opend = QPushButton("Open data folder")
        opend.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(str(DATA_DIR))))
        resetd = QPushButton("Reset hub data")
        resetd.clicked.connect(main.reset_data)
        dh.addWidget(opend); dh.addWidget(resetd)
        v.addWidget(self._row("Data", f"Settings live in {DATA_DIR}", dh))
        v.addStretch(1)
        scroll.setWidget(inner)
        outer.addWidget(scroll)

    @staticmethod
    def _header(title):
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(2, 10, 2, 2)
        h.setSpacing(12)
        t = QLabel(title); t.setObjectName("SectionHeader")
        h.addWidget(t)
        h.addWidget(hair(), 1)
        return w

    @staticmethod
    def _row(title, subtitle, control):
        f = QFrame(); f.setObjectName("Card")
        h = QHBoxLayout(f)
        h.setContentsMargins(16, 12, 16, 12)
        h.setSpacing(16)
        v = QVBoxLayout(); v.setSpacing(2)
        t = QLabel(title); t.setObjectName("RowTitle")
        s = QLabel(subtitle); s.setObjectName("Muted"); s.setWordWrap(True)
        v.addWidget(t); v.addWidget(s)
        h.addLayout(v, 1)
        if isinstance(control, QWidget):
            h.addWidget(control, 0, Qt.AlignmentFlag.AlignVCenter)
        else:
            h.addLayout(control)
        return f

    def refresh(self):
        self.wrap_t.setChecked(bool(self.store.get("editor_word_wrap")))
        self.ln_t.setChecked(bool(self.store.get("editor_line_numbers")))
        self.lock_t.setChecked(bool(self.store.get("lock_window_size")))
        self.autosave_t.setChecked(bool(self.store.get("window_size_autosave")))
        self.top_t.setChecked(bool(self.store.get("always_on_top")))
        self.win_w.setValue(self.main.width())
        self.win_h.setValue(self.main.height())
        self.side_w.setValue(int(self.store.get("sidebar_width", 250)))

# -------------------------------------------------------------------- main
class MainWindow(QMainWindow):
    EDGE = 7

    def __init__(self, store):
        super().__init__()
        self.store = store
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon(brand_pixmap(48)))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(1280, 800)
        self.setMinimumSize(1000, 640)

        root = QWidget()
        self.setCentralWidget(root)
        rv = QVBoxLayout(root)
        rv.setContentsMargins(0, 0, 0, 0)
        rv.setSpacing(0)

        self.titlebar = TitleBar(self)
        rv.addWidget(self.titlebar)
        rv.addWidget(hair())

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        self.side = QFrame()
        self.side.setObjectName("Sidebar")
        sv = QVBoxLayout(self.side)
        sv.setContentsMargins(0, 0, 0, 0)
        sv.setSpacing(0)
        brand_wrap = QWidget()
        bh = QHBoxLayout(brand_wrap)
        bh.setContentsMargins(14, 14, 10, 14)
        bh.setSpacing(10)
        logo = QLabel(); logo.setPixmap(brand_pixmap(26))
        self.brand_text = QLabel(APP_NAME); self.brand_text.setObjectName("Brand")
        self.collapse_b = QPushButton()
        self.collapse_b.setObjectName("Ghost")
        self.collapse_b.setFixedSize(30, 30)
        self.collapse_b.setCursor(Qt.CursorShape.PointingHandCursor)
        self.collapse_b.clicked.connect(self.toggle_sidebar)
        bh.addWidget(logo); bh.addWidget(self.brand_text, 1); bh.addWidget(self.collapse_b)
        sv.addWidget(brand_wrap)
        sv.addWidget(hair())

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        self.pages = QStackedWidget()
        self.dashboard = DashboardPage(self)
        self.executor = ExecutorPage(self)
        self.scripthub = ScripthubPage(self)
        self.clients = ClientManagerPage(self)
        self.settings = SettingsPage(self)
        for pg in (self.dashboard, self.executor, self.scripthub, self.clients, self.settings):
            self.pages.addWidget(pg)
        self.nav_buttons = []
        for i, (ic, label) in enumerate([("dashboard", "Dashboard"), ("code", "Executor"),
                                         ("book", "Scripthub"), ("users", "Client Manager"),
                                         ("gear", "Settings")]):
            b = NavButton(ic, label)
            self.nav_group.addButton(b, i)
            self.nav_buttons.append(b)
            sv.addWidget(b)
        self.nav_group.idClicked.connect(self.show_page)
        self.nav_buttons[0].setChecked(True)
        sv.addStretch(1)
        ver = QLabel(VERSION); ver.setObjectName("Ver")
        ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ver.setContentsMargins(0, 0, 0, 10)
        sv.addWidget(ver)
        body.addWidget(self.side)

        body.addWidget(self.pages, 1)
        rv.addLayout(body, 1)

        self.setStyleSheet(QSS)
        self.apply_sidebar_width(int(store.get("sidebar_width", 250)),
                                 collapsed=bool(store.get("sidebar_collapsed")))
        ws = store.get("window_size")
        if store.get("window_size_autosave") and ws:
            try:
                self.resize(int(ws[0]), int(ws[1]))
            except (TypeError, ValueError):
                pass
        self.apply_window_lock()
        if store.get("always_on_top"):
            self.apply_always_on_top()
        self.refresh_all()
        self._ready = True

    # ---- frameless shell
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = 0 if self.isMaximized() else 10
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5), r, r)
        p.fillPath(path, QColor(BG))
        p.setPen(QPen(QColor("#2a2a2e"), 1))
        p.drawPath(path)
        p.end()

    def toggle_max(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
        self.titlebar.sync_max_icon()

    def showEvent(self, e):
        super().showEvent(e)
        self.titlebar.sync_max_icon()

    # NOTE: the nativeEvent edge-resize override was removed — on some
    # Windows/Python builds any touch of the native message in Python
    # crashes the process (0xC000041D) before the window appears.
    # Window dragging still works via TitleBar mouse events.

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if getattr(self, "_ready", False):
            s = self.store.settings
            if s.get("window_size_autosave") and not s.get("lock_window_size"):
                s["window_size"] = [self.width(), self.height()]
                self.store.save()

    # ---- helpers
    def open_link(self, key):
        url = LINKS.get(key, "")
        if url:
            QDesktopServices.openUrl(QUrl(url))
        else:
            QMessageBox.information(self, APP_NAME,
                                    f'Set the "{key}" URL in the LINKS constant at the top of zeno.py.')

    def show_page(self, idx):
        self.pages.setCurrentIndex(idx)
        b = self.nav_group.button(idx)
        if b and not b.isChecked():
            b.setChecked(True)
        self.refresh_all()
        self.repaint()

    def refresh_all(self):
        for pg in (self.dashboard, self.executor, self.scripthub, self.clients, self.settings):
            pg.refresh()

    def apply_window_lock(self):
        if self.store.get("lock_window_size"):
            self.setFixedSize(self.size())
        else:
            self.setMinimumSize(1000, 640)
            self.setMaximumSize(16777215, 16777215)

    def apply_window_size(self, w, h):
        if self.store.get("lock_window_size"):
            self.setFixedSize(int(w), int(h))
        else:
            self.resize(int(w), int(h))
        self.store.set("window_size", [int(w), int(h)])
        self.settings.refresh()

    def apply_sidebar_width(self, w, collapsed=None):
        if collapsed is None:
            collapsed = bool(self.store.get("sidebar_collapsed"))
        self.store.settings["sidebar_width"] = int(w)
        self.store.settings["sidebar_collapsed"] = collapsed
        self.store.save()
        self.side.setFixedWidth(64 if collapsed else int(w))
        for b in self.nav_buttons:
            b.set_collapsed(collapsed)
        self.brand_text.setVisible(not collapsed)
        self.collapse_b.setIcon(QIcon(icon("chev_r" if collapsed else "chev_l", 15)))

    def toggle_sidebar(self):
        self.apply_sidebar_width(int(self.store.get("sidebar_width", 250)),
                                 collapsed=not self.store.get("sidebar_collapsed"))

    def apply_always_on_top(self):
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint,
                           bool(self.store.get("always_on_top")))
        self.show()

    def restart_app(self):
        os.execv(sys.executable, [sys.executable, os.path.abspath(__file__)])

    def reset_data(self):
        r = QMessageBox.question(self, "Reset hub data",
                                 "Reset all Zeno settings? This can't be undone.",
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if r == QMessageBox.StandardButton.Yes:
            self.store.settings = dict(Store.DEFAULTS)
            self.store.save()
            self.apply_sidebar_width(250, collapsed=False)
            self.apply_window_lock()
            self.refresh_all()

# -------------------------------------------------------------------- demo
def demo_screenshots(outdir):
    app = QApplication.instance() or QApplication([])
    store = Store.__new__(Store)
    store.settings = dict(Store.DEFAULTS)
    store.save = lambda: None
    win = MainWindow(store)
    win.show()
    app.processEvents()
    out = Path(outdir); out.mkdir(parents=True, exist_ok=True)
    for i, name in enumerate(["dashboard", "executor", "scripthub", "clients", "settings"]):
        win.show_page(i)
        app.processEvents()
        win.grab().save(str(out / f"{name}.png"))
        print("saved", out / f"{name}.png")
    app.quit()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    f = QFont("Segoe UI")
    f.setPixelSize(13)
    app.setFont(f)
    if "--demo-shot" in sys.argv:
        idx = sys.argv.index("--demo-shot")
        demo_screenshots(sys.argv[idx + 1] if idx + 1 < len(sys.argv) else "./shots")
        return
    win = MainWindow(Store())
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()