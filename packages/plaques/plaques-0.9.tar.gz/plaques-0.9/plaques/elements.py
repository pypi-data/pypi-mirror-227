"""More advanced UI elements."""

import os, sys, termios, tty, fcntl, time
from enum import Enum
from .base import CharCell, Plaque, Color, Pivot
globals().update(Color.__members__)
globals().update(Pivot.__members__)


class _Word():
    """Information unit for Text that renders into a list of CharCells."""
    def __init__(self, word):
        self.word = word

    def render(self):
        return [CharCell(char = _char, color = TRANSPARENT, bgcol = TRANSPARENT)
            for _char in self.word]

    def __len__(self):
        """Return displayed length of text."""
        return len(self.word)


class Text(Plaque):
    """Caption box element."""

    DEFAULTS = Plaque.DEFAULTS | {
        "text": "",
        "align": CENTER_CENTER,
        "fill": CharCell(color = TRANSPARENT, bgcol = TRANSPARENT)
    }
    
    def get_char_table(self, h_size: int, v_size: int
        ) -> list[list[CharCell]]:
        """Get a canvas of right size and render the words."""
        canvas = [
            [self.fill.copy() for _i in range(h_size)]
            for _j in range(v_size)
            ]
        if self.text == "":
            return canvas
        ### Break text into separate words ###
        words = []
        for _word in self.text.split(" "):
            words.append(_Word(_word))
        ### Get CharCell lines ###
        lines = []
        current_h_pos = current_v_pos = 0
        current_line = []
        _SPACE = CharCell(char = " ", color = TRANSPARENT, bgcol = TRANSPARENT)
        for _word in words:
            if current_h_pos >= h_size: #ran out of horizontal space
                if current_line[-1].char == " ":
                    current_line = current_line[:-1] #remove trailing space
                lines.append(current_line)
                current_line = []
                current_v_pos += 1
                current_h_pos = 0
                if current_v_pos >= v_size:
                    break #ran out of vertical space
            if (current_h_pos + len(_word) < h_size or not current_line
                or current_v_pos == v_size - 1):
                #can fit the current word or, if not, a line break won't help
                #or running out of vertical space
                current_line += (_word.render() + [_SPACE.copy()])
                current_h_pos = current_h_pos + len(_word) + 1
            else:
                if current_line[-1].char == " ":
                    current_line = current_line[:-1] #remove trailing space
                lines.append(current_line)
                current_line = _word.render() + [_SPACE.copy()]
                current_v_pos += 1
                current_h_pos = len(_word) + 1
        if current_line:
            if current_line[-1].char == " ":
                current_line = current_line[:-1] #remove trailing space
            lines.append(current_line)
        ### Place the rendered lines on the canvas according to align value ###
        v_shift = max(round(self.align.v_shift() * (v_size - len(lines))), 0)
        for line in range(len(lines)):
            h_shift = max(round(self.align.h_shift() 
                * (h_size - len(lines[line]))), 0)
            for cell in range(len(lines[line])):
                _v = line + v_shift
                _h = cell + h_shift
                try:
                    canvas[_v][_h] = canvas[_v][_h].overlay(lines[line][cell])
                except IndexError:
                    pass
        return canvas


class Frame(Enum):
    """Possible border styles for Window."""

    NO_FRAME = {
           TOP_LEFT: " ",    TOP_CENTER: " ",    TOP_RIGHT: " ",
        CENTER_LEFT: " ",                     CENTER_RIGHT: " ",
        BOTTOM_LEFT: " ", BOTTOM_CENTER: " ", BOTTOM_RIGHT: " ",
        }
    THIN = {
           TOP_LEFT: "┌",    TOP_CENTER: "─",    TOP_RIGHT: "┐",
        CENTER_LEFT: "│",                     CENTER_RIGHT: "│",
        BOTTOM_LEFT: "└", BOTTOM_CENTER: "─", BOTTOM_RIGHT: "┘",
        }
    THICK = {
           TOP_LEFT: "┏",    TOP_CENTER: "━",    TOP_RIGHT: "┓",
        CENTER_LEFT: "┃",                     CENTER_RIGHT: "┃",
        BOTTOM_LEFT: "┗", BOTTOM_CENTER: "━", BOTTOM_RIGHT: "┛",
        }
    DOUBLE = {
           TOP_LEFT: "╔",    TOP_CENTER: "═",    TOP_RIGHT: "╗",
        CENTER_LEFT: "║",                     CENTER_RIGHT: "║",
        BOTTOM_LEFT: "╚", BOTTOM_CENTER: "═", BOTTOM_RIGHT: "╝",
        }
    SMOOTH = {
           TOP_LEFT: "╭",    TOP_CENTER: "─",    TOP_RIGHT: "╮",
        CENTER_LEFT: "│",                     CENTER_RIGHT: "│",
        BOTTOM_LEFT: "╰", BOTTOM_CENTER: "─", BOTTOM_RIGHT: "╯",
        }
    OUTER_HALF = {
           TOP_LEFT: "▛",    TOP_CENTER: "▀",    TOP_RIGHT: "▜",
        CENTER_LEFT: "▌",                     CENTER_RIGHT: "▐",
        BOTTOM_LEFT: "▙", BOTTOM_CENTER: "▄", BOTTOM_RIGHT: "▟",
        }
    INNER_HALF = {
           TOP_LEFT: "▗",    TOP_CENTER: "▄",    TOP_RIGHT: "▖",
        CENTER_LEFT: "▐",                     CENTER_RIGHT: "▌",
        BOTTOM_LEFT: "▝", BOTTOM_CENTER: "▀", BOTTOM_RIGHT: "▘",
        }
    ASCII = {
           TOP_LEFT: "+",    TOP_CENTER: "-",    TOP_RIGHT: "+",
        CENTER_LEFT: "|",                     CENTER_RIGHT: "|",
        BOTTOM_LEFT: "+", BOTTOM_CENTER: "-", BOTTOM_RIGHT: "+",
        }
    SLC_OUTER = { # Unicode 13+ required!
           TOP_LEFT: "🭽",    TOP_CENTER: "▔",    TOP_RIGHT: "🭾",
        CENTER_LEFT: "▏",                     CENTER_RIGHT: "▕",
        BOTTOM_LEFT: "🭼", BOTTOM_CENTER: "▁", BOTTOM_RIGHT: "🭿",
        }

