import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial
import random
from PIL import Image, ImageTk
import pygame
 
class RecursionDemo:
    def __init__(self):
        self.MONTHS = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

    def head_recursion_attendance(self, students, idx=0, present=None, trace=None):
        """Calling Attendance (head-recursion style).
        The teacher asks the first student, who asks the next, and so on.
        Once the last student is reached, they say "Present!", and the calls
        return back to the teacher.
        Returns (present_list, trace_list).
        """
        if present is None:
            present = []
        if trace is None:
            trace = []
        if idx == 0:
            students = [name.strip().title() for name in students]

        if idx >= len(students):
            trace.append("Last student reached. Now reporting back.")
            return present, trace

        # head recursion: delegate to the next student first
        present, trace = self.head_recursion_attendance(students, idx + 1, present, trace)
        name = students[idx]
        trace.append(f"{name} says: Present!")
        present.append(name)
        return present, trace

class RecursionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Recursion Visualizer - Mafia Debt Game & Attendance")
        self.root.geometry("850x600")
        self.root.configure(bg="#ffc0cb")  # Pink color

        self.demo = RecursionDemo()
        self.animation_after_id = None
        self.debt_game_state = None
        self.debt_game_after_id = None
        self.gif_frames = []
        self.gif_animation_after_id = None
        self.result_gif_frames = []
        self.result_gif_animation_id = None
        self.result_frame = None # Frame to hold GIF and text
        self.image_photo = None # To hold a reference to the image

        # Initialize pygame for sound effects
        # Default sample rate is often 44100. We use 1.5x that for faster playback.
        # If sounds are distorted, the original files might have a different sample rate (e.g., 22050).
        # In that case, you would use 22050 * 1.5 = 33075.
        pygame.mixer.init(frequency=33075)
        self.setup_gui()

    def setup_gui(self):
        title = tk.Label(self.root, text="Recursion Demos: Mafia Debt Game & Attendance",
                         font=("Helvetica", 22, "bold"), bg="#ffc0cb", fg="black")
        title.pack(pady=16)

        # Debt payoff game (Simulated Tail Recursion)
        debt_frame = tk.LabelFrame(self.root, text="💰 Tail Recursion Debt Game 💰",
                                     bg="#ffc0cb", fg="black", font=("Arial", 12, "bold"), padx=10, pady=6)
        debt_frame.pack(fill="x", padx=20, pady=8)

        # Left: image slot (placeholder) -- user can set image later
        # use a Canvas so we can control exact pixel size (square)
        slot_size = 180
        self.debt_image_slot = tk.Canvas(debt_frame, width=slot_size, height=slot_size,
                                        bg="white", relief="ridge", bd=2, highlightthickness=0)
        # placeholder text centered in the square
        self.debt_image_slot.create_text(slot_size//2, slot_size//2,
                                         text="Image slot\n(put image here later)",
                                         font=("Arial", 10), fill="gray", justify="center", tags=("placeholder",))
        self.debt_image_slot.pack(side="left", padx=10, pady=5)
        # keep a reference container for the image and canvas image id
        self.debt_image = None
        self.debt_image_id = None

        # try to load provided image into the slot (falls back silently if missing)
        self._load_slot_image(r"recursiontest.py\yakuzamafia.jpg")

        # Right: info and controls packed into a sub-frame for neat layout
        debt_right = tk.Frame(debt_frame, bg="#ffc0cb")
        debt_right.pack(side="left", fill="both", expand=True, padx=(8,0))

        # Info labels
        self.debt_info_label = tk.Label(debt_right, text="Your debt: ₱0\nMonths to pay: 0",
                                        font=("Arial", 12), fg="black", bg="#ffc0cb")
        self.debt_info_label.pack(pady=5, anchor="w")

        tk.Label(debt_right, text="Enter your monthly payment:",
                 font=("Arial", 11), fg="black", bg="#ffc0cb").pack(anchor="w")

        self.debt_payment_entry = tk.Entry(debt_right, font=("Arial", 12), justify="center")
        self.debt_payment_entry.pack(pady=5, anchor="w")
 
        # Buttons Frame
        debt_btn_frame = tk.Frame(debt_frame, bg="#ffc0cb")
        debt_btn_frame.pack(pady=5)
 
        self.debt_play_btn = tk.Button(debt_btn_frame, text="Pay Off Debt!", command=self.play_debt_game,
                                       font=("Arial", 12, "bold"), bg="#35BB00", fg="white", width=15)
        self.debt_play_btn.pack(side="left", padx=5)
 
        self.debt_reset_btn = tk.Button(debt_btn_frame, text="Reset Game", command=self.reset_debt_game,
                                        font=("Arial", 11), bg="#FF6347", fg="white", width=15)
        self.debt_reset_btn.pack(side="left", padx=5)
 
        # Progress bar
        self.debt_progress = ttk.Progressbar(debt_frame, orient="horizontal", length=300, mode="determinate")
        self.debt_progress.pack(pady=5)
        self.debt_progress_label = tk.Label(debt_frame, text="", fg="black", bg="#ffc0cb", font=("Arial", 10))
        self.debt_progress_label.pack(pady=2)
 
        self.debt_result_label = tk.Label(debt_frame, text="", font=("Arial", 12), fg="black", bg="#ffc0cb")
        self.debt_result_label.pack(pady=5)
 
        # Unpacking input
        attend_head_frame = tk.LabelFrame(self.root, text="Calling Attendance (Head Recursion)",
                                  bg="#ffc0cb", fg="black", font=("Helvetica", 10, "bold"), padx=10, pady=6)
        attend_head_frame.pack(fill="x", padx=20, pady=8)
 
        # Prototype Button
        prototype_frame = tk.Frame(attend_head_frame, bg="#ffc0cb")
        prototype_frame.pack(fill="x", pady=4)
        tk.Label(prototype_frame, text="Students (comma-separated, in order):", bg="#ffc0cb", fg="black").pack(side="left", anchor="w")
        ttk.Button(prototype_frame, text="Prototype (WIP)", state="disabled").pack(side="right")
 
        self.students_head_var = tk.StringVar(value="")  # Empty default value
        self.students_head_entry = ttk.Entry(attend_head_frame, textvariable=self.students_head_var, width=80)
        # Placeholder text and logic removed as requested
        self.students_head_entry.pack(fill="x", pady=6)
 
        btn_box_frame = tk.Frame(attend_head_frame, bg="#ffc0cb")
        btn_box_frame.pack(fill="x", pady=4)
        ttk.Button(btn_box_frame, text="Run Attendance (Head Recursion)",
                   command=self.run_head_recursion).pack(side="left", padx=(0, 8))
        ttk.Button(btn_box_frame, text="Clear Log",
                   command=partial(self.clear_output, reset_game=False)).pack(side="left")
 
        # Output area
        out_frame = tk.Frame(self.root, bg="#ffc0cb")
        out_frame.pack(fill="both", expand=True, padx=20, pady=12)
 
        self.output_text = tk.Text(out_frame, height=18, bg="white", fg="black", font=("Courier", 10))
        self.output_text.pack(side="top", fill="both", expand=True)
 
        # Add a label to hold the image, initially empty
        self.image_label = tk.Label(out_frame, bg="white")
        self.image_label.pack(side="bottom", pady=5)
 
        # Clear button at bottom (also cancels animation)
        bottom_frame = tk.Frame(self.root, bg="#ffc0cb")
        bottom_frame.pack(fill="x", padx=20, pady=(0, 6))
        ttk.Button(bottom_frame, text="Clear Output", command=partial(self.clear_output, reset_game=True)).pack(side="right")
 
        # Initialize game values last (after UI is built)
        self.reset_debt_game(init=True)
 
    def parse_list(self, raw):
        # Update parse_list to handle case consistency
        items = [s.strip().title() if ',' in raw else s.strip() for s in raw.split(",") if s.strip()]
        return items
 
    def _prepare_lines(self, trace_list):
        # flatten any embedded newlines into separate lines
        lines = []
        for item in trace_list:
            parts = item.split("\n")
            for p in parts:
                lines.append(p)
        return lines
 
    def update_output(self, title, trace_list):
        """Start animated display of title + trace_list (word-by-word, 0.2s)."""
        # Cancel any running animation
        if self.animation_after_id:
            try:
                self.root.after_cancel(self.animation_after_id)
            except Exception:
                pass
            self.animation_after_id = None
 
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        # Insert title and separator immediately
        self.output_text.insert(tk.END, f"{title}\n{'='*60}\n")
        # Prepare lines to animate and start animation
        lines = self._prepare_lines(trace_list)
        # if first line is empty, keep it to create spacing
        self._animate_lines(lines, 0, 0)
        self.output_text.config(state="disabled")
 
    def _animate_lines(self, lines, line_idx, word_idx):
        """Animate lines word-by-word into the text widget. 0.3s delay per word."""
        # Make sure widget writable temporarily
        self.output_text.config(state="normal")
 
        if line_idx >= len(lines):
            self.animation_after_id = None
            self.output_text.config(state="disabled")
            return
 
        line = lines[line_idx]
        # split preserving empty line
        words = line.split(' ') if line != "" else []
        # Insert next word or move to next line
        if word_idx < len(words):
            prefix = "" if word_idx == 0 else " "
            self.output_text.insert(tk.END, prefix + words[word_idx])
            # Schedule next word (0.3s)
            self.animation_after_id = self.root.after(300, lambda: self._animate_lines(lines, line_idx, word_idx + 1))
        else:
            # finished this line -> insert newline and proceed
            self.output_text.insert(tk.END, "\n")
            # Schedule next line (0.3s)
            self.animation_after_id = self.root.after(300, lambda: self._animate_lines(lines, line_idx + 1, 0))
 
        self.output_text.see(tk.END)
        self.output_text.config(state="disabled")
 
    def clear_output(self, reset_game=True):
        """Clear the central log/output area and cancel any running animation."""
        if self.animation_after_id:
            try:
                self.root.after_cancel(self.animation_after_id)
            except Exception:
                pass
            self.animation_after_id = None
 
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")
 
        if reset_game:
            self.reset_debt_game()
 
    # --- New Debt Game Logic ---
    def play_debt_game(self):
        # Easter Egg check for "67"
        if self.debt_payment_entry.get().strip() == "67":
            self._load_slot_image(r"recursiontest.py\scp-067-67.gif")
        else:
            self._load_slot_image(r"recursiontest.py\yakuzamafia.jpg")

        try:
            # Using a relative path that should work if the script is run from the parent directory
            pygame.mixer.music.load(r"recursiontest.py\Cha-Ching Sound Effect.mp3")
            pygame.mixer.music.play()
        except pygame.error:
            pass # Silently ignore if the sound file is missing

        try:
            payment = int(self.debt_payment_entry.get())
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid whole number.")
            return
 
        self.debt_game_state["payment"] = payment
        self.debt_play_btn.config(state="disabled")
        self.debt_result_label.config(text="")
        self.debt_progress["maximum"] = self.debt_game_state["months"]
        self.debt_progress["value"] = 0
        self.debt_game_state["current_month"] = 1
        self.debt_game_state["remaining_debt"] = self.debt_game_state["debt"]
 
        self.update_debt_progress()
 
    def update_debt_progress(self):
        state = self.debt_game_state
        if state["current_month"] > state["months"]:
            self.show_debt_result()
            return
 
        # Update GUI progress
        self.debt_progress["value"] = state["current_month"] - 1
        self.debt_progress_label.config(
            text=f"Month {state['current_month']} - Remaining debt: ₱{max(state['remaining_debt'], 0):,}"
        )
        self.root.update_idletasks()
 
        # Tail recursion step (simulated with after)
        state["remaining_debt"] -= state["payment"]
        state["current_month"] += 1
 
        # Schedule next recursion step
        self.debt_game_after_id = self.root.after(400, self.update_debt_progress)
 
    def show_debt_result(self):
        state = self.debt_game_state
        self.debt_progress["value"] = state["months"]
        self.debt_progress_label.config(text=f"Final debt: ₱{state['remaining_debt']:,}")
 
        # Accept ±₱5 margin as win
        result_text = "" # This will be cleared from the main GUI
        if abs(state['remaining_debt']) <= 5:
            color = "#00FF7F"
            popup_message = f"Final debt: ₱{state['remaining_debt']:,} and YOU WIN!\nDebt cleared within ₱5 margin."
            self.show_result_gif(r"recursiontest.py\win.gif", popup_message, color)
        elif state['remaining_debt'] < -5:
            color = "#FF4500"
            popup_message = f"YOU LOSE!\nYou overpaid by ₱{abs(state['remaining_debt']):,}"
            self.show_result_gif(r"recursiontest.py\lose.gif", popup_message, color)
        else:
            color = "#FF4500"
            popup_message = f"YOU LOSE!\nYou still owe ₱{state['remaining_debt']:,}"
            self.show_result_gif(r"recursiontest.py\lose.gif", popup_message, color)
 
        self.debt_result_label.config(text=result_text, fg=color)
        self.debt_play_btn.config(state="normal")
        if abs(state['remaining_debt']) > 5:  # if not a win
            try:
                pygame.mixer.music.load("fail.wav")
                pygame.mixer.music.play()
            except pygame.error:
                pass  # Silently ignore if the sound file is missing
 
    def reset_debt_game(self, init=False):
        if not init:
            try:
                pygame.mixer.music.load("recursiontest.py\Impact Laser - Free Sound Effect-[AudioTrimmer.com].mp3")
                pygame.mixer.music.play()
            except pygame.error:
                pass # Ignore if sound file is missing
 
        if self.debt_game_after_id:
            self.root.after_cancel(self.debt_game_after_id)
            self.debt_game_after_id = None
        
        # Hide any active result GIF
        self.hide_result_gif()
 
        self.debt_game_state = {
            "debt": random.randint(1000, 9999),
            "months": random.randint(3, 12),
        }
        if not init:
            self.debt_payment_entry.delete(0, tk.END)
            self.debt_result_label.config(text="")
 
        self.debt_info_label.config(
            text=f"Your debt: ₱{self.debt_game_state['debt']:,}\nMonths to pay: {self.debt_game_state['months']}"
        )
        self.debt_progress["value"] = 0
        self.debt_progress_label.config(text="")
        self.debt_play_btn.config(state="normal")
        # Reset the image to the default on game reset
        self._load_slot_image(r"recursiontest.py\yakuzamafia.jpg")
 
    def run_head_recursion(self):
        raw = self.students_head_var.get()
        students = self.parse_list(raw)
        if not students:
            messagebox.showerror("Error", "Please enter at least one student name.")
            return
        present_list, trace = self.demo.head_recursion_attendance(students)
        # show reporting order and trace
        trace_display = trace + ["", "Reporting order (last student -> first student):"] + [f"{i+1}. {name}" for i, name in enumerate(present_list)]
        self.update_output("Calling Attendance (Head Recursion)", trace_display)
 
    def _on_entry_click(self, entry):
        """Function to handle entry click. (No longer needed for student entry)"""
        pass
 
    def _on_focus_out(self, entry, placeholder):
        """Function to handle focus out. (No longer needed for student entry)"""
        pass
 
    def _load_slot_image(self, path):
        """Try to load an image into the left image slot. Silent on failure."""
        # Cancel any previous GIF animation
        if self.gif_animation_after_id:
            try:
                self.root.after_cancel(self.gif_animation_after_id)
            except Exception:
                pass
            self.gif_animation_after_id = None
            self.gif_frames = []
        try:
            img = Image.open(path)
        except Exception:
            # fallback: try same folder as this script with filename only
            import os
            try:
                fallback = os.path.join(os.path.dirname(__file__), "yakuzamafia.jpg")
                img = Image.open(fallback)
            except Exception:
                return

        # Check if it's an animated GIF
        is_gif = getattr(img, 'is_animated', False)

        # Clear placeholder text from canvas
        try:
            self.debt_image_slot.delete("placeholder")
        except Exception:
            pass

        if is_gif:
            self.gif_frames = []
            try:
                while True:
                    # Process each frame: crop to square and resize
                    frame = img.copy().convert("RGBA") # Ensure consistent format
                    width, height = frame.size
                    min_dim = min(width, height)
                    left, top = (width - min_dim) / 2, (height - min_dim) / 2
                    right, bottom = (width + min_dim) / 2, (height + min_dim) / 2
                    frame = frame.crop((left, top, right, bottom))
                    frame = frame.resize((180, 180), Image.LANCZOS)
                    self.gif_frames.append(ImageTk.PhotoImage(frame))
                    img.seek(len(self.gif_frames)) # Move to next frame
            except EOFError:
                pass # End of frames
            
            if self.gif_frames:
                self._animate_gif(0)
        else:
            # It's a static image
            width, height = img.size
            min_dim = min(width, height)
            left, top = (width - min_dim) / 2, (height - min_dim) / 2
            right, bottom = (width + min_dim) / 2, (height + min_dim) / 2
            img = img.crop((left, top, right, bottom))
            img = img.resize((180, 180), Image.LANCZOS)
            self.debt_image = ImageTk.PhotoImage(img)
            if self.debt_image_id is not None:
                self.debt_image_slot.delete(self.debt_image_id)
            self.debt_image_id = self.debt_image_slot.create_image(90, 90, image=self.debt_image)

    def _animate_gif(self, frame_index):
        """Cycles through GIF frames on the canvas."""
        if not self.gif_frames:
            return
        frame = self.gif_frames[frame_index]
        
        # Update the canvas image
        if self.debt_image_id is not None:
            self.debt_image_slot.delete(self.debt_image_id)
        self.debt_image_id = self.debt_image_slot.create_image(90, 90, image=frame)
        
        next_index = (frame_index + 1) % len(self.gif_frames)
        self.gif_animation_after_id = self.root.after(100, self._animate_gif, next_index) # 100ms delay between frames

    def show_result_gif(self, gif_path, message, text_color):
        """Displays a result GIF with text in the middle of the window for 3 seconds."""
        self.hide_result_gif() # Hide any previous one

        try:
            img = Image.open(gif_path)
        except FileNotFoundError:
            return

        # Load all frames of the GIF
        self.result_gif_frames = []
        try:
            while True:
                frame = img.copy().convert("RGBA")
                frame.thumbnail((400, 400)) # Resize to fit
                self.result_gif_frames.append(ImageTk.PhotoImage(frame))
                img.seek(len(self.result_gif_frames))
        except EOFError:
            pass

        if not self.result_gif_frames:
            return

        # Create a container frame
        self.result_frame = tk.Frame(self.root, bg="black", bd=0)
        self.result_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.result_frame.lift()

        # Label for the GIF
        gif_label = tk.Label(self.result_frame, bg="black", bd=0)
        gif_label.pack()

        # Label for the text
        text_label = tk.Label(self.result_frame, text=message, font=("Arial", 18, "bold"), bg="black", fg=text_color, justify="center")
        text_label.pack(pady=(5, 10))

        self._animate_result_gif(gif_label, 0)
        self.root.after(3000, self.hide_result_gif) # Hide after 3 seconds

    def _animate_result_gif(self, label, frame_index):
        """Cycles through GIF frames on the result label."""
        # Check if the frame/label still exist
        if not self.result_gif_frames or not self.result_frame or not label.winfo_exists():
            return
        frame = self.result_gif_frames[frame_index]
        label.config(image=frame)
        next_index = (frame_index + 1) % len(self.result_gif_frames)
        self.result_gif_animation_id = self.root.after(100, self._animate_result_gif, label, next_index)

    def hide_result_gif(self):
        """Hides the result GIF and cancels its animation."""
        if self.result_gif_animation_id:
            self.root.after_cancel(self.result_gif_animation_id)
            self.result_gif_animation_id = None

        if self.result_frame:
            self.result_frame.destroy()
            self.result_frame = None
        
        self.result_gif_frames = []

def create_splash_screen(root):
    """Creates and centers a splash screen."""
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)  # Frameless window
    splash.config(bg="#ffc0cb")
 
    # Center the splash screen
    root_width = 400
    root_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (root_width // 2)
    y = (screen_height // 2) - (root_height // 2)
    splash.geometry(f'{root_width}x{root_height}+{x}+{y}')
 
    tk.Label(splash, text="Recursion Visualizer", font=("Helvetica", 24, "bold"), bg="#ffc0cb", fg="black").pack(pady=(40, 10))
    tk.Label(splash, text="Loading, please wait...", font=("Helvetica", 12), bg="#ffc0cb", fg="black").pack()
 
    progress = ttk.Progressbar(splash, orient="horizontal", length=300, mode='determinate')
    progress.pack(pady=20)
    progress.start(15) # Animate the progress bar
 
    return splash
 
def main_app():
    root = tk.Tk()
    root.withdraw()  # Hide the main window initially
    splash = create_splash_screen(root)
 
    def launch_app():
        splash.destroy()
        app = RecursionGUI(root)
        root.deiconify() # Show the main window
 
    root.after(3000, launch_app)  # Show splash for 3 seconds
    root.mainloop()
 
if __name__ == "__main__":
    main_app()