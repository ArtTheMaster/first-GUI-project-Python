import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import time

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_position(self, pos, data):
        new_node = Node(data)
        if pos <= 1 or not self.head:
            self.prepend(data)
            return
        cur = self.head
        count = 1
        while cur.next and count < pos - 1:
            cur = cur.next
            count += 1
        new_node.next = cur.next
        cur.next = new_node

    def delete_by_value(self, value):
        if not self.head:
            return "List is empty."

        if self.head.data == value:
            self.head = self.head.next
            return

        cur = self.head
        while cur.next and cur.next.data != value:
            cur = cur.next

        if cur.next:
            cur.next = cur.next.next
        else:
            return f"Value '{value}' not found."

    def display(self):
        values = []
        cur = self.head
        while cur:
            values.append(str(cur.data))
            cur = cur.next
        return " -> ".join(values) if values else "List is empty."

    def get_nodes(self):
        nodes = []
        cur = self.head
        while cur:
            nodes.append(str(cur.data))
            cur = cur.next
        return nodes

    def clear(self):
        self.head = None

class DoublyLinkedList(SinglyLinkedList):
    def append(self, data):
        new_node = DoublyNode(data)
        if not hasattr(self, "head") or not self.head:
            self.head = new_node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node
        new_node.prev = cur

    def prepend(self, data):
        new_node = DoublyNode(data)
        if self.head:
            self.head.prev = new_node
        new_node.next = self.head
        self.head = new_node

    def insert_at_position(self, pos, data):
        new_node = DoublyNode(data)
        if pos <= 1 or not self.head:
            self.prepend(data)
            return
        cur = self.head
        count = 1
        while cur.next and count < pos - 1:
            cur = cur.next
            count += 1
        
        new_node.next = cur.next
        new_node.prev = cur
        if cur.next:
            cur.next.prev = new_node
        cur.next = new_node

