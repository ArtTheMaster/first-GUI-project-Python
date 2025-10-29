import tkinter as tk
from tkinter import font, messagebox
from PIL import Image, ImageTk
import os

def show_image_popup(title, message, image_path, size=(500, 500)):
    """Show a popup with an image and message.

    size: maximum (width, height) in pixels. The image will be scaled to
    fit within this box while preserving aspect ratio using Pillow's
    thumbnail().
    """
    popup = tk.Toplevel()
    popup.title(title)
    popup.config(bg="pink")

    try:
        img = Image.open(image_path)
        # Preserve aspect ratio and fit inside `size`
        try:
            img.thumbnail(size, Image.LANCZOS)
        except Exception:
            img.thumbnail(size)
        photo = ImageTk.PhotoImage(img)
        label_img = tk.Label(popup, image=photo, bg="pink")
        label_img.image = photo  # prevent garbage collection
        label_img.pack(pady=40)
    except Exception as e:
        tk.Label(popup, text=f"Error loading image:\n{e}", fg="red", bg="pink").pack(pady=10)

    tk.Label(
        popup,
        text=message,
        fg="white",
        bg="black",
        font=("Arial", 12, "bold"),
        wraplength=250
    ).pack(padx=10, pady=5)

    tk.Button(
        popup,
        text="Close",
        command=popup.destroy,
        bg="black",
        fg="white"
    ).pack(pady=10)


