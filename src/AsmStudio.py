"""
The code in this file was coded using AI.
I only know tkinter, and Pyside was the
only one that works cross platform...
"""

import sys
import os
import threading
import time
from datetime import datetime
from pathlib import Path
from contextlib import redirect_stdout

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QTextEdit, QListWidget, QListWidgetItem, QPushButton,
    QLabel, QStatusBar, QToolBar, QLineEdit, QFrame, QScrollBar,
    QSizePolicy, QMenuBar, QMenu, QFileDialog, QMessageBox,
    QTabWidget, QPlainTextEdit, QDialog, QDialogButtonBox,
    QCheckBox, QSpinBox, QGroupBox
)
from PySide6.QtCore import (
    Qt, QObject, Signal, Slot, QTimer, QThread, QSize, QFileSystemWatcher, QSettings
)
from PySide6.QtGui import (
    QFont, QColor, QPalette, QSyntaxHighlighter, QTextCharFormat,
    QAction, QKeySequence, QIcon, QPixmap, QPainter, QBrush, QPen,
    QTextCursor, QTextDocument
)
import re


# ─────────────────────────────────────────────
#  THEME  (amber-on-obsidian terminal aesthetic)
# ─────────────────────────────────────────────
COLORS = {
    "bg_deep":      "#0d0f14",
    "bg_panel":     "#13161e",
    "bg_widget":    "#1a1e2a",
    "bg_hover":     "#1f2435",
    "bg_selected":  "#252b3d",
    "accent":       "#e8a020",
    "accent_dim":   "#a06810",
    "accent_glow":  "#ffbd4a",
    "green":        "#4ec94e",
    "red":          "#e85050",
    "blue":         "#5a9cf8",
    "purple":       "#b07af8",
    "cyan":         "#3dcfcf",
    "text_bright":  "#f0ead6",
    "text_normal":  "#b8b0a0",
    "text_dim":     "#6a6458",
    "border":       "#2a2e3e",
    "border_bright":"#3a3e52",
    "scrollbar":    "#2a2e3e",
    "scrollbar_h":  "#e8a020",
}

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {COLORS['bg_deep']};
    color: {COLORS['text_normal']};
    font-family: 'Segoe UI', 'Ubuntu', sans-serif;
    font-size: 13px;
}}

/* ── Panels ── */
#sidebar {{
    background-color: {COLORS['bg_panel']};
    border-right: 1px solid {COLORS['border']};
}}
#viewer_panel {{
    background-color: {COLORS['bg_panel']};
    border-right: 1px solid {COLORS['border']};
}}
#console_panel {{
    background-color: {COLORS['bg_panel']};
}}
#panel_header {{
    background-color: {COLORS['bg_deep']};
    border-bottom: 1px solid {COLORS['border']};
    padding: 6px 10px;
    color: {COLORS['text_dim']};
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 2px;
    text-transform: uppercase;
}}

/* ── File List ── */
QListWidget {{
    background-color: transparent;
    border: none;
    outline: none;
    padding: 4px 0;
}}
QListWidget::item {{
    padding: 7px 14px;
    color: {COLORS['text_normal']};
    border-left: 2px solid transparent;
    border-radius: 0px;
}}
QListWidget::item:hover {{
    background-color: {COLORS['bg_hover']};
    color: {COLORS['text_bright']};
}}
QListWidget::item:selected {{
    background-color: {COLORS['bg_selected']};
    color: {COLORS['accent_glow']};
    border-left: 2px solid {COLORS['accent']};
}}

/* ── Code Editor / Console ── */
QPlainTextEdit, QTextEdit {{
    background-color: {COLORS['bg_widget']};
    color: {COLORS['text_bright']};
    border: none;
    border-radius: 0px;
    selection-background-color: {COLORS['accent_dim']};
    selection-color: {COLORS['text_bright']};
}}

/* ── Buttons ── */
QPushButton {{
    background-color: {COLORS['bg_widget']};
    color: {COLORS['text_normal']};
    border: 1px solid {COLORS['border_bright']};
    border-radius: 4px;
    padding: 6px 14px;
    font-size: 12px;
}}
QPushButton:hover {{
    background-color: {COLORS['bg_hover']};
    color: {COLORS['text_bright']};
    border-color: {COLORS['accent_dim']};
}}
QPushButton:pressed {{
    background-color: {COLORS['bg_selected']};
}}
QPushButton:disabled {{
    color: {COLORS['text_dim']};
    border-color: {COLORS['border']};
}}
#run_btn {{
    background-color: {COLORS['accent_dim']};
    color: {COLORS['text_bright']};
    border: 1px solid {COLORS['accent']};
    font-weight: bold;
    font-size: 13px;
    padding: 8px 20px;
    border-radius: 4px;
}}
#run_btn:hover {{
    background-color: {COLORS['accent']};
    color: #000;
}}
#run_btn:disabled {{
    background-color: {COLORS['bg_widget']};
    color: {COLORS['text_dim']};
    border-color: {COLORS['border']};
}}
#stop_btn {{
    background-color: #5a1a1a;
    color: {COLORS['red']};
    border: 1px solid {COLORS['red']};
    font-weight: bold;
    padding: 8px 20px;
    border-radius: 4px;
}}
#stop_btn:hover {{
    background-color: {COLORS['red']};
    color: #fff;
}}

/* ── Search bar ── */
QLineEdit {{
    background-color: {COLORS['bg_widget']};
    color: {COLORS['text_bright']};
    border: 1px solid {COLORS['border']};
    border-radius: 3px;
    padding: 5px 8px;
    selection-background-color: {COLORS['accent_dim']};
}}
QLineEdit:focus {{
    border-color: {COLORS['accent']};
}}

/* ── Status Bar ── */
QStatusBar {{
    background-color: {COLORS['bg_deep']};
    color: {COLORS['text_dim']};
    border-top: 1px solid {COLORS['border']};
    font-size: 11px;
}}
QStatusBar::item {{ border: none; }}

/* ── Toolbar ── */
QToolBar {{
    background-color: {COLORS['bg_deep']};
    border-bottom: 1px solid {COLORS['border']};
    spacing: 4px;
    padding: 3px 6px;
}}
QToolBar QToolButton {{
    background: transparent;
    color: {COLORS['text_normal']};
    border: 1px solid transparent;
    border-radius: 3px;
    padding: 4px 8px;
    font-size: 12px;
}}
QToolBar QToolButton:hover {{
    background-color: {COLORS['bg_hover']};
    border-color: {COLORS['border_bright']};
    color: {COLORS['text_bright']};
}}

