import os
import sys
import tkinter as tk
from tkinter import font, messagebox
from typing import List, Optional, Tuple

try:
    from PIL import Image, ImageTk, ImageSequence
except Exception:
    Image = ImageTk = ImageSequence = None

try:
    import pygame
    pygame.mixer.init()
except Exception:
    pygame = None

try:
    import winsound
except Exception:
    winsound = None

DEFAULT_EXTS = ('.gif', '.jpg', '.png', '.jpeg', '.bmp')
MAX_STACK = 10
POPUP_MAX_SIZE = (360, 360)
WINDOW_BG = 'pink'
BOX_BG = 'pink'
BOX_BORDER = 'black'
BUTTON_BG = 'black'
BUTTON_FG = 'white'
BOX_HEIGHT = 38
BOX_SIDE_PAD = 6
MAX_CHARS = 36

SOUND_FILES = {
    'push': 'push',
    'pop': 'pop',
    'overflow': 'overflow',
    'peek': 'peek',
    'clear': 'clear',
    'invalid': 'invalid',
    'pop_invalid': 'pop_invalid',
    'peek_invalid': 'peek_invalid',
    'push_invalid': 'push_invalid',
    'clear_popup': 'clear_popup',
}

SOUND_VOLUME = 0.2

KEYWORD_DATA = {
    '67': ("'67'!", "You found 67!", '67', '67'),
    '1016': ("Leader", "You found art!", '1016', '1016'),
    '1001': ("Lem", "HUh? bat nandito ako?", '1001', '1001'),
    '0121': ("Timoth", "You found Tim!", '0121', '0121'),
    '1122': ("You found Lazaro!", "get lizarded", '1122', '1122'),
    '0623': ("luiging", "jarvis, prompt print 'hellow world' on javascript", '0623', '0623'),
}

def _script_dir() -> str:
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__) if '__file__' in globals() else os.getcwd()


def find_image(base_name: str, search_dirs: Optional[List[str]] = None) -> Optional[str]:
    if not search_dirs:
        search_dirs = [_script_dir(), os.getcwd()]
    for d in search_dirs:
        if not d:
            continue
        for ext in DEFAULT_EXTS:
            candidate = os.path.join(d, base_name + ext)
            if os.path.exists(candidate):
                return candidate
    return None


def _sound_path(name: str) -> Optional[str]:
    base = SOUND_FILES.get(name)
    if not base:
        base = name
    exts = ('.mp3', '.wav', '.ogg')

    for d in (_script_dir(), os.getcwd()):
        for ext in exts:
            p = os.path.join(d, base + ext)
            if os.path.exists(p):
                return p
    return None


def play_sound(name: str, loops: int = 0):
    path = _sound_path(name)
    if not path:
        return
    if pygame:
        try:
            snd = pygame.mixer.Sound(path)
            snd.set_volume(SOUND_VOLUME)
            snd.play(loops=loops)
            return
        except Exception:
            pass
    if winsound and sys.platform.startswith('win') and path.lower().endswith('.wav'):
        try:
            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass

class ImagePopup:
    def __init__(self, title: str, message: str, image_path: Optional[str], parent: Optional[tk.Widget] = None, max_size: Tuple[int, int] = POPUP_MAX_SIZE,
                 confirm: bool = False):
        self.title = title
        self.message = message
        self.image_path = image_path
        self.max_size = max_size
        self.confirm = confirm
        self.result = False
        self.parent = parent

        self.root = None
        self._label_img = None
        self._frames = [100]
        self._frame_index = 0
        self._after_id = None

        self._open_popup()

    def _open_popup(self):
        self.root = tk.Toplevel(self.parent)
        self.root.title(self.title)
        self.root.config(bg=WINDOW_BG)
        self.root.protocol("WM_DELETE_WINDOW", self._close)

        if self.image_path is None:
            tk.Label(self.root, text=self.message, bg=WINDOW_BG, fg='black', font=("Arial", 11, 'bold')).pack(padx=12, pady=(12, 8))
            if self.confirm:
                btn_frame = tk.Frame(self.root, bg=WINDOW_BG)
                btn_frame.pack(pady=(0, 12))
                tk.Button(btn_frame, text='Yes', width=10, command=self._on_yes, bg=BUTTON_BG, fg=BUTTON_FG).pack(side='left', padx=6)
                tk.Button(btn_frame, text='No', width=10, command=self._on_no, bg=BUTTON_BG, fg=BUTTON_FG).pack(side='left', padx=6)
            else:
                tk.Button(self.root, text='Close', command=self._close, bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=(0, 12))
            if self.confirm:
                try:
                    self.root.transient()
                    self.root.grab_set()
                    self.root.wait_window()
                except Exception:
                    pass
            return

        if Image is None:
            try:
                messagebox.showinfo(self.title, f"{self.message}\n(Image support not installed)")
            except Exception:
                pass
            try:
                self.root.destroy()
            except Exception:
                pass
            return

        try:
            img = Image.open(self.image_path)
        except Exception as e:
            tk.Label(self.root, text=f"Error loading image:\n{e}", fg='red', bg=WINDOW_BG).pack(padx=12, pady=12)
            tk.Button(self.root, text='Close', command=self._close, bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=(0, 12))
            return

        is_animated = getattr(img, "is_animated", False)
        if is_animated and ImageSequence is not None:
            self._frames = []
            try:
                for frame in ImageSequence.Iterator(img):
                    frame = frame.copy()
                    frame.thumbnail(self.max_size, Image.LANCZOS)
                    photo = ImageTk.PhotoImage(frame)
                    self._frames.append(photo)
            except Exception:
                img.thumbnail(self.max_size, Image.LANCZOS)
                self._frames = [ImageTk.PhotoImage(img)]
        else:
            try:
                img.thumbnail(self.max_size, Image.LANCZOS)
            except Exception:
                img.thumbnail(self.max_size)
            self._frames = [ImageTk.PhotoImage(img)]

        self._label_img = tk.Label(self.root, image=self._frames[0], bg=WINDOW_BG)
        self._label_img.image = self._frames[0]
        self._label_img.pack(padx=12, pady=(12, 6))

        tk.Label(self.root, text=self.message, bg=WINDOW_BG, fg='black', font=("Arial", 11, 'bold')).pack(padx=12, pady=(0, 8))
        if self.confirm:
            btn_frame = tk.Frame(self.root, bg=WINDOW_BG)
            btn_frame.pack(pady=(0, 12))
            tk.Button(btn_frame, text='Yes', width=10, command=self._on_yes, bg=BUTTON_BG, fg=BUTTON_FG).pack(side='left', padx=6)
            tk.Button(btn_frame, text='No', width=10, command=self._on_no, bg=BUTTON_BG, fg=BUTTON_FG).pack(side='left', padx=6)
        else:
            tk.Button(self.root, text='Close', command=self._close, bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=(0, 12))

        if len(self._frames) > 1:
            self._frame_index = 0
            self._animate()

        if self.confirm:
            try:
                self.root.transient()
                self.root.grab_set()
                self.root.wait_window()
            except Exception:
                pass

    def _animate(self):
        if not self.root or not self._frames:
            return
        self._frame_index = (self._frame_index + 1) % len(self._frames)
        f = self._frames[self._frame_index]
        try:
            self._label_img.config(image=f)
            self._label_img.image = f
        except Exception:
            pass
        self._after_id = self.root.after(100, self._animate)

    def _close(self):
        try:
            if self._after_id and self.root:
                self.root.after_cancel(self._after_id)
        except Exception:
            pass
        try:
            self.root.destroy()
        except Exception:
            pass

    def _on_yes(self):
        self.result = True
        self._close()

    def _on_no(self):
        self.result = False
        self._close()


def show_image_popup(title: str, message: str, image_path: Optional[str], parent: Optional[tk.Widget] = None, size: Tuple[int, int] = POPUP_MAX_SIZE, confirm: bool = False) -> Optional[bool]:
    p = ImagePopup(title, message, image_path, parent=parent, max_size=size, confirm=confirm)
    return p.result if confirm else None


class AsciiStackApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('Stack UI (GIF & Sound)')
        self.root.config(bg=WINDOW_BG)
        self.script_dir = _script_dir()
        self.stack: List[str] = []
        self._build_ui()
        self.update_info()
        self.draw()

    def _build_ui(self):
        top = tk.Frame(self.root, bg=WINDOW_BG)
        top.pack(padx=10, pady=10, fill='x')

        tk.Label(top, text='Value:', bg=WINDOW_BG).pack(side='left')
        self.entry = tk.Entry(top)
        self.entry.pack(side='left', fill='x', expand=True, padx=(6, 6))
        self.entry.bind('<Return>', lambda e: self.push())

        for (text, cmd) in (('Push', self.push), ('Pop', self.pop), ('Peek', self.peek), ('Clear', self.clear)):
            tk.Button(top, text=text, width=8, command=cmd, bg=BUTTON_BG, fg=BUTTON_FG).pack(side='left', padx=2)

        info = tk.Frame(self.root, bg=WINDOW_BG)
        info.pack(padx=10, pady=(0, 6), fill='x')

        tk.Label(info, text='Peek Result:', bg=WINDOW_BG, fg='black', font=("Arial", 10, 'bold')).pack(anchor='w')
        self.peek_label = tk.Label(info, text='(none)', bg='white', fg='black', width=45, anchor='w')
        self.peek_label.pack(anchor='w', pady=(2, 6))

        tk.Label(info, text='Stack Info:', bg=WINDOW_BG, fg='black', font=("Arial", 10, 'bold')).pack(anchor='w')
        self.info_label = tk.Label(info, text=f'Stacks: 0 / {MAX_STACK}', bg='white', fg='black', width=45, anchor='w')
        self.info_label.pack(anchor='w')

        self.stack_area = tk.Frame(self.root, bg=WINDOW_BG)
        self.stack_area.pack(padx=10, pady=(10, 12), fill='both')

        self.status = tk.Label(self.root, text='Ready', anchor='w', bg=WINDOW_BG)
        self.status.pack(fill='x', padx=10, pady=(0, 10))

        try:
            mono = font.nametofont('TkFixedFont')
            fam = mono.actual().get('family', 'Courier')
            size = mono.actual().get('size', 11)
        except Exception:
            fam, size = 'Courier', 11
        self.mono_font = font.Font(family=fam, size=size, weight='bold')

    def set_status(self, text: str):
        self.status.config(text=text)

    def _validate_digits(self, proposed: str) -> bool:
        if proposed == "":
            return True
        return proposed.isdigit()

    def update_info(self):
        count = len(self.stack)
        if count >= MAX_STACK:
            self.info_label.config(text='Overflow! Stack > 10', fg='red')
            candidate = find_image('overflow', [self.script_dir, os.getcwd()])
            if candidate:
                show_image_popup('Overflow', 'stack is full! stop', candidate, parent=self.root)
            else:
                messagebox.showwarning('Overflow', 'Stack is full! stop')
            play_sound('overflow')
        else:
            self.info_label.config(text=f'Stacks: {count} / {MAX_STACK}', fg='black')

    def _handle_keyword(self, word: str):
        key = word.lower()
        if key not in KEYWORD_DATA:
            return
        title, msg, filename, sound_name = KEYWORD_DATA[key]
        candidate = find_image(filename, [self.script_dir, os.getcwd()])
        if candidate:
            if sound_name:
                play_sound(sound_name)
            show_image_popup(title, msg, candidate, parent=self.root)
        else:
            self.set_status(f"Keyword '{key}' found but image missing.")
            print(f"Keyword '{key}' image missing.")

    def _show_alert(self, image_base: str, title: str, message: str, sound_name: Optional[str] = None):
        candidate = find_image(image_base, [self.script_dir, os.getcwd()])
        if candidate:
            show_image_popup(title, message, candidate, parent=self.root)
        else:
            try:
                messagebox.showinfo(title, message)
            except Exception:
                self.set_status(message)
        if sound_name:
            try:
                play_sound(sound_name)
            except Exception:
                pass

    def push(self):
        v = self.entry.get().strip()
        if not v:
            try:
                self._show_alert('push_invalid', 'Invalid push', 'Cant push nothing.', sound_name='push_invalid')
            except Exception:
                try:
                    self._show_alert('invalid', 'Invalid push', 'Cannot push empty value.', sound_name='invalid')
                except Exception:
                    self.set_status('Cannot push empty value.')
            return
        if not v.isdigit():
            try:
                self._show_alert('invalid', 'Invalid input', "Yea numbers only", sound_name='invalid')
            except Exception:
                self.set_status('Invalid input: non-numeric characters detected.')
            return
        if len(self.stack) >= MAX_STACK:
            self.set_status('Overflow! Cannot add more stacks.')
            self.update_info()
            return

        if len(v) > MAX_CHARS:
            v = v[:MAX_CHARS - 3] + '...'

        self.stack.append(v)
        try:
            self.entry.delete(0, tk.END)
        except Exception:
            try:
                self.entry.delete(0, 'end')
            except Exception:
                pass

        self.set_status(f'Pushed: {v}')
        self.update_info()
        self.draw()

        play_sound('push')
        self._handle_keyword(v)

    def pop(self):
        if not self.stack:
            self._show_alert('pop_invalid', 'Underflow', 'Pop failed: stack is empty.', sound_name='pop_invalid')
            return
        v = self.stack.pop()
        self.set_status(f'Popped: {v}')
        self.update_info()
        self.draw()
        play_sound('pop')

    def peek(self):
        if not self.stack:
            self._show_alert('peek_invalid', 'Peek empty', 'Peek: stack is empty.', sound_name='peek_invalid')
            self.peek_label.config(text='(empty)')
            return
        v = self.stack[-1]
        self.peek_label.config(text=v)
        self.set_status(f'Top: {v}')
        play_sound('peek')

    def clear(self):
        if not self.stack:
            self.set_status('Stack already empty.')
            return

        try:
            play_sound('clear_popup')
        except Exception:
            pass

        candidate = find_image('clear', [self.script_dir, os.getcwd()])

        if candidate and Image is not None:
            confirm = show_image_popup('Clear Stack?', 'Do you want to clear all items?', candidate, parent=self.root, confirm=True)
            if confirm:
                self.stack.clear()
                self.set_status('Stack cleared.')
                self.update_info()
                self.draw()
                self.peek_label.config(text='(none)')
                play_sound('clear')
            else:
                self.set_status('Clear cancelled.')
        else:
            if messagebox.askyesno('Clear stack', 'Clear all items from the stack?'):
                self.stack.clear()
                self.set_status('Stack cleared.')
                self.update_info()
                self.draw()
                self.peek_label.config(text='(none)')
                play_sound('clear')

    def draw(self):
        for c in self.stack_area.winfo_children():
            c.destroy()
        if not self.stack:
            self._draw_empty()
            return
        for idx, item in enumerate(reversed(self.stack)):
            self._draw_box(item, top=(idx == 0))

    def _draw_empty(self):
        outer = tk.Frame(self.stack_area, bg=BOX_BORDER, height=BOX_HEIGHT)
        outer.pack(anchor='w', pady=4, padx=(BOX_SIDE_PAD, 0))
        outer.pack_propagate(False)
        inner = tk.Frame(outer, bg=BOX_BG)
        inner.place(x=2, y=2, width=220, height=BOX_HEIGHT - 4)
        lbl = tk.Label(inner, text='[ empty stack :3 ]', bg=BOX_BG,
                       fg='black', anchor='w', padx=8, font=self.mono_font)
        lbl.pack(fill='both', expand=True)

    def _draw_box(self, text: str, top: bool = False):
        display_text = str(text)
        char_w = self.mono_font.measure('0') if hasattr(self.mono_font, 'measure') else 8
        target_chars = min(MAX_CHARS, max(12, len(display_text)))
        box_w = target_chars * char_w + 40
        outer = tk.Frame(self.stack_area, bg=BOX_BORDER, height=BOX_HEIGHT, width=box_w)
        outer.pack(anchor='w', pady=4, padx=(BOX_SIDE_PAD, 0))
        outer.pack_propagate(False)
        inner = tk.Frame(outer, bg=BOX_BG)
        inner.place(x=2, y=2, width=box_w - 4, height=BOX_HEIGHT - 4)
        lbl = tk.Label(inner, text=display_text, bg=BOX_BG,
                       fg='black', anchor='w', padx=8, font=self.mono_font, width=target_chars)
        lbl.pack(fill='both', expand=True)
        if top:
            top_font = font.Font(family=self.mono_font.actual().get('family', 'Courier'),
                                 size=max(self.mono_font.actual().get('size', 9) - 2, 8), weight='bold')
            top_lbl = tk.Label(inner, text='TOP', bg=BOX_BG, fg='black', font=top_font)
            top_lbl.place(relx=0.95, rely=0.5, anchor='e')


if __name__ == '__main__':
    root = tk.Tk()
    app = AsciiStackApp(root)
    root.mainloop()