class CircularLinkedList(SinglyLinkedList):
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
            return
        cur = self.head
        while cur.next != self.head:
            cur = cur.next
        cur.next = new_node
        new_node.next = self.head

    def prepend(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = new_node
            return
        
        last = self.head
        while last.next != self.head:
            last = last.next
        
        new_node.next = self.head
        last.next = new_node
        self.head = new_node

    def get_nodes(self):
        nodes = []
        if not self.head:
            return nodes
        cur = self.head
        while True:
            nodes.append(str(cur.data))
            cur = cur.next
            if cur == self.head:
                break
        return nodes

    def display(self):
        if not self.head:
            return "List is empty."
        cur = self.head
        result = []
        while True:
            result.append(str(cur.data))
            cur = cur.next
            if cur == self.head:
                break
        return " -> ".join(result) + " -> (back to head)"

    def delete_by_value(self, value):
        if not self.head:
            return "List is empty."

        if self.head.data == value:
            if self.head.next == self.head:
                self.head = None
                return
            
            last = self.head
            while last.next != self.head:
                last = last.next
            self.head = self.head.next
            last.next = self.head
            return

        prev = self.head
        cur = self.head.next
        while cur != self.head and cur.data != value:
            prev = cur
            cur = cur.next

        if cur == self.head:
            return f"Value '{value}' not found."
        
        prev.next = cur.next

class LinkedListGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Linked List Visualizer")
        self.root.geometry("950x720")

        self.theme = "pink"
        self.linked_list = None
        self.list_type = None
        self.current_frame = None

        self.log_history = []

        self.node_fill = "#ffc0cb"
        self.arrow_color = "#000000"

        self.themes = {
            "pink": {
                "root_bg": "#ffc0cb",
                "panel_bg": "#ffffff",
                "entry_bg": "#ffffff",
                "entry_fg": "#000000",
                "text_bg": "#ffffff",
                "text_fg": "#000000",
                "button_bg": "#ffc0cb",
                "button_active": "#ff8aa0",
                "button_fg": "#000000",
                "label_fg": "#000000",
                "canvas_bg": "#ffffff",
            },
            "dark": {
                "root_bg": "#121212",
                "panel_bg": "#1e1e1e",
                "entry_bg": "#1e1e1e",
                "entry_fg": "#ffdce6",
                "text_bg": "#1e1e1e",
                "text_fg": "#ffdce6",
                "button_bg": "#000000",
                "button_active": "#444444",
                "button_fg": "#ffc0cb",
                "label_fg": "#ffdce6",
                "canvas_bg": "#ffffff",
            }
        }

        self.log_text_color = "#00ff00"

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 11), padding=6, foreground="#000000")
        self.style.configure("Small.TButton", font=("Helvetica", 9), padding=4, foreground="#000000")

        self.create_main_menu()

    def apply_theme(self):
        t = self.themes[self.theme]

        try:
            self.root.configure(bg=t["root_bg"])
        except Exception:
            pass

        try:
            self.style.configure("TButton",
                                 background=t["button_bg"],
                                 foreground=t["button_fg"])
            self.style.map("TButton",
                           background=[("active", t["button_active"]), ("!active", t["button_bg"])],
                           foreground=[("active", t["button_fg"]), ("!active", t["button_fg"])])
            
            self.style.configure("Small.TButton",
                                 background=t["button_bg"],
                                 foreground=t["button_fg"])
            self.style.map("Small.TButton",
                           background=[("active", t["button_active"]), ("!active", t["button_bg"])],
                           foreground=[("active", t["button_fg"]), ("!active", t["button_fg"])])
        except Exception:
            pass

        def recolor(widget):
            cls = widget.winfo_class()
            
            if cls in ("Frame", "Labelframe"):
                try:
                    widget.configure(bg=t["root_bg"])
                except Exception:
                    pass
            if cls == "Label":
                try:
                    widget.configure(bg=t["root_bg"], fg=t["label_fg"])
                except Exception:
                    pass
            if cls == "Entry":
                try:
                    widget.configure(bg=t["entry_bg"], fg=t["entry_fg"], insertbackground=t["entry_fg"])
                except Exception:
                    pass
            if cls == "Text":
                try:
                    if hasattr(self, "log_box") and widget is self.log_box:
                        widget.configure(bg=t["text_bg"], fg=self.log_text_color, insertbackground=t["entry_fg"])
                    elif hasattr(self, "output_box") and widget is self.output_box:
                        widget.configure(bg="#ffffff", fg="#000000", insertbackground="#000000")
                    else:
                        widget.configure(bg=t["text_bg"], fg=t["text_fg"], insertbackground=t["entry_fg"])
                except Exception:
                    pass
            if cls == "Canvas":
                try:
                    widget.configure(bg="#ffffff")
                except Exception:
                    pass
            
            for child in widget.winfo_children():
                recolor(child)

        if self.current_frame:
            recolor(self.current_frame)

    def clear_window(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def create_header(self, parent, title_text, show_switch=True):
        header = tk.Frame(parent)
        header.pack(fill="x", pady=(12, 0), padx=12)
        
        lbl = tk.Label(header, text=title_text, font=("Helvetica", 18, "bold"))
        lbl.pack(side="left")
        
        if show_switch:
            btn = ttk.Button(header, text="Switch Theme", command=self.switch_theme, style="Small.TButton")
            btn.pack(side="right")
        return header

    def create_main_menu(self):
        self.clear_window()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(expand=True, fill="both")

        self.create_header(self.current_frame, "LINKED LIST VISUALIZER", show_switch=True)

        tk.Label(self.current_frame, text="Select a Linked List Type:",
                 font=("Helvetica", 14)).pack(pady=20)

        for text, cls in [("Singly Linked List", SinglyLinkedList),
                          ("Doubly Linked List", DoublyLinkedList),
                          ("Circular Linked List", CircularLinkedList)]:
            btn = ttk.Button(self.current_frame, text=text,
                             command=lambda c=cls, t=text: self.setup_list(c, t))
            btn.pack(pady=8, ipadx=10, ipady=5)

        self.apply_theme()
        self._restore_logs_to_widget_if_present()

    def setup_list(self, list_class, list_type):
        self.linked_list = list_class()
        self.list_type = list_type
        self.create_list_menu(list_type)

    def create_list_menu(self, list_type):
        self.clear_window()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(expand=True, fill="both")

        self.create_header(self.current_frame, list_type.upper(), show_switch=False)

        entry_frame = tk.Frame(self.current_frame)
        entry_frame.pack(pady=10)
        tk.Label(entry_frame, text="Value:").grid(row=0, column=0, padx=5)
        self.value_entry = tk.Entry(entry_frame, width=28, bd=1, relief="solid", font=("Helvetica", 11))
        self.value_entry.grid(row=0, column=1, padx=5)

        tk.Label(entry_frame, text="Position (optional):").grid(row=1, column=0, padx=5)
        self.pos_entry = tk.Entry(entry_frame, width=28, bd=1, relief="solid", font=("Helvetica", 11))
        self.pos_entry.grid(row=1, column=1, padx=5, pady=5)

        self.value_entry.bind("<KeyRelease>", lambda e: self.clear_visual(keep_logs=True))
        self.pos_entry.bind("<KeyRelease>", lambda e: self.clear_visual(keep_logs=True))

        btn_frame = tk.Frame(self.current_frame)
        btn_frame.pack(pady=10)

        buttons = [
            ("Append", self.append_value),
            ("Prepend", self.prepend_value),
            ("Insert", self.insert_value),
            ("Delete", self.delete_value),
            ("Random", self.random_nodes),
            ("Clear List", self.clear_list),
            ("Back", self.create_main_menu)
        ]

        for i, (txt, cmd) in enumerate(buttons):
            btn = ttk.Button(btn_frame, text=txt, command=cmd, width=14)
            btn.grid(row=i // 4, column=i % 4, padx=8, pady=5)

        self.canvas = tk.Canvas(self.current_frame, width=900, height=360, highlightthickness=0, bg="#ffffff")
        self.canvas.pack(pady=6)
        
        self.x_scrollbar = ttk.Scrollbar(self.current_frame, orient="horizontal", command=self.canvas.xview)
        self.x_scrollbar.pack(fill="x", padx=20, pady=(0, 6)) 
        
        self.canvas.configure(xscrollcommand=self.x_scrollbar.set)

        self.output_box = tk.Text(self.current_frame, height=4, width=95, state="disabled", wrap="word",
                                  bd=1, relief="solid", font=("Helvetica", 11), bg="#ffffff", fg="#000000", insertbackground="#000000")
        self.output_box.pack(pady=6)

        log_label_row = tk.Frame(self.current_frame)
        log_label_row.pack(fill="x", padx=20)
        tk.Label(log_label_row, text="Activity Log:").pack(side="left", anchor="w")
        ttk.Button(log_label_row, text="Clear Log (All History)", command=self.clear_log, style="Small.TButton").pack(side="right")

        log_frame = tk.Frame(self.current_frame)
        log_frame.pack(fill="both", expand=False, padx=20, pady=(4, 6))
        self.log_box = tk.Text(log_frame, height=8, width=95, state="disabled", wrap="word",
                               bd=1, relief="solid", font=("Helvetica", 11))
        self.log_box.pack(side="left", fill="both", expand=True)
        log_scroll = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_box.yview)
        log_scroll.pack(side="right", fill="y")
        self.log_box['yscrollcommand'] = log_scroll.set

        self.apply_theme()
        self._restore_logs_to_widget_if_present()


    def append_log(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        
        self.log_history.append(entry)
        
        if hasattr(self, "log_box") and self.log_box:
            try:
                self.log_box.config(state="normal")
                self.log_box.insert(tk.END, entry + "\n")
                self.log_box.see(tk.END)
                self.log_box.config(state="disabled")
            except Exception:
                pass

    def _restore_logs_to_widget_if_present(self):
        if hasattr(self, "log_box") and self.log_box:
            try:
                self.log_box.config(state="normal")
                self.log_box.delete("1.0", tk.END)
                for e in self.log_history:
                    self.log_box.insert(tk.END, e + "\n")
                self.log_box.see(tk.END)
                self.log_box.config(state="disabled")
            except Exception:
                pass

    def clear_log(self):
        self.log_history = []
        if hasattr(self, "log_box") and self.log_box:
            try:
                self.log_box.config(state="normal")
                self.log_box.delete("1.0", tk.END)
                self.log_box.config(state="disabled")
            except Exception:
                pass

    def clear_visual(self, keep_logs=False):
        try:
            if hasattr(self, "canvas") and self.canvas:
                self.canvas.delete("all")
        except Exception:
            pass
        if hasattr(self, "output_box") and self.output_box:
            try:
                self.output_box.config(state="normal")
                self.output_box.delete("1.0", tk.END)
                self.output_box.config(state="disabled")
            except Exception:
                pass
        
        if not keep_logs:
            pass

    def append_value(self):
        val_str = self.value_entry.get().strip()
        if not val_str:
            return messagebox.showwarning("Warning", "Enter a value!")
        
        try:
            val = int(val_str)
        except ValueError:
            return messagebox.showwarning("Invalid Input", "Value must be an integer.")

        self.linked_list.append(val)
        self.display_list()
        self.append_log(f"Appended value {val} to {self.list_type}.")

    def prepend_value(self):
        val_str = self.value_entry.get().strip()
        if not val_str:
            return messagebox.showwarning("Warning", "Enter a value!")

        try:
            val = int(val_str)
        except ValueError:
            return messagebox.showwarning("Invalid Input", "Value must be an integer.")

        self.linked_list.prepend(val)
        self.display_list()
        self.append_log(f"Prepended value {val} to {self.list_type}.")

    def insert_value(self):
        val_str = self.value_entry.get().strip()
        pos_text = self.pos_entry.get().strip()
        
        if not val_str:
            return messagebox.showwarning("Warning", "Enter a value!")

        try:
            val = int(val_str)
        except ValueError:
            return messagebox.showwarning("Invalid Input", "Value must be an integer.")

        try:
            pos = int(pos_text) if pos_text else 1
            if pos < 1:
                pos = 1
        except ValueError:
            messagebox.showwarning("Invalid Input", "Position must be an integer. Defaulting to 1.")
            pos = 1  
        
        self.linked_list.insert_at_position(pos, val)
        self.display_list()
        self.append_log(f"Inserted value {val} at position {pos} in {self.list_type}.")

    def delete_value(self):
        val_str = self.value_entry.get().strip()
        if not val_str:
            return messagebox.showwarning("Warning", "Enter a value to delete!")
        
        try:
            val = int(val_str)
        except ValueError:
            return messagebox.showwarning("Invalid Input", "Value to delete must be an integer.")

        msg = self.linked_list.delete_by_value(val)
        
        if msg:
            messagebox.showinfo("Info", msg)
            self.append_log(f"Attempted to delete {val} from {self.list_type}: {msg}")
        else:
            self.append_log(f"Deleted value {val} from {self.list_type}.")
        self.display_list()

    def random_nodes(self):
        if not self.linked_list:
            return
        count = simpledialog.askinteger("Random nodes", "How many random nodes to create?", initialvalue=5, minvalue=1, maxvalue=100)
        if count is None:
            return
        
        for _ in range(count):
            val = random.randint(0, 999)
            self.linked_list.append(val)
            
        self.display_list()
        self.append_log(f"Added {count} random node(s) to {self.list_type}.")

    def clear_list(self):
        if self.linked_list:
            self.linked_list.clear()
        self.display_list()
        self.append_log(f"Cleared all nodes from {self.list_type}.")

    def switch_theme(self):
        self.theme = "dark" if self.theme == "pink" else "pink"
        self.create_main_menu()
        self.append_log(f"Theme switched to {self.theme}.")

    
    def display_list(self):
        nodes = self.linked_list.get_nodes() if self.linked_list else []
        text = self.linked_list.display() if self.linked_list else "List is empty."
        
        if hasattr(self, "output_box") and self.output_box:
            try:
                self.output_box.config(state="normal")
                self.output_box.delete("1.0", tk.END)
                self.output_box.insert(tk.END, text)
                self.output_box.config(state="disabled")
            except Exception:
                pass
            
        self.animate_nodes(nodes)

    def animate_nodes(self, nodes):
        canvas = getattr(self, "canvas", None)
        if not canvas:
            return
        
        try:
            canvas.delete("all")
            canvas.configure(bg="#ffffff")
        except Exception:
            pass

        if not nodes:
            try:
                canvas.create_text(450, 180, text="List is empty.",
                                   font=("Helvetica", 14, "italic"),
                                   fill="#000000")
            except Exception:
                pass
        
        else:
            x, y = 60, 180
            node_d = 60
            spacing = 40
            
            centers = []
            
            try:
                for i, val in enumerate(nodes):
                    cx = x + i * (node_d + spacing) + node_d // 2
                    cy = y
                    centers.append((cx, cy))
                    
                    outline_color = "#000000"
                    canvas.create_oval(cx - node_d // 2, cy - node_d // 2, cx + node_d // 2, cy + node_d // 2,
                                       fill=self.node_fill, outline=outline_color, width=2)
                    canvas.create_text(cx, cy, text=val, fill="#000000", font=("Helvetica", 12, "bold"))

                for i in range(len(centers) - 1):
                    x1, y1 = centers[i]
                    x2, y2 = centers[i+1]
                    canvas.create_line(x1 + node_d // 2, y1, x2 - node_d // 2, y2,
                                       arrow=tk.LAST, width=2, fill=self.arrow_color)

                if self.list_type == "Doubly Linked List" and len(centers) > 1:
                    for i in range(len(centers) - 1):
                        x1, y1 = centers[i]
                        x2, y2 = centers[i + 1]
                        canvas.create_line(x2 - node_d // 2, y2 + 12, x1 + node_d // 2, y1 + 12,
                                           arrow=tk.LAST, dash=(4, 3), width=2, fill=self.arrow_color)

                if self.list_type == "Circular Linked List" and len(centers) > 1:
                    x_first, y_first = centers[0]
                    x_last, y_last = centers[-1]
                    top = y - 80
                    canvas.create_line(x_last + node_d // 2, y_last,
                                       x_last + node_d // 2 + 20, top,
                                       x_first - node_d // 2 - 20, top,
                                       x_first - node_d // 2, y_first,
                                       smooth=True, width=2, arrow=tk.LAST, dash=(4, 3), fill=self.arrow_color)
                    canvas.create_text((x_first + x_last) / 2, top - 12,
                                       text="(back to head)", fill="#000000", font=("Helvetica", 10, "italic"))

                if centers:
                    hx, hy = centers[0]
                    canvas.create_text(hx, hy - node_d // 2 - 10, text="HEAD", fill="#000000", font=("Helvetica", 9, "bold"))
                    tx, ty = centers[-1]
                    canvas.create_text(tx, ty + node_d // 2 + 12, text="TAIL", fill="#000000", font=("Helvetica", 9, "bold"))
            except Exception:
                pass

        try:
            bbox = canvas.bbox("all")
            if bbox:
                c_height = canvas.winfo_height()
                if c_height < 50: c_height = 360 
                
                scroll_x1 = max(0, bbox[0] - 20)
                scroll_x2 = bbox[2] + 20
                
                canvas.configure(scrollregion=(scroll_x1, 0, scroll_x2, c_height))
            else:
                c_width = canvas.winfo_width()
                c_height = canvas.winfo_height()
                if c_width < 50: c_width = 900
                if c_height < 50: c_height = 360
                canvas.configure(scrollregion=(0, 0, c_width, c_height))
        except Exception:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = LinkedListGUI(root)
    root.mainloop()