/* ── Tab Widget ── */
QTabWidget::pane {{
    border: none;
    background-color: {COLORS['bg_panel']};
}}
QTabBar::tab {{
    background-color: {COLORS['bg_deep']};
    color: {COLORS['text_dim']};
    padding: 7px 18px;
    border: 1px solid {COLORS['border']};
    border-bottom: none;
    margin-right: 1px;
    font-size: 12px;
}}
QTabBar::tab:selected {{
    background-color: {COLORS['bg_panel']};
    color: {COLORS['accent']};
    border-bottom: 1px solid {COLORS['bg_panel']};
}}
QTabBar::tab:hover {{
    color: {COLORS['text_bright']};
}}

/* ── Scrollbars ── */
QScrollBar:vertical {{
    background: {COLORS['bg_deep']};
    width: 8px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {COLORS['scrollbar']};
    border-radius: 4px;
    min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{
    background: {COLORS['scrollbar_h']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background: {COLORS['bg_deep']};
    height: 8px;
}}
QScrollBar::handle:horizontal {{
    background: {COLORS['scrollbar']};
    border-radius: 4px;
    min-width: 20px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {COLORS['scrollbar_h']};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}

/* ── Splitter ── */
QSplitter::handle {{
    background-color: {COLORS['border']};
    width: 1px;
    height: 1px;
}}
QSplitter::handle:hover {{
    background-color: {COLORS['accent_dim']};
}}

/* ── Menu ── */
QMenuBar {{
    background-color: {COLORS['bg_deep']};
    color: {COLORS['text_normal']};
    border-bottom: 1px solid {COLORS['border']};
    font-size: 12px;
    padding: 2px;
}}
QMenuBar::item:selected {{
    background-color: {COLORS['bg_hover']};
    color: {COLORS['text_bright']};
}}
QMenu {{
    background-color: {COLORS['bg_widget']};
    color: {COLORS['text_normal']};
    border: 1px solid {COLORS['border_bright']};
    padding: 4px 0;
}}
QMenu::item {{
    padding: 6px 20px;
}}
QMenu::item:selected {{
    background-color: {COLORS['bg_selected']};
    color: {COLORS['accent_glow']};
}}
QMenu::separator {{
    height: 1px;
    background: {COLORS['border']};
    margin: 4px 8px;
}}

/* ── GroupBox ── */
QGroupBox {{
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    margin-top: 12px;
    padding-top: 8px;
    color: {COLORS['text_dim']};
    font-size: 11px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px;
    color: {COLORS['accent_dim']};
    font-size: 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
}}
"""


# ─────────────────────────────────────────────
#  ASM SYNTAX HIGHLIGHTER
# ─────────────────────────────────────────────
class AsmHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rules = []

        def fmt(color, bold=False, italic=False):
            f = QTextCharFormat()
            f.setForeground(QColor(color))
            if bold:   f.setFontWeight(700)
            if italic: f.setFontItalic(True)
            return f

        # ── Schema-based instruction groups ──────────────────────────────

        # Arithmetic: set add sub mul div mod pow abs root log ln exp fact
        #             flr ceil rnd trnc min max
        arith = (r'(?<![A-Za-z0-9_])'
                 r'(set|add|sub|mul|div|mod|pow|abs|root|log|ln|exp|fact|'
                 r'flr|ceil|rnd|trnc|min|max)'
                 r'(?![A-Za-z0-9_])')
        self.rules.append((re.compile(arith), fmt(COLORS['blue'], bold=True)))

        # Bitwise: and or xor nand nor xnor shl shr rol ror
        #          bitset bitclr bittog bitget bitson bitlen
        bitwise = (r'(?<![A-Za-z0-9_])'
                   r'(and|or|xor|nand|nor|xnor|shl|shr|rol|ror|'
                   r'bitset|bitclr|bittog|bitget|bitson|bitlen)'
                   r'(?![A-Za-z0-9_])')
        self.rules.append((re.compile(bitwise), fmt(COLORS['purple'], bold=True)))

        # Trig: sin cos tan csc sec cot
        trig = (r'(?<![A-Za-z0-9_])'
                r'(sin|cos|tan|csc|sec|cot)'
                r'(?![A-Za-z0-9_])')
        self.rules.append((re.compile(trig), fmt(COLORS['cyan'], bold=True)))

        # String ops: cast len strsub strfind strsplit strjoin strrev strupper strlower strtrim
        strops = (r'(?<![A-Za-z0-9_])'
                  r'(cast|len|strsub|strfind|strsplit|strjoin|strrev|strupper|strlower|strtrim)'
                  r'(?![A-Za-z0-9_])')
        self.rules.append((re.compile(strops), fmt("#e8964a", bold=True)))

        # Type checks: typeof isint isfloat isstr isnone
        typechk = (r'(?<![A-Za-z0-9_])'
                   r'(typeof|isint|isfloat|isstr|isnone)'
                   r'(?![A-Za-z0-9_])')
        self.rules.append((re.compile(typechk), fmt(COLORS['green'], bold=True)))

        # Control flow: call ret jeq jne jgt jlt jge jle jz jnz
        flow = (r'(?<![A-Za-z0-9_])'
                r'(jmp|jeq|jne|jgt|jlt|jge|jle|jz|jnz)'
                r'(?![A-Za-z0-9_])')
        self.rules.append((re.compile(flow), fmt(COLORS['accent_glow'], bold=True)))

        # I/O + misc: print println input clear halt --
        io_ops = (r'(?<![A-Za-z0-9_])'
                  r'(println|print|input|clear|halt|sound|sleep|clockspeed)'
                  r'(?![A-Za-z0-9_])')
        self.rules.append((re.compile(io_ops), fmt("#7dd87d", bold=True)))
        self.rules.append((re.compile(r'(?m)^[ \t]*--[ \t]*$'), fmt(COLORS['text_dim'])))

        # Graphics: draw_bg draw_rect draw_circ update get_mouse get_press
        #           draw_line draw_text draw_tri
        gfx = (r'(?<![A-Za-z0-9_])'
               r'(draw_bg|draw_rect|draw_circ|draw_line|draw_text|draw_tri|'
               r'update|get_mouse|get_press|get_scroll)'
               r'(?![A-Za-z0-9_])')
        self.rules.append((re.compile(gfx), fmt("#d07af0", bold=True)))

        # Labels (identifier followed by colon at line start)
        self.rules.append((re.compile(r'^:[A-Za-z_][A-Za-z0-9_]*\s*', re.MULTILINE),
                           fmt(COLORS['accent'], bold=True)))

        # String literals
        self.rules.append((re.compile(r'"[^"]*"'), fmt("#c8a070")))
        self.rules.append((re.compile(r"'[^']*'"), fmt("#c8a070")))

        # Comments: ; // #
        self.rules.append((re.compile(r'(?m)^[ \t]*--.*$'),
                           fmt(COLORS['text_dim'], italic=True)))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            for m in pattern.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), fmt)


# ─────────────────────────────────────────────
#  LINE-NUMBER GUTTER
# ─────────────────────────────────────────────
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor._line_number_width(), 0)

    def paintEvent(self, event):
        self.editor._paint_line_numbers(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self._update_line_number_width)
        self.updateRequest.connect(self._update_line_number_area)
        self._update_line_number_width(0)

        font = QFont("Cascadia Code", 11)
        font.setStyleHint(QFont.Monospace)
        if not font.exactMatch():
            font = QFont("Consolas", 11)
            if not font.exactMatch():
                font = QFont("Courier New", 11)
        self.setFont(font)
        self.setTabStopDistance(28)
        self.setReadOnly(True)

    def _line_number_width(self):
        digits = max(3, len(str(self.blockCount())))
        return 14 + self.fontMetrics().horizontalAdvance('9') * digits

    def _update_line_number_width(self, _):
        self.setViewportMargins(self._line_number_width(), 0, 0, 0)

    def _update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self._update_line_number_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(cr.left(), cr.top(), self._line_number_width(), cr.height())

    def _paint_line_numbers(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(COLORS['bg_deep']))
        painter.setPen(QColor(COLORS['text_dim']))

        font = self.font()
        font.setPointSize(font.pointSize() - 1)
        painter.setFont(font)

        block = self.firstVisibleBlock()
        block_num = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.drawText(
                    0, top,
                    self.line_number_area.width() - 6,
                    self.fontMetrics().height(),
                    Qt.AlignRight, str(block_num + 1)
                )
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_num += 1


# ─────────────────────────────────────────────
#  CONSOLE OUTPUT WIDGET
# ─────────────────────────────────────────────
class ConsoleOutput(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        font = QFont("Cascadia Code", 11)
        font.setStyleHint(QFont.Monospace)
        if not font.exactMatch():
            font = QFont("Consolas", 11)
        self.setFont(font)
        self.setReadOnly(True)
        self.setMaximumBlockCount(5000)
        self._running_time_start = None

    def append_colored(self, text, color=None):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        fmt = QTextCharFormat()
        if color:
            fmt.setForeground(QColor(color))
        cursor.setCharFormat(fmt)
        cursor.insertText(text)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    def write_stdout(self, text):
        self.append_colored(text, COLORS['text_bright'])

    def write_info(self, text):
        self.append_colored(text, COLORS['cyan'])

    def write_success(self, text):
        self.append_colored(text, COLORS['green'])

    def write_error(self, text):
        self.append_colored(text, COLORS['red'])

    def write_accent(self, text):
        self.append_colored(text, COLORS['accent'])


# ─────────────────────────────────────────────
#  THREADING BRIDGE
# ─────────────────────────────────────────────
class Signaller(QObject):
    text_out    = Signal(str, str)   # text, color
    run_done    = Signal(float)      # elapsed seconds
    run_error   = Signal(str)


class StdoutCapture:
    """File-like object that routes stdout to the signaller."""
    def __init__(self, signaller: Signaller):
        self.sig = signaller

    def write(self, text):
        if text:
            self.sig.text_out.emit(str(text), COLORS['text_bright'])

    def flush(self):
        pass


# ─────────────────────────────────────────────
#  FIND BAR
# ─────────────────────────────────────────────
class FindBar(QWidget):
    def __init__(self, editor: CodeEditor, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.setVisible(False)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Find in file…")
        self.input.textChanged.connect(self._search)
        self.input.returnPressed.connect(self._find_next)

        self.lbl = QLabel("0 matches")
        self.lbl.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 11px;")

        self.btn_prev = QPushButton("▲")
        self.btn_prev.setFixedWidth(28)
        self.btn_next = QPushButton("▼")
        self.btn_next.setFixedWidth(28)
        self.btn_prev.clicked.connect(self._find_prev)
        self.btn_next.clicked.connect(self._find_next)

        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedWidth(28)
        self.btn_close.clicked.connect(self.hide_bar)

        layout.addWidget(QLabel("Find:"))
        layout.addWidget(self.input)
        layout.addWidget(self.lbl)
        layout.addWidget(self.btn_prev)
        layout.addWidget(self.btn_next)
        layout.addWidget(self.btn_close)

        self._matches = []
        self._current = -1

    def show_bar(self):
        self.setVisible(True)
        self.input.setFocus()
        self.input.selectAll()

    def hide_bar(self):
        self.setVisible(False)
        self.editor.setFocus()
        # Clear highlights
        cursor = self.editor.textCursor()
        cursor.clearSelection()
        self.editor.setTextCursor(cursor)

    def _search(self, query):
        self._matches = []
        self._current = -1
        if not query:
            self.lbl.setText("0 matches")
            return
        doc = self.editor.document()
        cursor = QTextCursor(doc)
        while True:
            cursor = doc.find(query, cursor, QTextDocument.FindFlag(0))
            if cursor.isNull():
                break
            self._matches.append(cursor)
        count = len(self._matches)
        self.lbl.setText(f"{count} match{'es' if count != 1 else ''}")
        self.lbl.setStyleSheet(f"color: {COLORS['green'] if count else COLORS['red']}; font-size: 11px;")
        if count:
            self._current = 0
            self._highlight_current()

    def _highlight_current(self):
        if not self._matches:
            return
        cursor = self._matches[self._current]
        self.editor.setTextCursor(cursor)
        self.editor.ensureCursorVisible()

    def _find_next(self):
        if not self._matches: return
        self._current = (self._current + 1) % len(self._matches)
        self._highlight_current()

    def _find_prev(self):
        if not self._matches: return
        self._current = (self._current - 1) % len(self._matches)
        self._highlight_current()


# ─────────────────────────────────────────────
#  SETTINGS DIALOG
# ─────────────────────────────────────────────
class SettingsDialog(QDialog):
    def __init__(self, parent=None, programs_dir="examples"):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(380)
        self.setStyleSheet(STYLESHEET)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        grp = QGroupBox("Programs Directory")
        grp_layout = QHBoxLayout(grp)
        self.dir_input = QLineEdit(str(programs_dir))
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self._browse)
        grp_layout.addWidget(self.dir_input)
        grp_layout.addWidget(browse_btn)

        grp2 = QGroupBox("Console")
        grp2_layout = QVBoxLayout(grp2)
        self.cb_timestamps = QCheckBox("Show timestamps in console")
        self.cb_timestamps.setChecked(True)
        self.cb_autoscroll = QCheckBox("Auto-scroll console output")
        self.cb_autoscroll.setChecked(True)
        grp2_layout.addWidget(self.cb_timestamps)
        grp2_layout.addWidget(self.cb_autoscroll)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(grp)
        layout.addWidget(grp2)
        layout.addWidget(buttons)

    def _browse(self):
        path = QFileDialog.getExistingDirectory(self, "Select Programs Directory")
        if path:
            self.dir_input.setText(path)

    def get_values(self):
        return {
            "programs_dir": self.dir_input.text(),
            "timestamps": self.cb_timestamps.isChecked(),
            "autoscroll": self.cb_autoscroll.isChecked(),
        }


# ─────────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────────
class AssemblyRunnerIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AsmStudio")
        self.resize(1280, 800)
        self.setMinimumSize(900, 600)

        # State
        # AFTER
        settings = QSettings("AsmStudio", "AssemblyRunnerIDE")
        self.programs_dir = Path(settings.value("programs_dir", "programs"))
        self.show_timestamps = settings.value("show_timestamps", True, type=bool)
        self.autoscroll = settings.value("autoscroll", True, type=bool)

        self.current_file: Path | None = None
        self.is_running = False
        self.show_timestamps = True
        self.autoscroll = True
        self.run_start_time = 0.0
        self._editor_dirty = False
        self.elapsed_timer = QTimer()
        self.elapsed_timer.timeout.connect(self._tick_elapsed)
        self._run_thread: threading.Thread | None = None

        # Signal bridge
        self.sig = Signaller()
        self.sig.text_out.connect(self._on_output)
        self.sig.run_done.connect(self._on_run_done)
        self.sig.run_error.connect(self._on_run_error)

        # File watcher
        self.watcher = QFileSystemWatcher()
        self.watcher.directoryChanged.connect(self._refresh_file_list)

        self._build_ui()
        self._build_menu()
        self.setStyleSheet(STYLESHEET)
        self._refresh_file_list()
        self._update_statusbar("Ready")

    def _save_settings(self):
        settings = QSettings("AsmStudio", "AssemblyRunnerIDE")
        settings.setValue("programs_dir", str(self.programs_dir))
        settings.setValue("show_timestamps", self.show_timestamps)
        settings.setValue("autoscroll", self.autoscroll)

    # ── UI Construction ──────────────────────
    def _build_ui(self):
        # ── Toolbar ──
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        self.act_run = QAction("▶  Run", self)
        self.act_run.setShortcut(QKeySequence("F5"))
        self.act_run.triggered.connect(self._run_selected)
        toolbar.addAction(self.act_run)

        self.act_stop = QAction("■  Stop", self)
        self.act_stop.setShortcut(QKeySequence("F6"))
        self.act_stop.setEnabled(False)
        self.act_stop.triggered.connect(self._stop_run)
        toolbar.addAction(self.act_stop)

        toolbar.addSeparator()

        self.act_save = QAction("⬆  Save", self)
        self.act_save.setShortcut(QKeySequence("Ctrl+S"))
        self.act_save.triggered.connect(self._save_file)
        self.act_save.setEnabled(False)
        toolbar.addAction(self.act_save)

        act_save_as = QAction("Save As…", self)
        act_save_as.setShortcut(QKeySequence("Ctrl+Shift+S"))
        act_save_as.triggered.connect(self._save_file_as)
        toolbar.addAction(act_save_as)

        toolbar.addSeparator()

        act_clear = QAction("⊘  Clear Console", self)
        act_clear.setShortcut(QKeySequence("Ctrl+K"))
        act_clear.triggered.connect(self._clear_console)
        toolbar.addAction(act_clear)

        act_save_log = QAction("⬇  Save Log", self)
        act_save_log.triggered.connect(self._save_log)
        toolbar.addAction(act_save_log)

        toolbar.addSeparator()

        act_find = QAction("⌕  Find", self)
        act_find.setShortcut(QKeySequence("Ctrl+F"))
        act_find.triggered.connect(self._show_find)
        toolbar.addAction(act_find)

        act_refresh = QAction("↺  Refresh", self)
        act_refresh.setShortcut(QKeySequence("F5"))
        act_refresh.triggered.connect(self._refresh_file_list)
        toolbar.addAction(act_refresh)

        toolbar.addSeparator()

        # Search box in toolbar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search files…")
        self.search_box.setFixedWidth(180)
        self.search_box.textChanged.connect(self._filter_files)
        toolbar.addWidget(self.search_box)

        # ── Central splitter layout ──
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(1)
        root_layout.addWidget(splitter)

        # ── Left Sidebar (file list) ──
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setMinimumWidth(180)
        sidebar.setMaximumWidth(320)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        hdr_files = QLabel("PROGRAMS")
        hdr_files.setObjectName("panel_header")
        hdr_files.setContentsMargins(10, 6, 10, 6)
        sidebar_layout.addWidget(hdr_files)

        self.file_list = QListWidget()
        self.file_list.currentItemChanged.connect(self._on_file_selected)
        self.file_list.itemDoubleClicked.connect(self._run_selected)
        sidebar_layout.addWidget(self.file_list)

        # File info footer
        self.file_info_label = QLabel("No file selected")
        self.file_info_label.setContentsMargins(10, 4, 10, 4)
        self.file_info_label.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 10px; border-top: 1px solid {COLORS['border']};")
        self.file_info_label.setWordWrap(True)
        sidebar_layout.addWidget(self.file_info_label)

        # Run button at bottom of sidebar
        btn_row = QWidget()
        btn_row.setStyleSheet(f"background-color: {COLORS['bg_deep']}; padding: 6px;")
        btn_row_layout = QHBoxLayout(btn_row)
        btn_row_layout.setContentsMargins(6, 6, 6, 6)
        btn_row_layout.setSpacing(6)

        self.run_btn = QPushButton("▶  Run")
        self.run_btn.setObjectName("run_btn")
        self.run_btn.clicked.connect(self._run_selected)
        self.run_btn.setEnabled(False)

        self.stop_btn = QPushButton("■")
        self.stop_btn.setObjectName("stop_btn")
        self.stop_btn.clicked.connect(self._stop_run)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setFixedWidth(36)

        btn_row_layout.addWidget(self.run_btn)
        btn_row_layout.addWidget(self.stop_btn)
        sidebar_layout.addWidget(btn_row)

        splitter.addWidget(sidebar)

        # ── Center (code viewer) ──
        viewer_panel = QWidget()
        viewer_panel.setObjectName("viewer_panel")
        viewer_layout = QVBoxLayout(viewer_panel)
        viewer_layout.setContentsMargins(0, 0, 0, 0)
        viewer_layout.setSpacing(0)

        # File path header
        self.viewer_header = QLabel("SELECT A FILE TO VIEW")
        self.viewer_header.setObjectName("panel_header")
        self.viewer_header.setContentsMargins(10, 6, 10, 6)
        viewer_layout.addWidget(self.viewer_header)

        # Tab: Source | Info
        self.view_tabs = QTabWidget()

        # Source tab
        src_tab = QWidget()
        src_layout = QVBoxLayout(src_tab)
        src_layout.setContentsMargins(0, 0, 0, 0)
        src_layout.setSpacing(0)

        self.code_editor = CodeEditor()
        self.highlighter = AsmHighlighter(self.code_editor.document())

        self.find_bar = FindBar(self.code_editor)
        self.find_bar.setStyleSheet(f"background-color: {COLORS['bg_deep']}; border-top: 1px solid {COLORS['border']};")

        src_layout.addWidget(self.code_editor)
        src_layout.addWidget(self.find_bar)

        self.view_tabs.addTab(src_tab, "Source")

        # Info tab
        info_tab = QWidget()
        info_layout = QVBoxLayout(info_tab)
        info_layout.setContentsMargins(12, 12, 12, 12)
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setStyleSheet(f"background-color: {COLORS['bg_widget']}; color: {COLORS['text_normal']}; font-size: 12px;")
        info_layout.addWidget(self.info_text)
        self.view_tabs.addTab(info_tab, "File Info")

        # ── Edit tab ──
        edit_tab = QWidget()
        edit_layout = QVBoxLayout(edit_tab)
        edit_layout.setContentsMargins(0, 0, 0, 0)
        edit_layout.setSpacing(0)

        # Editor toolbar
        edit_toolbar = QWidget()
        edit_toolbar.setStyleSheet(
            f"background-color: {COLORS['bg_deep']}; border-bottom: 1px solid {COLORS['border']};"
        )
        edit_tb_layout = QHBoxLayout(edit_toolbar)
        edit_tb_layout.setContentsMargins(8, 4, 8, 4)
        edit_tb_layout.setSpacing(6)

        self.save_btn = QPushButton("⬆  Save")
        self.save_btn.setToolTip("Save (Ctrl+S)")
        self.save_btn.clicked.connect(self._save_file)
        self.save_btn.setEnabled(False)
        self.save_btn.setStyleSheet(
            f"QPushButton {{ background: {COLORS['accent_dim']}; color: {COLORS['text_bright']};"
            f" border: 1px solid {COLORS['accent']}; border-radius: 3px; padding: 4px 12px; font-weight: bold; }}"
            f"QPushButton:hover {{ background: {COLORS['accent']}; color: #000; }}"
            f"QPushButton:disabled {{ background: {COLORS['bg_widget']}; color: {COLORS['text_dim']};"
            f" border-color: {COLORS['border']}; }}"
        )

        save_as_btn = QPushButton("Save As…")
        save_as_btn.setToolTip("Save As (Ctrl+Shift+S)")
        save_as_btn.clicked.connect(self._save_file_as)

        revert_btn = QPushButton("↺  Revert")
        revert_btn.setToolTip("Discard changes and reload from disk")
        revert_btn.clicked.connect(self._revert_file)

        self.dirty_label = QLabel("")
        self.dirty_label.setStyleSheet(f"color: {COLORS['accent']}; font-size: 12px;")

        edit_tb_layout.addWidget(self.save_btn)
        edit_tb_layout.addWidget(save_as_btn)
        edit_tb_layout.addWidget(revert_btn)
        edit_tb_layout.addStretch()
        edit_tb_layout.addWidget(self.dirty_label)

        # The writable editor
        self.text_editor = CodeEditor()
        self.text_editor.setReadOnly(False)
        self.editor_highlighter = AsmHighlighter(self.text_editor.document())
        self.text_editor.document().contentsChanged.connect(self._on_editor_modified)
        self.text_editor.cursorPositionChanged.connect(self._update_cursor_pos)

        # Find bar for editor too
        self.editor_find_bar = FindBar(self.text_editor)
        self.editor_find_bar.setStyleSheet(
            f"background-color: {COLORS['bg_deep']}; border-top: 1px solid {COLORS['border']};"
        )

        edit_layout.addWidget(edit_toolbar)
        edit_layout.addWidget(self.text_editor)
        edit_layout.addWidget(self.editor_find_bar)

        self.view_tabs.addTab(edit_tab, "Edit")
        self.view_tabs.tabBar().setTabTextColor(2, QColor(COLORS['green']))

        viewer_layout.addWidget(self.view_tabs)
        splitter.addWidget(viewer_panel)

        # ── Right (console) ──
        console_panel = QWidget()
        console_panel.setObjectName("console_panel")
        console_layout = QVBoxLayout(console_panel)
        console_layout.setContentsMargins(0, 0, 0, 0)
        console_layout.setSpacing(0)

        # Console header with elapsed time
        console_hdr = QWidget()
        console_hdr.setStyleSheet(f"background-color: {COLORS['bg_deep']}; border-bottom: 1px solid {COLORS['border']};")
        console_hdr_layout = QHBoxLayout(console_hdr)
        console_hdr_layout.setContentsMargins(10, 5, 10, 5)

        console_title = QLabel("CONSOLE OUTPUT")
        console_title.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 10px; font-weight: bold; letter-spacing: 2px;")

        self.elapsed_label = QLabel("")
        self.elapsed_label.setStyleSheet(f"color: {COLORS['accent']}; font-size: 11px; font-family: 'Consolas';")

        console_hdr_layout.addWidget(console_title)
        console_hdr_layout.addStretch()
        console_hdr_layout.addWidget(self.elapsed_label)

        console_layout.addWidget(console_hdr)

        self.console = ConsoleOutput()
        console_layout.addWidget(self.console)

        splitter.addWidget(console_panel)

        # Splitter proportions: sidebar | viewer | console
        splitter.setSizes([220, 520, 480])

        # ── Status Bar ──
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(f"color: {COLORS['text_dim']};")
        self.status_bar.addWidget(self.status_label)

        self.status_bar.addPermanentWidget(QLabel("  "))
        self.line_col_label = QLabel("")
        self.line_col_label.setStyleSheet(f"color: {COLORS['text_dim']};")
        self.status_bar.addPermanentWidget(self.line_col_label)

        self.status_bar.addPermanentWidget(QLabel("  "))
        self.prog_count_label = QLabel("")
        self.prog_count_label.setStyleSheet(f"color: {COLORS['text_dim']};")
        self.status_bar.addPermanentWidget(self.prog_count_label)

        self.code_editor.cursorPositionChanged.connect(self._update_cursor_pos)

    def _build_menu(self):
        menu = self.menuBar()

        # File
        file_menu = menu.addMenu("File")
        act_new_m = QAction("New File…", self)
        act_new_m.setShortcut(QKeySequence("Ctrl+N"))
        act_new_m.triggered.connect(self._new_file)
        file_menu.addAction(act_new_m)

        act_open_dir = QAction("Open Programs Folder…", self)
        act_open_dir.triggered.connect(self._open_programs_folder)
        file_menu.addAction(act_open_dir)

        act_open_file = QAction("Open .asm File…", self)
        act_open_file.setShortcut(QKeySequence("Ctrl+O"))
        act_open_file.triggered.connect(self._open_single_file)
        file_menu.addAction(act_open_file)

        file_menu.addSeparator()

        act_save_m = QAction("Save", self)
        act_save_m.setShortcut(QKeySequence("Ctrl+S"))
        act_save_m.triggered.connect(self._save_file)
        file_menu.addAction(act_save_m)

        act_save_as_m = QAction("Save As…", self)
        act_save_as_m.setShortcut(QKeySequence("Ctrl+Shift+S"))
        act_save_as_m.triggered.connect(self._save_file_as)
        file_menu.addAction(act_save_as_m)

        act_revert_m = QAction("Revert to Saved", self)
        act_revert_m.triggered.connect(self._revert_file)
        file_menu.addAction(act_revert_m)

        file_menu.addSeparator()

        act_save_log = QAction("Save Console Log…", self)
        act_save_log.triggered.connect(self._save_log)
        file_menu.addAction(act_save_log)

        file_menu.addSeparator()

        act_quit = QAction("Quit", self)
        act_quit.setShortcut(QKeySequence("Ctrl+Q"))
        act_quit.triggered.connect(self.close)
        file_menu.addAction(act_quit)

        # Run
        run_menu = menu.addMenu("Run")
        act_run = QAction("Run Selected (F5)", self)
        act_run.triggered.connect(self._run_selected)
        run_menu.addAction(act_run)

        act_stop = QAction("Stop (F6)", self)
        act_stop.triggered.connect(self._stop_run)
        run_menu.addAction(act_stop)

        run_menu.addSeparator()

        act_clear = QAction("Clear Console (Ctrl+K)", self)
        act_clear.triggered.connect(self._clear_console)
        run_menu.addAction(act_clear)

        # View
        view_menu = menu.addMenu("View")
        act_find = QAction("Find in File (Ctrl+F)", self)
        act_find.triggered.connect(self._show_find)
        view_menu.addAction(act_find)

        act_refresh = QAction("Refresh File List", self)
        act_refresh.triggered.connect(self._refresh_file_list)
        view_menu.addAction(act_refresh)

        # Tools
        tools_menu = menu.addMenu("Tools")
        act_settings = QAction("Settings…", self)
        act_settings.triggered.connect(self._open_settings)
        tools_menu.addAction(act_settings)

        act_stats = QAction("File Statistics", self)
        act_stats.triggered.connect(self._show_file_stats)
        tools_menu.addAction(act_stats)

    # ── File List Management ──────────────────
    def _refresh_file_list(self, *_):
        restore_selection = getattr(self, "_restore_selection", True)

        prev_item = self.file_list.currentItem()
        prev_name = prev_item.text() if prev_item else None
        self.file_list.clear()

        if not self.programs_dir.exists():
            self._update_statusbar(f"Directory not found: '{self.programs_dir}'")
            return

        # Watch the directory
        if str(self.programs_dir) not in self.watcher.directories():
            self.watcher.addPath(str(self.programs_dir))

        asm_files = sorted(self.programs_dir.glob("*.asm"))
        for f in asm_files:
            item = QListWidgetItem(f"  {f.name}")
            item.setData(Qt.UserRole, f)
            self.file_list.addItem(item)

        count = len(asm_files)
        self.prog_count_label.setText(f"{count} file{'s' if count != 1 else ''}  ")

        # Restore selection
        if restore_selection and prev_name:
            for i in range(self.file_list.count()):
                if prev_name.strip() == self.file_list.item(i).text().strip():
                    self.file_list.setCurrentRow(i)
                    break

        if count == 0:
            self._update_statusbar(f"No .asm files found in '{self.programs_dir}'")

    def _filter_files(self, query):
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            item.setHidden(query.lower() not in item.text().lower())

    def _on_file_selected(self, item, _prev=None):
        if item is None:
            return
        path: Path = item.data(Qt.UserRole)
        if path is None:
            return
        # Guard: ask to save before switching away
        if not self._confirm_discard():
            # Reselect the previous file in the list without triggering recursion
            if self.current_file:
                for i in range(self.file_list.count()):
                    if self.file_list.item(i).data(Qt.UserRole) == self.current_file:
                        self.file_list.blockSignals(True)
                        self.file_list.setCurrentRow(i)
                        self.file_list.blockSignals(False)
                        break
            return
        self.current_file = path
        self._load_file(path)
        self.run_btn.setEnabled(True)
        self._update_statusbar(f"Loaded: {path.name}")

    # ── File Loading ─────────────────────────
    def _load_file(self, path: Path):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            self.console.write_error(f"[ERROR] Cannot read {path.name}: {e}\n")
            return

        self.code_editor.setPlainText(text)
        self.viewer_header.setText(str(path))
        self._update_file_info(path, text)

        # Load into editor without triggering the dirty flag
        self.text_editor.document().blockSignals(True)
        self.text_editor.setPlainText(text)
        self.text_editor.document().blockSignals(False)
        self._set_dirty(False)

    def _update_file_info(self, path: Path, text: str):
        lines = text.splitlines()
        size = path.stat().st_size if path.exists() else 0
        mtime = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S") if path.exists() else "?"
        labels = sum(1 for l in lines if re.match(r'^[A-Za-z_][A-Za-z0-9_]*\s*:', l))
        comments = sum(1 for l in lines if l.strip().startswith(';') or l.strip().startswith('//')  or l.strip().startswith('#'))
        instrs = sum(1 for l in lines if l.strip() and not l.strip().startswith(';') and not l.strip().startswith('//'))

        info = f"""<style>
            body {{ color: {COLORS['text_normal']}; font-family: Consolas, monospace; font-size: 12px; }}
            td {{ padding: 3px 12px 3px 0; }}
            .key {{ color: {COLORS['text_dim']}; }}
            .val {{ color: {COLORS['accent_glow']}; }}
            .sec {{ color: {COLORS['accent']}; font-weight: bold; margin-top: 10px; display: block; }}
        </style>
        <table>
        <tr><td class='key'>Name</td><td class='val'>{path.name}</td></tr>
        <tr><td class='key'>Path</td><td class='val'>{path.parent}</td></tr>
        <tr><td class='key'>Size</td><td class='val'>{size:,} bytes</td></tr>
        <tr><td class='key'>Modified</td><td class='val'>{mtime}</td></tr>
        <tr><td colspan='2'><span class='sec'>CODE STATS</span></td></tr>
        <tr><td class='key'>Total lines</td><td class='val'>{len(lines)}</td></tr>
        <tr><td class='key'>Code lines</td><td class='val'>{instrs}</td></tr>
        <tr><td class='key'>Comment lines</td><td class='val'>{comments}</td></tr>
        <tr><td class='key'>Labels</td><td class='val'>{labels}</td></tr>
        </table>"""
        self.info_text.setHtml(info)

        short = f"{len(lines)} lines  •  {size:,} B  •  {labels} labels"
        self.file_info_label.setText(short)

    # ── Run / Stop ───────────────────────────
    def _run_selected(self, *_):
        if self.is_running:
            return
        if self.current_file is None:
            self._update_statusbar("No file selected")
            return

        self.is_running = True
        self.run_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.act_run.setEnabled(False)
        self.act_stop.setEnabled(True)

        ts = datetime.now().strftime("%H:%M:%S") if self.show_timestamps else ""
        if ts:
            header = f"\n  [{ts}]  ▶  {self.current_file.name}\n"
        else:
            header = f"\n  ▶  {self.current_file.name}\n"
        self.console.write_accent(header)

        self.run_start_time = time.time()
        self.elapsed_timer.start(100)

        self._run_thread = threading.Thread(
            target=self._thread_run,
            args=(str(self.current_file),),
            daemon=True
        )
        self._run_thread.start()

    def _thread_run(self, path: str):
        capture = StdoutCapture(self.sig)
        try:
            import AsmBlur as asm_main
            with redirect_stdout(capture):
                asm_main.run_assembly(path)
            elapsed = time.time() - self.run_start_time
            self.sig.run_done.emit(elapsed)
        except ImportError:
            self.sig.run_error.emit("'main' module not found. Place AsmBlur.py alongside this script.")
        except Exception as e:
            self.sig.run_error.emit(str(e))

    def _stop_run(self):
        # Note: Python threads can't be forcibly killed.
        # We flip state and let the user know.
        if self.is_running:
            self.console.write_error("\n[STOP REQUESTED — thread will finish current instruction]\n")
            self._finalize_run(aborted=True)

    @Slot(str, str)
    def _on_output(self, text: str, color: str):
        self.console.append_colored(text, color)

    @Slot(float)
    def _on_run_done(self, elapsed: float):
        ts = f"[{datetime.now().strftime('%H:%M:%S')}]  " if self.show_timestamps else ""
        self.console.write_success(f"  {ts}■  Done  •  {elapsed:.3f}s\n")
        self._finalize_run()

    @Slot(str)
    def _on_run_error(self, msg: str):
        self.console.write_error(f"\n[ERROR] {msg}\n")
        self._finalize_run()

    def _finalize_run(self, aborted=False):
        self.is_running = False
        self.elapsed_timer.stop()
        self.elapsed_label.setText("")
        self.run_btn.setEnabled(self.current_file is not None)
        self.stop_btn.setEnabled(False)
        self.act_run.setEnabled(True)
        self.act_stop.setEnabled(False)
        self._update_statusbar("Aborted" if aborted else "Finished")

    def _tick_elapsed(self):
        elapsed = time.time() - self.run_start_time
        self.elapsed_label.setText(f"⏱  {elapsed:.1f}s")

    # ── Console helpers ───────────────────────
    def _clear_console(self):
        self.console.clear()
        self._update_statusbar("Console cleared")

    def _save_log(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Console Log", "console.log",
            "Log Files (*.log *.txt);;All Files (*)"
        )
        if path:
            try:
                Path(path).write_text(self.console.toPlainText(), encoding="utf-8")
                self._update_statusbar(f"Log saved: {path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    # ── Find ─────────────────────────────────
    def _show_find(self):
        if self.view_tabs.currentIndex() == 2:
            self.editor_find_bar.show_bar()
        else:
            self.view_tabs.setCurrentIndex(0)
            self.find_bar.show_bar()

    # ── File open helpers ─────────────────────
    def _open_programs_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Programs Folder", str(self.programs_dir))
        if path:
            self.programs_dir = Path(path)
            self._refresh_file_list()

    def _open_single_file(self):
        if not self._confirm_discard():
            return
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Assembly File", str(self.programs_dir),
            "Assembly Files (*.asm *.s *.S *.nasm *.nas);;All Files (*)"
        )
        if path:
            p = Path(path)
            self.current_file = p
            self._load_file(p)
            self.run_btn.setEnabled(True)
            self._update_statusbar(f"Opened: {p.name}")

    # ── Settings ─────────────────────────────
    def _open_settings(self):
        dlg = SettingsDialog(self, self.programs_dir)
        if dlg.exec():
            vals = dlg.get_values()
            self.programs_dir = Path(vals["programs_dir"])
            self.show_timestamps = vals["timestamps"]
            self.autoscroll = vals["autoscroll"]
            self._save_settings()
            self._refresh_file_list()

    def closeEvent(self, event):
        if self._confirm_discard():
            self._save_settings()  # ← add this
            event.accept()
        else:
            event.ignore()

    # ── File Stats ───────────────────────────
    def _show_file_stats(self):
        if not self.current_file:
            QMessageBox.information(self, "Stats", "No file loaded.")
            return
        self.view_tabs.setCurrentIndex(1)

    # ── Editor: dirty state ───────────────────
    def _set_dirty(self, dirty: bool):
        self._editor_dirty = dirty
        self.save_btn.setEnabled(dirty)
        self.act_save.setEnabled(dirty)
        if dirty:
            self.dirty_label.setText("● unsaved changes")
            self.view_tabs.setTabText(2, "Edit ●")
        else:
            self.dirty_label.setText("")
            self.view_tabs.setTabText(2, "Edit")

    def _on_editor_modified(self):
        if not self._editor_dirty:
            self._set_dirty(True)

    # ── Editor: save ─────────────────────────
    def _save_file(self):
        if not self.current_file:
            self._save_file_as()
            return
        try:
            text = self.text_editor.toPlainText()
            self.current_file.write_text(text, encoding="utf-8")
            # Sync read-only viewer
            self.code_editor.blockSignals(True)
            self.code_editor.setPlainText(text)
            self.code_editor.blockSignals(False)
            self._update_file_info(self.current_file, text)
            self._set_dirty(False)
            self._update_statusbar(f"Saved: {self.current_file.name}")
        except Exception as e:
            QMessageBox.critical(self, "Save Failed", str(e))

    def _save_file_as(self):
        start = str(self.current_file) if self.current_file else str(self.programs_dir)
        path, _ = QFileDialog.getSaveFileName(
            self, "Save As", start,
            "Assembly Files (*.asm *.s *.nasm);;All Files (*)"
        )
        if not path:
            return
        p = Path(path)
        try:
            text = self.text_editor.toPlainText()
            p.write_text(text, encoding="utf-8")
            self.current_file = p
            self.viewer_header.setText(str(p))
            self.code_editor.blockSignals(True)
            self.code_editor.setPlainText(text)
            self.code_editor.blockSignals(False)
            self._update_file_info(p, text)
            self._set_dirty(False)
            self._refresh_file_list()
            self._update_statusbar(f"Saved as: {p.name}")
        except Exception as e:
            QMessageBox.critical(self, "Save Failed", str(e))

    # ── Editor: revert ───────────────────────
    def _revert_file(self):
        if not self.current_file or not self.current_file.exists():
            return
        if self._editor_dirty:
            ans = QMessageBox.question(
                self, "Revert",
                f"Discard all changes to {self.current_file.name} and reload from disk?",
                QMessageBox.Yes | QMessageBox.Cancel,
                QMessageBox.Cancel
            )
            if ans != QMessageBox.Yes:
                return
        self._load_file(self.current_file)
        self._update_statusbar(f"Reverted: {self.current_file.name}")

    # ── Editor: new file ─────────────────────
    def _new_file(self):
        if not self._confirm_discard():
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "New Assembly File", str(self.programs_dir),
            "Assembly Files (*.asm *.s *.nasm);;All Files (*)"
        )
        if not path:
            return
        p = Path(path)

        if not p.parent.exists():
            QMessageBox.critical(self, "Error", f"Directory does not exist: {p.parent}")
            return

        self.current_file = p
        self.viewer_header.setText(str(p))
        self.text_editor.document().blockSignals(True)
        self.text_editor.setPlainText("")
        self.text_editor.document().blockSignals(False)
        self.code_editor.setPlainText("")
        self._set_dirty(False)
        self.run_btn.setEnabled(True)
        self.view_tabs.setCurrentIndex(2)
        self._refresh_file_list()
        self._update_statusbar(f"Created: {p.name}")

    # ── Unsaved-changes guard ─────────────────
    def _confirm_discard(self) -> bool:
        """Returns True if it's safe to proceed (saved / discarded / no changes)."""
        if not self._editor_dirty:
            return True
        name = self.current_file.name if self.current_file else "untitled"
        box = QMessageBox(self)
        box.setWindowTitle("Unsaved Changes")
        box.setIcon(QMessageBox.Warning)
        box.setText(f"<b>{name}</b> has unsaved changes.")
        box.setInformativeText("Save before continuing?")
        box.setStyleSheet(STYLESHEET)
        save_btn    = box.addButton("Save",    QMessageBox.AcceptRole)
        discard_btn = box.addButton("Discard", QMessageBox.DestructiveRole)
        cancel_btn  = box.addButton("Cancel",  QMessageBox.RejectRole)
        box.setDefaultButton(save_btn)
        box.exec()
        clicked = box.clickedButton()
        if clicked == save_btn:
            self._save_file()
            return not self._editor_dirty   # False if save was cancelled
        elif clicked == discard_btn:
            self._set_dirty(False)
            return True
        else:
            return False

    def closeEvent(self, event):
        if self._confirm_discard():
            event.accept()
        else:
            event.ignore()

    # ── Cursor position ───────────────────────
    def _update_cursor_pos(self):
        # Read from whichever editor is active
        active = self.text_editor if self.view_tabs.currentIndex() == 2 else self.code_editor
        cursor = active.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.line_col_label.setText(f"Ln {line}  Col {col}  ")

    # ── Status Bar ───────────────────────────
    def _update_statusbar(self, msg: str):
        self.status_label.setText(f"  {msg}")

    def _show_about(self):
        QMessageBox.about(
            self,
            "AsmStudio",
            "<b>AsmStudio</b><br>"
            "A polished GUI for browsing, inspecting, and running .asm examples.<br><br>"
            "Drop .asm files into the <code>examples/</code> folder to get started."
        )


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("AsmStudio")

    # On Windows, set app ID so the taskbar shows the right icon
    try:
        from ctypes import windll
        windll.shell32.SetCurrentProcessExplicitAppUserModelID("assemblyrunner.ide.1")
    except Exception:
        pass

    window = AssemblyRunnerIDE()
    window.show()
    sys.exit(app.exec())