import tkinter as tk
from tkinter import ttk, messagebox
from itertools import count
import os

# --- NEW: Import Pygame for music ---
try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False
    print("Warning: 'pygame' library not found. Music will not be played.")
    print("Please install it by running: pip install pygame")
# --- END OF NEW IMPORT ---


# Optional Pillow support
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# --- Animated GIF Loader (No changes) ---
class AnimatedGIF(tk.Label):
    def __init__(self, master, path, delay=100, bg="black", target_size=None):
        super().__init__(master, bg=bg)
        self.master = master
        self.delay = delay
        self.frames = []
        self.target_size = target_size
        
        if not path: # Handle if no path is given
            return
            
        if HAS_PIL:
            try:
                pil_img = Image.open(path)
                from PIL import ImageSequence
                for pil_frame in ImageSequence.Iterator(pil_img):
                    try:
                        frame_copy = pil_frame.copy()
                        try:
                            frame_conv = frame_copy.convert('RGBA')
                        except Exception:
                            frame_conv = frame_copy.convert('RGB')
                        if self.target_size is not None:
                            try:
                                frame_conv = frame_conv.resize(self.target_size, Image.LANCZOS)
                            except Exception:
                                pass
                        tk_frame = ImageTk.PhotoImage(frame_conv)
                        self.frames.append(tk_frame)
                    except Exception:
                        continue
            except Exception:
                self.frames = []

        if not self.frames:
            try:
                for i in count(0):
                    frame = tk.PhotoImage(file=path, format=f"gif -index {i}")
                    self.frames.append(frame)
            except tk.TclError:
                pass

        if not self.frames:
            try:
                # This will load a single frame for static images like PNG/JPG
                img = tk.PhotoImage(file=path)
                self.frames.append(img)
            except tk.TclError:
                self.frames = []

        if self.frames:
            self.index = 0
            self._current_image = self.frames[0]
            self.configure(image=self._current_image)
            try:
                print("AnimatedGIF: loaded", len(self.frames), "frames")
            except Exception:
                pass
            if len(self.frames) > 1:
                self.animate()

    def animate(self):
        if not self.frames:
            return
        self.index = (self.index + 1) % len(self.frames)
        self._current_image = self.frames[self.index]
        self.configure(image=self._current_image)
        self.after(self.delay, self.animate)


