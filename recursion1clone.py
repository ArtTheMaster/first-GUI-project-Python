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
        if present is None:
            present = []
        if trace is None:
            trace = []
        if idx == 0:
            students = [name.strip().title() for name in students]

        if idx >= len(students):
            trace.append("Last student reached. Now reporting back.")
            return present, trace

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
        self.root.configure(bg="#ffc0cb")

        self.demo = RecursionDemo()
        self.animation_after_id = None
        self.debt_game_state = None
        self.debt_game_after_id = None
        self.gif_frames = []
        self.gif_animation_after_id = None
        self.result_gif_frames = []
        self.result_gif_animation_id = None
        self.result_frame = None
        self.image_photo = None

        pygame.mixer.init(frequency=33075)
        self.setup_gui()

    def setup_gui(self):
        title = tk.Label(self.root, text="Recursion Demos: Mafia Debt Game & Attendance",
                         font=("Helvetica", 22, "bold"), bg="#ffc0cb", fg="black")
        title.pack(pady=16)

        debt_frame = tk.LabelFrame(self.root, text="💰 Tail Recursion Debt Game 💰",
                                     bg="#ffc0cb", fg="black", font=("Arial", 12, "bold"), padx=10, pady=6)
        debt_frame.pack(fill="x", padx=20, pady=8)

        slot_size = 180
        self.debt_image_slot = tk.Canvas(debt_frame, width=slot_size, height=slot_size,
                                        bg="white", relief="ridge", bd=2, highlightthickness=0)
        self.debt_image_slot.create_text(slot_size//2, slot_size//2,
                                         text="Image slot\n(put image here later)",
                                         font=("Arial", 10), fill="gray", justify="center", tags=("placeholder",))
        self.debt_image_slot.pack(side="left", padx=10, pady=5)
        self.debt_image = None
        self.debt_image_id = None

        self._load_slot_image(r"yakuzamafia.jpg")

        debt_right = tk.Frame(debt_frame, bg="#ffc0cb")
        debt_right.pack(side="left", fill="both", expand=True, padx=(8,0))

        self.debt_info_label = tk.Label(debt_right, text="Your debt: ₱0\nMonths to pay: 0",
                                        font=("Arial", 12), fg="black", bg="#ffc0cb")
        self.debt_info_label.pack(pady=5, anchor="w")

        tk.Label(debt_right, text="Enter your monthly payment:",
                 font=("Arial", 11), fg="black", bg="#ffc0cb").pack(anchor="w")

        self.debt_payment_entry = tk.Entry(debt_right, font=("Arial", 12), justify="center")
        self.debt_payment_entry.pack(pady=5, anchor="w")
 
        debt_btn_frame = tk.Frame(debt_frame, bg="#ffc0cb")
        debt_btn_frame.pack(pady=5)
 
        self.debt_play_btn = tk.Button(debt_btn_frame, text="Pay Off Debt!", command=self.play_debt_game,
                                       font=("Arial", 12, "bold"), bg="#35BB00", fg="white", width=15)
        self.debt_play_btn.pack(side="left", padx=5)
 
        self.debt_reset_btn = tk.Button(debt_btn_frame, text="Reset Game", command=self.reset_debt_game,
                                        font=("Arial", 11), bg="#FF6347", fg="white", width=15)
        self.debt_reset_btn.pack(side="left", padx=5)
 
        self.debt_progress = ttk.Progressbar(debt_frame, orient="horizontal", length=300, mode="determinate")
        self.debt_progress.pack(pady=5)
        self.debt_progress_label = tk.Label(debt_frame, text="", fg="black", bg="#ffc0cb", font=("Arial", 10))
        self.debt_progress_label.pack(pady=2)
 
        self.debt_result_label = tk.Label(debt_frame, text="", font=("Arial", 12), fg="black", bg="#ffc0cb")
        self.debt_result_label.pack(pady=5)
 
        attend_head_frame = tk.LabelFrame(self.root, text="Calling Attendance (Head Recursion)",
                                  bg="#ffc0cb", fg="black", font=("Helvetica", 10, "bold"), padx=10, pady=6)
        attend_head_frame.pack(fill="x", padx=20, pady=8)
 
        self.students_head_var = tk.StringVar(value="")
        self.students_head_entry = ttk.Entry(attend_head_frame, textvariable=self.students_head_var, width=80)
        self.students_head_entry.pack(fill="x", pady=6)
 
        btn_box_frame = tk.Frame(attend_head_frame, bg="#ffc0cb")
        btn_box_frame.pack(fill="x", pady=4)
        ttk.Button(btn_box_frame, text="Run Attendance (Head Recursion)",
                   command=self.run_head_recursion).pack(side="left", padx=(0, 8))
        ttk.Button(btn_box_frame, text="Clear Log",
                   command=partial(self.clear_output, reset_game=False)).pack(side="left")
 
        out_frame = tk.Frame(self.root, bg="#ffc0cb")
        out_frame.pack(fill="both", expand=True, padx=20, pady=12)
 
        self.output_text = tk.Text(out_frame, height=18, bg="white", fg="black", font=("Courier", 10))
        self.output_text.pack(side="top", fill="both", expand=True)
 
        self.image_label = tk.Label(out_frame, bg="white")
        self.image_label.pack(side="bottom", pady=5)
 
        bottom_frame = tk.Frame(self.root, bg="#ffc0cb")
        bottom_frame.pack(fill="x", padx=20, pady=(0, 6))
        ttk.Button(bottom_frame, text="Clear Output", command=partial(self.clear_output, reset_game=True)).pack(side="right")
 
        self.reset_debt_game(init=True)
 
    def parse_list(self, raw):
        items = [s.strip().title() if ',' in raw else s.strip() for s in raw.split(",") if s.strip()]
        return items
 
    def _prepare_lines(self, trace_list):
        lines = []
        for item in trace_list:
            parts = item.split("\n")
            for p in parts:
                lines.append(p)
        return lines
 
    def update_output(self, title, trace_list):
        if self.animation_after_id:
            try:
                self.root.after_cancel(self.animation_after_id)
            except Exception:
                pass
            self.animation_after_id = None
 
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"{title}\n{'='*60}\n")
        lines = self._prepare_lines(trace_list)
        self._animate_lines(lines, 0, 0)
        self.output_text.config(state="disabled")
 
    def _animate_lines(self, lines, line_idx, word_idx):
        self.output_text.config(state="normal")
 
        if line_idx >= len(lines):
            self.animation_after_id = None
            self.output_text.config(state="disabled")
            return
 
        line = lines[line_idx]
        words = line.split(' ') if line != "" else []
        if word_idx < len(words):
            prefix = "" if word_idx == 0 else " "
            self.output_text.insert(tk.END, prefix + words[word_idx])
            self.animation_after_id = self.root.after(300, lambda: self._animate_lines(lines, line_idx, word_idx + 1))
        else:
            self.output_text.insert(tk.END, "\n")
            self.animation_after_id = self.root.after(300, lambda: self._animate_lines(lines, line_idx + 1, 0))
 
        self.output_text.see(tk.END)
        self.output_text.config(state="disabled")
 
    def clear_output(self, reset_game=True):
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
 
    def play_debt_game(self):
        if self.debt_payment_entry.get().strip() == "67":
            self._load_slot_image(r"scp-067-67.gif")
        else:
            self._load_slot_image(r"yakuzamafia.jpg")

        try:
            pygame.mixer.music.load(r"Cha-Ching Sound Effect.mp3")
            pygame.mixer.music.play()
        except pygame.error:
            pass

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
 
        self.debt_progress["value"] = state["current_month"] - 1
        self.debt_progress_label.config(
            text=f"Month {state['current_month']} - Remaining debt: ₱{max(state['remaining_debt'], 0):,}"
        )
        self.root.update_idletasks()
 
        state["remaining_debt"] -= state["payment"]
        state["current_month"] += 1
 
        self.debt_game_after_id = self.root.after(400, self.update_debt_progress)
 
    def show_debt_result(self):
        state = self.debt_game_state
        self.debt_progress["value"] = state["months"]
        self.debt_progress_label.config(text=f"Final debt: ₱{state['remaining_debt']:,}")
 
        result_text = ""
        if abs(state['remaining_debt']) <= 5:
            color = "#00FF7F"
            popup_message = f"Final debt: ₱{state['remaining_debt']:,} and YOU WIN!\nDebt cleared within ₱5 margin."
            self.show_result_gif(r"win.gif", popup_message, color, 7000)
        elif state['remaining_debt'] < -5:
            color = "#FF4500"
            popup_message = f"YOU LOSE!\nYou overpaid by ₱{abs(state['remaining_debt']):,}"
            self.show_result_gif(r"lose.gif", popup_message, color, 11000)
        else:
            color = "#FF4500"
            popup_message = f"YOU LOSE!\nYou still owe ₱{state['remaining_debt']:,}"
            self.show_result_gif(r"lose.gif", popup_message, color, 11000)
 
        self.debt_result_label.config(text=result_text, fg=color)
        self.debt_play_btn.config(state="normal")
        
        if abs(state['remaining_debt']) <= 5:
            try:
                pygame.mixer.music.load(r"Persona 4 - Specialist.mp3")
                pygame.mixer.music.play()
            except pygame.error:
                pass
        else:
            try:
                pygame.mixer.music.load(r"Yakuza OST - Baka Mitai - Kiryu full versionJapanese Romaji English lyrics.mp3")
                pygame.mixer.music.play()
            except pygame.error:
                pass
 
    def reset_debt_game(self, init=False):
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass
            
        if not init:
            try:
                pygame.mixer.music.load("Impact Laser - Free Sound Effect-[AudioTrimmer.com].mp3")
                pygame.mixer.music.play()
            except pygame.error:
                pass
 
        if self.debt_game_after_id:
            self.root.after_cancel(self.debt_game_after_id)
            self.debt_game_after_id = None
        
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
        self._load_slot_image(r"yakuzamafia.jpg")
 
    def run_head_recursion(self):
        raw = self.students_head_var.get()
        students = self.parse_list(raw)
        if not students:
            messagebox.showerror("Error", "Please enter at least one student name.")
            return
        present_list, trace = self.demo.head_recursion_attendance(students)
        trace_display = trace + ["", "Reporting order (last student -> first student):"] + [f"{i+1}. {name}" for i, name in enumerate(present_list)]
        self.update_output("Calling Attendance (Head Recursion)", trace_display)
 
    def _on_entry_click(self, entry):
        pass
 
    def _on_focus_out(self, entry, placeholder):
        pass
 
    def _load_slot_image(self, path):
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
            import os
            try:
                fallback = os.path.join(os.path.dirname(__file__), "yakuzamafia.jpg")
                img = Image.open(fallback)
            except Exception:
                return

        is_gif = getattr(img, 'is_animated', False)

        try:
            self.debt_image_slot.delete("placeholder")
        except Exception:
            pass

        if is_gif:
            self.gif_frames = []
            try:
                while True:
                    frame = img.copy().convert("RGBA")
                    width, height = frame.size
                    min_dim = min(width, height)
                    left, top = (width - min_dim) / 2, (height - min_dim) / 2
                    right, bottom = (width + min_dim) / 2, (height + min_dim) / 2
                    frame = frame.crop((left, top, right, bottom))
                    frame = frame.resize((180, 180), Image.LANCZOS)
                    self.gif_frames.append(ImageTk.PhotoImage(frame))
                    img.seek(len(self.gif_frames))
            except EOFError:
                pass
            
            if self.gif_frames:
                self._animate_gif(0)
        else:
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
        if not self.gif_frames:
            return
        frame = self.gif_frames[frame_index]
        
        if self.debt_image_id is not None:
            self.debt_image_slot.delete(self.debt_image_id)
        self.debt_image_id = self.debt_image_slot.create_image(90, 90, image=frame)
        
        next_index = (frame_index + 1) % len(self.gif_frames)
        self.gif_animation_after_id = self.root.after(100, self._animate_gif, next_index)

    def show_result_gif(self, gif_path, message, text_color, duration_ms):
        self.hide_result_gif()

        try:
            img = Image.open(gif_path)
        except FileNotFoundError:
            return

        self.result_gif_frames = []
        try:
            while True:
                frame = img.copy().convert("RGBA")
                frame.thumbnail((400, 400))
                self.result_gif_frames.append(ImageTk.PhotoImage(frame))
                img.seek(len(self.result_gif_frames))
        except EOFError:
            pass

        if not self.result_gif_frames:
            return

        self.result_frame = tk.Frame(self.root, bg="black", bd=0)
        self.result_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.result_frame.lift()

        gif_label = tk.Label(self.result_frame, bg="black", bd=0)
        gif_label.pack()

        text_label = tk.Label(self.result_frame, text=message, font=("Arial", 18, "bold"), bg="black", fg=text_color, justify="center")
        text_label.pack(pady=(5, 10))

        self._animate_result_gif(gif_label, 0)
        self.root.after(duration_ms, self.hide_result_gif)

    def _animate_result_gif(self, label, frame_index):
        if not self.result_gif_frames or not self.result_frame or not label.winfo_exists():
            return
        frame = self.result_gif_frames[frame_index]
        label.config(image=frame)
        next_index = (frame_index + 1) % len(self.result_gif_frames)
        self.result_gif_animation_id = self.root.after(100, self._animate_result_gif, label, next_index)

    def hide_result_gif(self):
        if self.result_gif_animation_id:
            self.root.after_cancel(self.result_gif_animation_id)
            self.result_gif_animation_id = None

        if self.result_frame:
            self.result_frame.destroy()
            self.result_frame = None
        
        self.result_gif_frames = []

def create_splash_screen(root):
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.config(bg="#ffc0cb")
 
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
    progress.start(15)
 
    return splash
 
def main_app():
    root = tk.Tk()
    root.withdraw()
    splash = create_splash_screen(root)
 
    def launch_app():
        splash.destroy()
        app = RecursionGUI(root)
        root.deiconify()
 
    root.after(3000, launch_app)
    root.mainloop()
 
if __name__ == "__main__":
    main_app()