class AsciiStackApp:
    MAX_STACK = 10

    def __init__(self, root):
        self.root = root
        root.title("ASCII Stack (Tkinter)")
        root.config(bg="pink")

        self.stack = []

        main_frame = tk.Frame(root, bg="pink")
        main_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(main_frame, text="Value:", bg="pink").pack(side="left")
        self.entry = tk.Entry(main_frame)
        self.entry.pack(side="left", fill="x", expand=True, padx=(5, 5))
        self.entry.bind("<Return>", lambda e: self.push())

        btn_push = tk.Button(main_frame, text="Push", width=8, command=self.push, bg="black", fg="white")
        btn_pop = tk.Button(main_frame, text="Pop", width=8, command=self.pop, bg="black", fg="white")
        btn_peek = tk.Button(main_frame, text="Peek", width=8, command=self.peek, bg="black", fg="white")
        btn_clear = tk.Button(main_frame, text="Clear", width=8, command=self.clear, bg="black", fg="white")

        btn_push.pack(side="left", padx=2)
        btn_pop.pack(side="left", padx=2)
        btn_peek.pack(side="left", padx=2)
        btn_clear.pack(side="left", padx=2)

        info_frame = tk.Frame(root, bg="pink")
        info_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(info_frame, text="Peek Result:", bg="pink", fg="black", font=("Arial", 10, "bold")).pack(anchor="w")
        self.peek_label = tk.Label(info_frame, text="(none)", bg="white", fg="black", width=40, anchor="w")
        self.peek_label.pack(anchor="w", pady=(0, 5))

        tk.Label(info_frame, text="Stack Info:", bg="pink", fg="black", font=("Arial", 10, "bold")).pack(anchor="w")
        self.info_label = tk.Label(info_frame, text="Stacks: 0 / 10", bg="white", fg="black", width=40, anchor="w")
        self.info_label.pack(anchor="w")

        self.text = tk.Text(root, width=48, height=20, wrap="none", bg="white")
        mono = font.nametofont("TkFixedFont")
        self.text.configure(font=(mono.actual("family"), 12))
        self.text.pack(padx=10, pady=(10, 5))
        self.text.configure(state="disabled")

        self.status = tk.Label(root, text="Ready", anchor="w", bg="pink")
        self.status.pack(fill="x", padx=10, pady=(0, 10))

        self.max_width = 36
        self.draw()

    def set_status(self, msg):
        self.status.config(text=msg)

    def update_info(self):
        count = len(self.stack)
        if count >= self.MAX_STACK:
            self.info_label.config(text="Overflow! Stack > 10", fg="red")
        
            base_dir = os.path.dirname(__file__)
            img_path = None
            for candidate in ("overflow.jpg", "overflow.png"):
                candidate_path = os.path.join(base_dir, candidate)
                if os.path.exists(candidate_path):
                    img_path = candidate_path
                    break

            if img_path is None:
                img_path = os.path.join(base_dir, 'overflow.jpg')
            show_image_popup("Bruh ", "stack is full! stop", img_path)

        else:
            self.info_label.config(text=f"Stacks: {count} / {self.MAX_STACK}", fg="black")

    def push(self):
        v = self.entry.get().strip()
        if v == "":
            self.set_status("Cannot push empty value.")
            return

        if len(self.stack) >= self.MAX_STACK:
            self.set_status("Overflow! Cannot add more stacks.")
            self.update_info()
            return

        if len(v) > self.max_width:
            v = v[:self.max_width - 3] + "..."

        self.stack.append(v)
        self.entry.delete(0, "end")
        self.set_status(f"Pushed: {v}")
        self.update_info()
        self.draw()

        keyword = v.lower()
        script_dir = os.path.dirname(__file__)

        if keyword == "67":
            show_image_popup("'67'!", "You found 67!", os.path.join(script_dir, "67.jpg"))
        elif keyword == "art":
            show_image_popup("Leader", "You found art!", os.path.join(script_dir, "art.png"))
        elif keyword == "lem":
            show_image_popup("Lem", "HUh? bat nandito ako?", os.path.join(script_dir, "lem.png"))
        elif keyword == "tim":
            show_image_popup("Timoth", "You found Tim!", os.path.join(script_dir, "tim.jpg"))
        elif keyword == "lizardo":
            show_image_popup("You found Lazaro!", "get lizarded", os.path.join(script_dir, "lizardo.png"))
        elif keyword == "luwigee":
            show_image_popup("Luwigee", "Luwigee Nambahwan!", os.path.join(script_dir, "luwigee.jpg"))

    def pop(self):
        if not self.stack:
            self.set_status("Pop failed: stack is empty.")
            return
        v = self.stack.pop()
        self.set_status(f"Popped: {v}")
        self.update_info()
        self.draw()

    def peek(self):
        if not self.stack:
            self.set_status("Peek: stack is empty.")
            self.peek_label.config(text="(empty)")
            return
        v = self.stack[-1]
        self.peek_label.config(text=v)
        self.set_status(f"Top: {v}")

    def clear(self):
        if not self.stack:
            self.set_status("Stack already empty.")
            return
        if messagebox.askyesno("Clear stack", "Clear all items from the stack?"):
            self.stack.clear()
            self.set_status("Stack cleared.")
            self.update_info()
            self.draw()
            self.peek_label.config(text="(none)")

    def draw(self):
        lines = []
        if not self.stack:
            lines = ["+----------------------------+",
                     "|      [ empty stack :3 ]    |",
                     "+----------------------------+"]
        else:
            # Show top-first (most recent at the top)
            contents = self.stack[::-1]
            inside_width = min(self.max_width, max(len(str(x)) for x in contents))
            box_w = inside_width + 2
            border = "+" + "-" * box_w + "+"
            # Build lines for each item
            for item in contents:
                s = str(item)
                if len(s) > inside_width:
                    s = s[:inside_width - 3] + "..."
                padded = " " + s.ljust(inside_width) + " "
                lines.append(border)
                lines.append("|" + padded + "|")
            lines.append(border)
            # indicate top at the top of the display
            lines.insert(0, "↓ TOP")

        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        for ln in lines:
            self.text.insert("end", ln + "\n")
        self.text.configure(state="disabled")

  


if __name__ == "__main__":
    root = tk.Tk()
    app = AsciiStackApp(root)
    root.mainloop()