# --- Splash Screen (No changes) ---
class SplashScreen(tk.Toplevel):
    def __init__(self, parent, bg_path=None, gif_path=None):
        super().__init__(parent)
        self.title("Starting up...")
        self.geometry("500x450")
        self.configure(bg="black")
        self.overrideredirect(True)
        try:
            self.attributes("-topmost", True)
        except Exception:
            pass
        try:
            self.lift()
            self.focus_force()
        except Exception:
            pass

        self.update_idletasks()
        w, h = 500, 350
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = (sw // 2) - (w // 2), (sh // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

        try:
            self.attributes("-alpha", 0.0)
            self._fade = True
        except tk.TclError:
            self._fade = False

        self.bg_label = None
        gif_size = None
        
        # Check if gif_path is provided and valid
        if gif_path and os.path.exists(gif_path):
            try:
                if HAS_PIL:
                    pil = Image.open(gif_path)
                    gif_size = pil.size
                else:
                    tmp = tk.PhotoImage(file=gif_path)
                    gif_size = (tmp.width(), tmp.height())
            except Exception:
                gif_size = None
        else:
             # No image for splash, just show progress bar
             w, h = 400, 100
             x, y = (sw // 2) - (w // 2), (sh // 2) - (h // 2)
             self.geometry(f"{w}x{h}+{x}+{y}")
             self.progress = ttk.Progressbar(self, orient="horizontal", length=350, mode="determinate")
             self.progress.place(relx=0.5, rely=0.5, anchor="center")
             if self._fade: self.fade_in()
             self.loading_bar()
             return # Skip the rest of the image logic

        if gif_size:
            gw, gh = gif_size
            progress_height = 40
            max_w = int(self.winfo_screenwidth() * 0.5)
            max_h = int(self.winfo_screenheight() * 0.5)
            # --- Auto-size based on GIF dimensions ---
            # Use a slightly larger base height for this GIF
            target_h = min(gh + progress_height + 40, max_h) 
            scale = target_h / (gh + progress_height + 40) if (gh + progress_height + 40) > 0 else 1
            target_w = max(int(gw * scale), 200)
            
            if target_w < 300: target_w = 300 # Ensure it's wide enough
            if target_h < 250: target_h = 250 # Ensure it's tall enough
            
            w, h = target_w, target_h
            sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
            x, y = (sw // 2) - (w // 2), (sh // 2) - (h // 2)
            self.geometry(f"{w}x{h}+{x}+{y}")
        else:
            w, h = 500, 350
        
        # --- ANIMATION DATA ---
        # Start the image off-screen (rely = -0.5 is above the window)
        self.current_image_y = -0.5 
        self.target_image_y = 0.45 # Final position
        # --- END ANIMATION DATA ---

        if gif_path:
            target_size = None
            try:
                if gif_size:
                    gw, gh = gif_size
                    progress_height = 40
                    avail_h = h - progress_height - 20
                    scale = avail_h / gh if gh else 1.0
                    target_w = max(1, int(gw * scale))
                    target_h = max(1, int(gh * scale))
                    target_size = (target_w, target_h)
            except Exception:
                target_size = None
            
            # Use AnimatedGIF class, which supports static PNGs/GIFs
            self.gif = AnimatedGIF(self, gif_path, delay=80, bg="black", target_size=target_size)
            
            # Place the image at its STARTING off-screen position
            self.gif.place(relx=0.5, rely=self.current_image_y, anchor="center")

        self.progress = ttk.Progressbar(
            self, orient="horizontal", length=int(w * 0.8), mode="determinate"
        )
        self.progress.place(relx=0.5, rely=0.9, anchor="center")

        if self._fade:
            self.fade_in()
        self.loading_bar()

    def fade_in(self):
        alpha = self.attributes("-alpha")
        if alpha < 1:
            alpha += 0.05
            self.attributes("-alpha", alpha)
            self.after(50, self.fade_in)
        else:
            # When fade_in is done, start the slide animation
            self.attributes("-alpha", 1.0)
            self.animate_image_slide_in()

    def animate_image_slide_in(self):
        """Animates the image sliding in from the top with an ease-out effect."""
        
        distance = self.target_image_y - self.current_image_y
        
        if abs(distance) < 0.001:
            self.current_image_y = self.target_image_y
            self.gif.place(rely=self.current_image_y)
            return
            
        move_step = distance * 0.1
        self.current_image_y += move_step
        
        self.gif.place(rely=self.current_image_y)
        
        self.after(15, self.animate_image_slide_in) # 15ms for a smooth animation

    def loading_bar(self):
        val = self.progress["value"]
        if val < 100:
            self.progress["value"] = val + 2
            self.after(50, self.loading_bar)
        else:
            self.after(500, self.destroy)

#---- Importing gui_blkpink and tk_with_pics ----
try:
    from gui_blkpnk import LinkedListGUI
except ImportError:
    messagebox.showerror("Import Error", "Could not import LinkedListGUI from gui_blkpnk.py.")
    exit()
    
try:
    from tk_with_pics import AsciiStackApp
except ImportError:
    messagebox.showerror("Import Error", "Could not import AsciiStackApp from tk_with_pics.py.")
    exit()

# --- *** NEW IMPORT FOR RECURSION *** ---
try:
    # We need both the GUI class and the splash screen function from the other file
    from recursion1clone import RecursionGUI, create_splash_screen as create_recursion_splash
except ImportError:
    messagebox.showerror("Import Error", "Could not import from recursion1clone.py.")
    exit()
# --- *** END OF NEW IMPORT *** ---


# --- Main Application Window (MODIFIED) ---
class AppMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("GROUP 7 - DATA STRUCTURES VISUALIZER")
        self.root.geometry("500x500")
        
        # --- Define Colors (MODIFIED) ---
        self.BG_COLOR = "#FFC0CB"       # "pink"
        self.BTN_BG = "#FFFFFF"         # White, per target image
        self.BTN_FG = "#000000"         # Black text
        
        # --- MODIFICATION HERE: Darker pinks for hover/active ---
        self.BTN_HOVER_BG = "#FFB6C1"    # LightPink (darker than before)
        self.BTN_ACTIVE_BG = "#DB7093"   # PaleVioletRed (darker for click)
        # --- END OF MODIFICATION ---
        
        self.root.config(bg=self.BG_COLOR)
        self.center_window(800, 750)
        
        # --- Store main menu image path ---
        # This still points to splash_image.png for the main menu
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.splash_image_path = os.path.join(script_dir, "splash_image.png")
        if not os.path.exists(self.splash_image_path):
            print(f"Warning: 'splash_image.png' not found at {self.splash_image_path}.")
            self.splash_image_path = None # Set to None if not found
            
        # --- *** NEW: Initialize Pygame Mixer and set Music Path *** ---
        self.music_file = "Kill this love but lofi BLACKPINK lofi mix  chillhop beats to study_relax to.mp3"
        self.music_path = None
        global HAS_PYGAME # Use the global flag
        
        if HAS_PYGAME:
            try:
                pygame.mixer.init()
                self.music_path = os.path.join(script_dir, self.music_file)
                if not os.path.exists(self.music_path):
                    print(f"Warning: Music file not found: {self.music_path}")
                    self.music_path = None
            except Exception as e:
                print(f"Error initializing pygame.mixer: {e}")
                HAS_PYGAME = False # Disable music if init fails
        # --- *** END OF NEW MUSIC INIT *** ---
        
        self.style = ttk.Style()
        self.style.theme_use('default')
        
        # --- STYLING FIX (MODIFIED FOR "SHAPE") ---
        self.style.configure("MainMenu.TButton",
                             font=("Segoe UI", 18, "bold"),
                             padding=20,
                             background=self.BTN_BG,
                             foreground=self.BTN_FG,
                             # --- MODIFICATION HERE: Add border and relief ---
                             borderwidth=3,
                             relief="raised"
                             # --- END OF MODIFICATION ---
                             )
        
        self.style.map("MainMenu.TButton",
                       background=[
                           ('pressed', self.BTN_ACTIVE_BG),  # Color when clicked
                           ('active', self.BTN_HOVER_BG),   # Color when hovered
                           ('!disabled', self.BTN_BG)       # Default color
                       ],
                       foreground=[
                           ('!disabled', self.BTN_FG)       # Always black text
                       ],
                       # --- MODIFICATION HERE: Make non-pressed state "raised" ---
                       relief=[
                           ('pressed', 'sunken'),      # Sunken effect on click
                           ('!pressed', 'raised')      # "Raised" shape otherwise
                       ])
        # --- END OF STYLING FIX ---

        # --- *** NEW STYLE FOR THE EXIT BUTTON *** ---
        # It's the same as the main menu, but with less vertical padding
        self.style.configure("Exit.TButton",
                             font=("Segoe UI", 18, "bold"),
                             padding=(20, 10),  # (horizontal=20, vertical=10)
                             background=self.BTN_BG,
                             foreground=self.BTN_FG,
                             borderwidth=3,
                             relief="raised"
                             )
        
        self.style.map("Exit.TButton",
                       background=[
                           ('pressed', self.BTN_ACTIVE_BG),
                           ('active', self.BTN_HOVER_BG),
                           ('!disabled', self.BTN_BG)
                       ],
                       foreground=[
                           ('!disabled', self.BTN_FG)
                       ],
                       relief=[
                           ('pressed', 'sunken'),
                           ('!pressed', 'raised')
                       ])
        # --- *** END OF NEW STYLE *** ---
        
        self.main_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.main_frame.pack(expand=True, fill="both")

        self.create_main_menu()

    def center_window(self, width, height):
        """Centers the root window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_main_menu(self):
        """Creates the main menu buttons."""

        for widget in self.main_frame.winfo_children():
            widget.destroy() 
        
        self.main_frame.pack_configure(padx=40, pady=40)

        # --- Use hammer image for main menu ---
        target_size = (460, 210) 
        
        self.header_image = AnimatedGIF(
            self.main_frame, 
            self.splash_image_path, 
            bg=self.BG_COLOR, 
            target_size=target_size
        )
        self.header_image.pack(pady=(0, 30))
        # --- END OF MODIFICATION ---

        ttk.Button(self.main_frame, text="LINKED LISTS",
                   style="MainMenu.TButton",
                   width=30,  # Keep this for alignment
                   command=self.open_linked_list_gui
                   ).pack(pady=10) 

        ttk.Button(self.main_frame, text="STACKS",
                   style="MainMenu.TButton",
                   width=30,  # Keep this for alignment
                   command=self.open_stack_gui
                   ).pack(pady=10) 

        # --- *** MODIFIED BUTTON *** ---
        ttk.Button(self.main_frame, text="RECURSION",
                   style="MainMenu.TButton",
                   width=30,  # Keep this for alignment
                   command=self.open_recursion_gui # Changed from recursion_wip
                   ).pack(pady=10) 
        # --- *** END OF MODIFICATION *** ---

        ttk.Button(self.main_frame, text="EXIT",
                   style="MainMenu.TButton",
                   width=30,  # Keep this for alignment
                   command=self.show_credits_window
                   ).pack(pady=10)

    def open_app_window(self, app_class, title):
        """Opens a new application window."""
        self.root.withdraw()
        app_window = tk.Toplevel(self.root)
        app_window.title(title)
        
        app_instance = app_class(app_window)
        app_window.protocol("WM_DELETE_WINDOW",
                            lambda: self.close_app_window(app_window))

    def open_linked_list_gui(self): # Open Linked List GUI
        self.open_app_window(LinkedListGUI, "Linked List Visualizer")

    def close_app_window(self, app_window):
        """Closes the application window and returns to the main menu."""
        app_window.destroy()
        self.root.deiconify()
        self.root.lift() # Bring main menu to the front

    def open_stack_gui(self):  # Open Stack GUI
        self.open_app_window(AsciiStackApp, "Stack Visualizer")

    # --- *** NEW METHOD TO LAUNCH RECURSION APP WITH SPLASH *** ---
    def open_recursion_gui(self):
        """Opens the Recursion app with its custom splash screen."""
        self.root.withdraw()
        app_window = tk.Toplevel(self.root)
        app_window.withdraw() # Hide the app window initially
        
        # Create the splash screen *for* the new Toplevel window
        # This uses the imported 'create_recursion_splash' function
        splash = create_recursion_splash(app_window)
        
        def launch_app():
            splash.destroy()
            # Pass app_window (the Toplevel) as the 'root' for RecursionGUI
            app_instance = RecursionGUI(app_window) 
            # The RecursionGUI class sets its own title.
            app_window.deiconify() # Show the app window
        
        # Set the close protocol to use our main app's closer
        app_window.protocol("WM_DELETE_WINDOW",
                            lambda: self.close_app_window(app_window))
        
        # Launch the app after the splash screen's duration (3000ms)
        app_window.after(3000, launch_app)
    # --- *** END OF NEW METHOD *** ---

    # --- 'recursion_wip' method has been removed ---

    # --- *** NEW METHOD TO QUIT APP AND STOP MUSIC *** ---
    def quit_app(self):
        """Stops the music and exits the application."""
        global HAS_PYGAME
        if HAS_PYGAME:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload() # Unload the file
                pygame.mixer.quit()
            except Exception as e:
                print(f"Error stopping pygame: {e}")
        self.root.quit()
    # --- *** END OF NEW METHOD *** ---

    # --- *** NEW METHOD FOR IMAGE FADE-IN ANIMATION *** ---
    def fade_in_image(self, window, alpha):
        """Recursively fades in the credits image using PIL.Image.blend."""
        try:
            if alpha > 1.0:
                # Animation done, set final image
                self._final_credits_img = ImageTk.PhotoImage(self._credits_pil_img)
                self.credits_image_label.config(image=self._final_credits_img)
                self.credits_image_label.image = self._final_credits_img
                return

            # Blend the image
            blended_img = Image.blend(self._credits_bg_img, self._credits_pil_img, alpha)
            
            # Convert to PhotoImage
            self._tk_frame = ImageTk.PhotoImage(blended_img)
            
            # Update the label
            self.credits_image_label.config(image=self._tk_frame)
            self.credits_image_label.image = self._tk_frame # Keep reference
            
            # Schedule next step (0.04 * 25 steps = 1.0)
            new_alpha = alpha + 0.04 
            # Use the credits window for the 'after' call
            window.after(40, lambda: self.fade_in_image(window, new_alpha))
        
        except Exception as e:
            # If animation fails (e.g., window closed), just show final image
            try:
                self._final_credits_img = ImageTk.PhotoImage(self._credits_pil_img)
                self.credits_image_label.config(image=self._final_credits_img)
                self.credits_image_label.image = self._final_credits_img
            except Exception:
                pass # Failsafe
    # --- *** END OF NEW METHOD *** ---

    def show_credits_window(self):
        """Creates the 'ending credits' window for the developers."""
        self.root.withdraw()  # Hide the main menu

        credits_window = tk.Toplevel(self.root)
        credits_window.title("Developers")
        credits_window.config(bg=self.BG_COLOR)
        credits_window.resizable(False, False)

        # Center the window
        win_width = 800
        win_height = 700
        screen_width = credits_window.winfo_screenwidth()
        screen_height = credits_window.winfo_screenheight()
        x = (screen_width // 2) - (win_width // 2)
        y = (screen_height // 2) - (win_height // 2)
        credits_window.geometry(f"{win_width}x{win_height}+{x}+{y}")

        # --- MODIFICATION: Use self.quit_app to stop music ---
        credits_window.protocol("WM_DELETE_WINDOW", self.quit_app)

        # --- *** NEW: Play Music *** ---
        global HAS_PYGAME
        if HAS_PYGAME and self.music_path:
            try:
                pygame.mixer.music.load(self.music_path)
                pygame.mixer.music.play(loops=-1) # -1 loops indefinitely
            except Exception as e:
                print(f"Error playing music: {e}")
        # --- *** END OF MUSIC MODIFICATION *** ---

        # --- Image Placeholder ---
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # --- Use the group67.jpg image ---
        dev_image_path = os.path.join(script_dir, "group67.png") 

        # --- *** MODIFIED: IMAGE FADE-IN LOGIC *** ---
        target_size = (400, 400)
        
        global HAS_PIL
        if os.path.exists(dev_image_path) and HAS_PIL:
            try:
                # Load PIL images for blending
                self._credits_pil_img = Image.open(dev_image_path).resize(target_size, Image.LANCZOS).convert('RGB')
                self._credits_bg_img = Image.new('RGB', target_size, self.BG_COLOR)
                
                # Create label
                self.credits_image_label = tk.Label(credits_window, bg=self.BG_COLOR)
                
                # Create a blank first frame so it holds the space
                self._tk_frame = ImageTk.PhotoImage(self._credits_bg_img)
                self.credits_image_label.config(image=self._tk_frame)
                self.credits_image_label.image = self._tk_frame
                
                self.credits_image_label.pack(pady=(20, 10))
                
                # Start animation
                self.fade_in_image(credits_window, 0.0)
                
            except Exception as e:
                print(f"Error starting fade-in animation: {e}. Falling back.")
                # Fallback to just showing it statically
                dev_image = AnimatedGIF(credits_window, dev_image_path, bg=self.BG_COLOR, target_size=target_size)
                dev_image.pack(pady=(20, 10))
        
        elif os.path.exists(dev_image_path):
             # HAS_PIL is False, just show it normally without fade
            dev_image = AnimatedGIF(credits_window, dev_image_path, bg=self.BG_COLOR, target_size=target_size)
            dev_image.pack(pady=(20, 10))
            
        else:
            # Image doesn't exist, show placeholder
            placeholder = tk.Label(credits_window, text="", font=("Segoe UI", 14, "italic"),
                                   bg=self.BTN_BG, fg=self.BTN_FG, width=30, height=15, relief="solid", borderwidth=2)
            placeholder.pack(pady=(20, 10))
        # --- *** END OF IMAGE MODIFICATION *** ---


        # --- Developer Names ---
        names_text = "Art Lorence Veridiano - UI MAIN MENU & LINKED LISTS\nRalph Gabriel Lazaro - UI OF STACKS & RECURSION\nLuigie Lato - RECURSION PROGRAM & CREDITS\nTimothy John Ramos - STACKS PROGRAM"
        tk.Label(credits_window, text=names_text, font=("Segoe UI", 14, "bold"),
                 bg=self.BG_COLOR, fg=self.BTN_FG).pack(pady=10)

        # --- Exit Button (MODIFIED to use self.quit_app) ---
        ttk.Button(credits_window, text="End", style="Exit.TButton",
                   command=self.quit_app).pack(pady=(15, 20))


    # --- MODIFIED: start_with_splash (No changes from previous) ---
    def start_with_splash(self):
        # --- PATHS ARE NOW DYNAMIC ---
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # --- CHANGE: Point to the new GIF for the splash screen ---
        splash_gif_name = "blackpink-cheering.gif"
        splash_gif_path = os.path.join(script_dir, splash_gif_name)
        gif_path = None
        
        if os.path.exists(splash_gif_path):
            gif_path = splash_gif_path
        else:
            print(f"Warning: '{splash_gif_name}' not found at {splash_gif_path}.")
            # Fallback to the hammer image if the GIF is missing
            fallback_image = os.path.join(script_dir, "splash_image.png")
            if os.path.exists(fallback_image):
                gif_path = fallback_image
        
        # bg_path has been removed
        splash = SplashScreen(self.root, bg_path=None, gif_path=gif_path)
        self.root.wait_window(splash)
        
        self.root.deiconify()
    # --- END OF MODIFICATION ---

    #
    # --- The 'load_background' method has been deleted ---
    #


# --- Run the App (No changes) ---
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() # Hide window until splash is done

    app = AppMenu(root)
    app.start_with_splash() # This will show splash, then deiconify root
    root.mainloop()