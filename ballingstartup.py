import tkinter as tk
from tkinter import ttk
from itertools import count

# Optional Pillow support for JPEG and other formats not supported by
# Tk's PhotoImage (which commonly supports GIF/PNG). If Pillow is
# available we will use it to load background images.
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except Exception:
    HAS_PIL = False

# --- Animated GIF Loader ---
class AnimatedGIF(tk.Label):
    def __init__(self, master, path, delay=100, bg="black", target_size=None):
        super().__init__(master, bg=bg)
        self.master = master
        self.delay = delay
        self.frames = []
        self.target_size = target_size
        # Try to load frames using Pillow's ImageSequence for best
        # compatibility. If that fails or Pillow not available, fall back
        # to Tk's PhotoImage indexing.
        if HAS_PIL:
            try:
                pil_img = Image.open(path)
                from PIL import ImageSequence
                for pil_frame in ImageSequence.Iterator(pil_img):
                    try:
                        # Ensure we have a concrete image in memory
                        frame_copy = pil_frame.copy()
                        # Convert to a mode ImageTk can handle (RGBA preferred)
                        try:
                            frame_conv = frame_copy.convert('RGBA')
                        except Exception:
                            frame_conv = frame_copy.convert('RGB')
                        # If a target size is provided, resize while
                        # preserving aspect ratio
                        if self.target_size is not None:
                            try:
                                frame_conv = frame_conv.resize(self.target_size, Image.LANCZOS)
                            except Exception:
                                pass
                        tk_frame = ImageTk.PhotoImage(frame_conv)
                        self.frames.append(tk_frame)
                    except Exception:
                        # skip bad frames
                        continue
            except Exception:
                # PIL failed to read the GIF; fall back below
                self.frames = []

        if not self.frames:
            try:
                # Load all frames of the GIF using PhotoImage indexing
                for i in count(0):
                    frame = tk.PhotoImage(file=path, format=f"gif -index {i}")
                    self.frames.append(frame)
            except tk.TclError:
                pass  # no more frames

        self.index = 0
        # If no frames were loaded (bad path or unsupported GIF), try a
        # single-frame load so the label still shows something instead of
        # raising IndexError.
        if not self.frames:
            try:
                img = tk.PhotoImage(file=path)
                self.frames.append(img)
            except tk.TclError:
                # give up — keep an empty label
                self.frames = []

        if self.frames:
            self.index = 0
            # Keep a strong reference to the current image to prevent GC
            self._current_image = self.frames[0]
            self.configure(image=self._current_image)
            # Debug output so we can confirm frames were loaded
            try:
                print("AnimatedGIF: loaded", len(self.frames), "frames")
            except Exception:
                pass
            # Only animate if there are multiple frames
            if len(self.frames) > 1:
                self.animate()

    def animate(self):
        """Cycle through frames"""
        if not self.frames:
            return
        self.index = (self.index + 1) % len(self.frames)
        # update current image reference
        self._current_image = self.frames[self.index]
        self.configure(image=self._current_image)
        self.after(self.delay, self.animate)