globals().update(Frame.__members__)


class Window(Plaque):
    """Groups other UI elements in a frame."""

    DEFAULTS = Plaque.DEFAULTS | {
        "title": Text(
            pivot = TOP_LEFT,
            h_abs_pos = 1,
            v_abs_size = 1,
            h_rel_size = 1.0,
            h_abs_size = -2,
            fill = CharCell(color = TRANSPARENT, bgcol = TRANSPARENT),
            ),
        "status": Text(
            pivot = BOTTOM_LEFT,
            h_abs_pos = 1,
            v_rel_pos = 1.0,
            v_abs_pos = 0,
            v_abs_size = 1,
            h_rel_size = 1.0,
            h_abs_size = -2,
            fill = CharCell(color = TRANSPARENT, bgcol = TRANSPARENT),
            ),
        "frame": Frame.THIN,
    }

    BORDER = {
        "top": 1,
        "right": 1,
        "bottom": 1,
        "left": 1,
    }

    DEFAULT_ELEMENTS = ["title", "status"]

    def get_char_table(self, h_size: int, v_size: int
        ) -> list[list[CharCell]]:
        """Get a canvas of right size with frame."""
        canvas = [
            [self.fill.copy() for _i in range(h_size)]
            for _j in range(v_size)
            ]
        canvas[0][0].char = self.frame.value[TOP_LEFT]
        for _i in range(h_size - 2):
            canvas[0][_i + 1].char = self.frame.value[TOP_CENTER]
        canvas[0][-1].char = self.frame.value[TOP_RIGHT]
        for _i in range(v_size - 2):
            canvas[_i + 1][-1].char = self.frame.value[CENTER_RIGHT]
        canvas[-1][-1].char = self.frame.value[BOTTOM_RIGHT]
        for _i in range(h_size - 2):
            canvas[-1][_i + 1].char = self.frame.value[BOTTOM_CENTER]
        canvas[-1][0].char = self.frame.value[BOTTOM_LEFT]
        for _i in range(v_size - 2):
            canvas[_i + 1][0].char = self.frame.value[CENTER_LEFT]
        return canvas


class Screen(Plaque):
    """Takes care of proper interactive TUI operations.

    Screen is a context manager. The context does the following:
    * Enable alternative screen buffer;
    * Hide the cursor;
    * Switch terminal to raw mode;
    * Set non-blocking input;
    * Set terminal title (not every terminal emulator supports this).
    """

    DEFAULTS = Plaque.DEFAULTS | {
        "title": "",
        "h_rel_size": 1.0,
        "v_rel_size": 1.0,
    }

    def __enter__(self):
        """Modify terminal behavior for TUI."""
        self.file_descriptor = sys.stdin.fileno()
        self.old_fd_settings = termios.tcgetattr(self.file_descriptor)
        tty.setraw(self.file_descriptor)
        # Switch terminal to raw mode
        fcntl.fcntl(self.file_descriptor, fcntl.F_SETFL,
            fcntl.fcntl(self.file_descriptor, fcntl.F_GETFL) | os.O_NONBLOCK)
        # Set non-blocking input
        sys.stdout.write("\033[?1049h") # Enable alternative buffer
        sys.stdout.write("\033[?25l") # Hide cursor
        sys.stdout.write(f"\033]2;{self.title}\a") # Set terminal window title
        sys.stdout.flush()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Restore the the normal terminal behavior."""
        sys.stdout.write("\033]2\a") # Clear the title
        sys.stdout.write("\033[?25h") # Show cursor
        sys.stdout.write("\033[?1049l") # Disable alternative buffer
        sys.stdout.flush()
        fcntl.fcntl(self.file_descriptor, fcntl.F_SETFL,
            fcntl.fcntl(self.file_descriptor, fcntl.F_GETFL) - os.O_NONBLOCK)
        # Set blocking input
        termios.tcsetattr(self.file_descriptor, termios.TCSADRAIN,
            self.old_fd_settings)
        # Switch terminal to normal mode

    def refresh(self):
        """Print changed areas."""
        #TODO: actually calculate deltas
        h_avail, v_avail = os.get_terminal_size()
        lines, _, _ = self.render(h_avail, v_avail)
        for line in range(v_avail):
            try:
                sys.stdout.write(f"\033[{line + 1};0H"
                    + self.ansi_char_line(lines[line]))
            except BlockingIOError:
                line -= 1
                time.sleep(0.05)
        while True:
            try:
                sys.stdout.flush()
                break
            except BlockingIOError:
                time.sleep(0.05)

    def getkey(self):
        """Return pressed key."""
        return sys.stdin.read(1)
        # TODO: support keys that return longer sequences