# --- Splash Screen with Background + GIF ---
class SplashScreen(tk.Toplevel):
    def __init__(self, parent, bg_path=None, gif_path=None):
        super().__init__(parent)
        self.title("Starting up...")
        # default geometry; will be adjusted based on GIF aspect ratio
        self.geometry("500x350")
        self.configure(bg="black")
        self.overrideredirect(True)
        # Keep the splash above other windows so the GIF is visible
        try:
            self.attributes("-topmost", True)
        except Exception:
            pass
        try:
            self.lift()
            self.focus_force()
        except Exception:
            pass

        # --- Center window ---
        self.update_idletasks()
        w, h = 500, 350
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = (sw // 2) - (w // 2), (sh // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

        # --- Fade-in Support ---
        try:
            self.attributes("-alpha", 0.0)
            self._fade = True
        except tk.TclError:
            self._fade = False

        # NOTE: background is intentionally not shown on the splash.
        # The main window will display the background image (if any)
        # after the splash completes.
        self.bg_label = None

        # Determine GIF natural size so we can size the splash window
        gif_size = None
        if gif_path:
            try:
                if HAS_PIL:
                    pil = Image.open(gif_path)
                    gif_size = pil.size  # (width, height)
                else:
                    # fallback: try a single PhotoImage
                    tmp = tk.PhotoImage(file=gif_path)
                    gif_size = (tmp.width(), tmp.height())
            except Exception:
                gif_size = None

        # If we have a gif size, compute a window size that preserves
        # the GIF aspect ratio and leaves room at the bottom for the
        # progress bar.
        if gif_size:
            gw, gh = gif_size
            # reserve some vertical space for progress bar and padding
            progress_height = 40
            max_w = int(self.winfo_screenwidth() * 0.5)
            max_h = int(self.winfo_screenheight() * 0.5)
            # target height is gif height + progress area, but cap to
            # a reasonable fraction of the screen
            target_h = min(gh + progress_height, max_h)
            # scale width to keep aspect ratio
            scale = target_h / (gh + progress_height)
            target_w = max( int(gw * scale), 200 )
            # avoid zero or tiny sizes
            if target_w < 200:
                target_w = 200
            if target_h < 150:
                target_h = 150
            w, h = target_w, target_h
            # center
            sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
            x, y = (sw // 2) - (w // 2), (sh // 2) - (h // 2)
            self.geometry(f"{w}x{h}+{x}+{y}")
        else:
            # use defaults
            w, h = 500, 350

        # --- Animated GIF (logo or loader) ---
        if gif_path:
            # If we computed gif_size and the window size, request a
            # target size for the GIF frames that preserves aspect ratio
            # and fits comfortably within the window.
            target_size = None
            try:
                if gif_size:
                    gw, gh = gif_size
                    # compute available height for GIF (window height - progress)
                    progress_height = 40
                    avail_h = h - progress_height - 20
                    scale = avail_h / gh if gh else 1.0
                    target_w = max(1, int(gw * scale))
                    target_h = max(1, int(gh * scale))
                    target_size = (target_w, target_h)
            except Exception:
                target_size = None

            self.gif = AnimatedGIF(self, gif_path, delay=80, bg="black", target_size=target_size)
            # place the GIF roughly above the progress bar
            self.gif.place(relx=0.5, rely=0.45, anchor="center")

        # --- Progress bar ---
        self.progress = ttk.Progressbar(
            self, orient="horizontal", length=350, mode="determinate"
        )
        self.progress.place(relx=0.5, rely=0.9, anchor="center")

        # Start animations
        if self._fade:
            self.fade_in()
        self.loading_bar()

    def fade_in(self):
        alpha = self.attributes("-alpha")
        if alpha < 1:
            alpha += 0.05
            self.attributes("-alpha", alpha)
            self.after(50, self.fade_in)

    def loading_bar(self):
        val = self.progress["value"]
        if val < 100:
            self.progress["value"] = val + 2
            self.after(50, self.loading_bar)
        else:
            self.after(500, self.destroy)


# --- Main Application Window ---
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.title("Main App")
        self.geometry("600x400")
        self.configure(bg="#222")
        # placeholders for background handling
        self._bg_img = None
        self._bg_label = None

        tk.Label(
            self,
            text="Main Application Loaded ✅",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#222"
        ).pack(expand=True)

    def start_with_splash(self):
        # 👇 PUT YOUR IMAGE FILE PATHS HERE 👇
        bg_path = r"C:\Users\Arlo\Downloads\python prac\data_struc\GUI\blkpnk\bg.jpg"   # background image (optional)
        gif_path = r"C:\Users\Arlo\Downloads\python prac\data_struc\GUI\blkpnk\startup.gif"     # your animated gif (required)
        # Splash no longer shows background; only pass the gif.
        splash = SplashScreen(self, bg_path=None, gif_path=gif_path)
        self.wait_window(splash)
        # After splash finishes, load background onto the main window.
        if bg_path:
            self.load_background(bg_path)
        self.deiconify()

    def load_background(self, path):
        """Load a background image into the main window.

        Uses Pillow (ImageTk) when available to support JPEG and other
        formats. Falls back to Tk's PhotoImage for GIF/PNG. If loading
        fails, the function will silently skip the background.
        """
        # remove existing background if present
        if self._bg_label is not None:
            try:
                self._bg_label.destroy()
            except Exception:
                pass
            self._bg_label = None
            self._bg_img = None

        loaded = False
        if HAS_PIL:
            try:
                pil = Image.open(path)
                # Resize to window size while keeping aspect ratio? For
                # now just use the image as-is.
                self._bg_img = ImageTk.PhotoImage(pil)
                loaded = True
            except Exception:
                self._bg_img = None

        if not loaded:
            try:
                self._bg_img = tk.PhotoImage(file=path)
                loaded = True
            except Exception:
                self._bg_img = None

        if loaded and self._bg_img is not None:
            # place background label behind other widgets
            self._bg_label = tk.Label(self, image=self._bg_img)
            self._bg_label.place(relx=0.5, rely=0.5, anchor="center")
            # Lower it so content is visible
            try:
                self._bg_label.lower()
            except Exception:
                pass


# --- Run the App ---
if __name__ == "__main__":
    app = MainApp()
    app.start_with_splash()
    app.mainloop()