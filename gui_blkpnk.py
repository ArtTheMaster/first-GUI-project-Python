import tkinter as tk
from tkinter import ttk, messagebox, simpledialog  # Import necessary tkinter components
import random  # Used for the "Random" button
import time    # Used for timestamping log entries

# -------------------------------
# Linked List Implementations
# (These classes define the "backend" data structures)
# -------------------------------

class Node:
    """A standard Node for a Singly or Circular Linked List."""
    def __init__(self, data):
        self.data = data  # The value stored in the node
        self.next = None  # The pointer to the next node in the list

class DoublyNode:
    """A Node for a Doubly Linked List."""
    def __init__(self, data):
        self.data = data  # The value stored in the node
        self.prev = None  # The pointer to the *previous* node
        self.next = None  # The pointer to the *next* node

# -------------------------------
# Singly Linked List
# (The base class for all list types in this app)
# -------------------------------
class SinglyLinkedList:
    def __init__(self):
        """Initializes an empty list."""
        self.head = None  # The 'head' is the pointer to the very first node. If None, the list is empty.

    def append(self, data):
        """Adds a new node with 'data' to the *end* of the list."""
        new_node = Node(data)
        if not self.head:
            # If the list is empty, the new node becomes the head
            self.head = new_node
            return
        # Otherwise, traverse the list to find the last node
        cur = self.head
        while cur.next:  # Loop until 'cur' is the last node (i.e., cur.next is None)
            cur = cur.next
        # Link the last node to the new node
        cur.next = new_node

    def prepend(self, data):
        """Adds a new node with 'data' to the *beginning* of the list."""
        new_node = Node(data)
        # Link the new node to the old head
        new_node.next = self.head
        # Update the head to be the new node
        self.head = new_node

    def insert_at_position(self, pos, data):
        """Inserts a new node at a specific position (1-based index)."""
        new_node = Node(data)
        # If pos is 1 or list is empty, just prepend
        if pos <= 1 or not self.head:
            self.prepend(data)
            return
        # Traverse to the node *before* the target position
        cur = self.head
        count = 1  # Start at position 1 (the head)
        while cur.next and count < pos - 1:
            cur = cur.next
            count += 1
        # Insert the new node: new_node's next points to cur's next
        new_node.next = cur.next
        # cur's next points to the new_node
        cur.next = new_node

    def delete_by_value(self, value):
        """Finds and deletes the first node containing 'value'."""
        if not self.head:
            return "List is empty."  # Cannot delete from an empty list

        # If the head node is the one to delete
        if self.head.data == value:
            self.head = self.head.next  # Move the head pointer to the next node
            return  # Deletion successful

        # Traverse the list to find the node *before* the one to delete
        cur = self.head
        while cur.next and cur.next.data != value:
            cur = cur.next

        # If we found the node (i.e., cur.next is the target)
        if cur.next:
            cur.next = cur.next.next  # "Skip over" the node to delete it
        else:
            return f"Value '{value}' not found."  # Reached end of list without finding value

    def display(self):
        """Returns a string representation of the list for the output box."""
        values = []
        cur = self.head
        while cur:
            values.append(str(cur.data))
            cur = cur.next
        return " -> ".join(values) if values else "List is empty."

    def get_nodes(self):
        """Returns a simple list of node values (as strings) for the visualizer."""
        nodes = []
        cur = self.head
        while cur:
            nodes.append(str(cur.data))
            cur = cur.next
        return nodes

    def clear(self):
        """Empties the list."""
        self.head = None


# -------------------------------
# Doubly Linked List
# (Inherits from SinglyLinkedList and overrides methods to add 'prev' links)
# -------------------------------
class DoublyLinkedList(SinglyLinkedList):
    def append(self, data):
        """Overrides append to add 'prev' links."""
        new_node = DoublyNode(data)  # Use DoublyNode
        if not hasattr(self, "head") or not self.head:
            self.head = new_node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        # Standard link
        cur.next = new_node
        # New link for doubly
        new_node.prev = cur

    def prepend(self, data):
        """Overrides prepend to add 'prev' links."""
        new_node = DoublyNode(data)  # Use DoublyNode
        if self.head:
            # New link: old head's prev points to new node
            self.head.prev = new_node
        # Standard links
        new_node.next = self.head
        self.head = new_node

    def insert_at_position(self, pos, data):
        """Overrides insert to add 'prev' links."""
        new_node = DoublyNode(data)
        if pos <= 1 or not self.head:
            self.prepend(data)
            return
        cur = self.head
        count = 1
        while cur.next and count < pos - 1:
            cur = cur.next
            count += 1
        
        # Standard links
        new_node.next = cur.next
        # New links for doubly
        new_node.prev = cur
        if cur.next:
            # Make the *next* node's prev point back to the new node
            cur.next.prev = new_node
        cur.next = new_node


# -------------------------------
# Circular Linked List
# (Inherits from SinglyLinkedList and overrides methods for circular logic)
# -------------------------------
class CircularLinkedList(SinglyLinkedList):
    def append(self, data):
        """Overrides append. Last node must point back to head."""
        new_node = Node(data)
        if not self.head:
            # If empty, new node is head and points to itself
            self.head = new_node
            new_node.next = self.head
            return
        # Traverse to the last node (the one pointing to head)
        cur = self.head
        while cur.next != self.head:
            cur = cur.next
        # Link last node to new node
        cur.next = new_node
        # Link new node back to head
        new_node.next = self.head

    def prepend(self, data):
        """Overrides prepend. Must update *last* node's pointer."""
        new_node = Node(data)
        if not self.head:
            # If empty, new node points to itself
            self.head = new_node
            new_node.next = new_node
            return
        
        # Find the last node
        last = self.head
        while last.next != self.head:
            last = last.next
        
        # Link new node to old head
        new_node.next = self.head
        # Link last node to new node
        last.next = new_node
        # Update head
        self.head = new_node

    def get_nodes(self):
        """Overrides get_nodes for circular traversal."""
        nodes = []
        if not self.head:
            return nodes
        cur = self.head
        while True:
            # Loop runs at least once
            nodes.append(str(cur.data))
            cur = cur.next
            if cur == self.head:
                break  # Stop when we've returned to the head
        return nodes

    def display(self):
        """Overrides display for circular traversal."""
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
        """Overrides delete for circular logic."""
        if not self.head:
            return "List is empty."

        # Case 1: Deleting the head node
        if self.head.data == value:
            # Case 1a: Only one node in the list
            if self.head.next == self.head:
                self.head = None
                return
            
            # Case 1b: Multiple nodes. Find last node.
            last = self.head
            while last.next != self.head:
                last = last.next
            # New head is the next node
            self.head = self.head.next
            # Link last node to new head
            last.next = self.head
            return

        # Case 2: Deleting a node other than the head
        prev = self.head
        cur = self.head.next
        # Traverse until we find the value or return to the head
        while cur != self.head and cur.data != value:
            prev = cur
            cur = cur.next

        # If we looped all the way around, value was not found
        if cur == self.head:
            return f"Value '{value}' not found."
        
        # Found it. Skip over 'cur'
        prev.next = cur.next


# -------------------------------
# GUI Class
# (Handles all Tkinter widgets, layout, and event handling)
# -------------------------------
class LinkedListGUI:
    def __init__(self, root):
        self.root = root  # The main application window
        self.root.title("Linked List Visualizer")
        self.root.geometry("950x720")

        # --- State Variables ---
        # These variables track the application's current state
        self.theme = "pink"          # Current theme: 'pink' or 'dark'
        self.linked_list = None      # The *instance* of the currently active linked list object
        self.list_type = None        # A string name like "Singly Linked List"
        self.current_frame = None    # Holds the currently displayed frame (main menu or list menu)

        # --- Persistent Data ---
        # This log survives menu switches
        self.log_history = []  # A list of all log strings

        # --- Theme & Color Definitions ---
        # Specific colors requested
        self.node_fill = "#ffc0cb"   # Exact pink for nodes
        self.arrow_color = "#000000" # Black arrows

        # Theme palettes define all colors for 'pink' and 'dark' modes
        self.themes = {
            "pink": {
                "root_bg": "#ffc0cb",        # page background (soft pink)
                "panel_bg": "#ffffff",       # panel / canvas background (kept white)
                "entry_bg": "#ffffff",
                "entry_fg": "#000000",
                "text_bg": "#ffffff",
                "text_fg": "#000000",
                "button_bg": "#ffc0cb",      # Pink button background
                "button_active": "#ff8aa0",  # hover (darker pink)
                "button_fg": "#000000",      # BUTTON TEXT: black
                "label_fg": "#000000",
                "canvas_bg": "#ffffff",      # FORCE canvas background to white
            },
            "dark": {
                "root_bg": "#121212",        # dark background
                "panel_bg": "#1e1e1e",       # panels slightly lighter
                "entry_bg": "#1e1e1e",
                "entry_fg": "#ffdce6",
                "text_bg": "#1e1e1e",
                "text_fg": "#ffdce6",
                "button_bg": "#000000",      # Black button background
                "button_active": "#444444",
                "button_fg": "#ffc0cb",      # BUTTON TEXT: pink
                "label_fg": "#ffdce6",
                "canvas_bg": "#ffffff",      # FORCE canvas background to white per request
            }
        }

        # Specific color for the activity log text
        self.log_text_color = "#00ff00"  # Bright green

        # --- TTK Styling ---
        # We use ttk.Style to get more control over ttk widget (like button) colors
        self.style = ttk.Style()
        # Configure standard buttons
        self.style.configure("TButton", font=("Helvetica", 11), padding=6, foreground="#000000")
        # Configure a smaller button style for "Switch Theme" and "Clear Log"
        self.style.configure("Small.TButton", font=("Helvetica", 9), padding=4, foreground="#000000")

        # --- Initial UI Build ---
        self.create_main_menu()  # Start the app on the main menu

    # ---------------------------
    # Theme and widget recoloring
    # ---------------------------
    def apply_theme(self):
        """Applies the *current* self.theme to all widgets."""
        t = self.themes[self.theme]  # Get the active theme's color palette

        # Configure the root window's background
        try:
            self.root.configure(bg=t["root_bg"])
        except Exception:
            pass  # Fails silently if window is destroyed

        # Configure the ttk button styles
        try:
            # Configure the 'TButton' style
            self.style.configure("TButton",
                                 background=t["button_bg"],  # Set default background
                                 foreground=t["button_fg"])  # Set default foreground
            self.style.map("TButton",
                           background=[("active", t["button_active"]), ("!active", t["button_bg"])],
                           foreground=[("active", t["button_fg"]), ("!active", t["button_fg"])])
            
            # Configure the 'Small.TButton' style
            self.style.configure("Small.TButton",
                                 background=t["button_bg"],  # Set default background
                                 foreground=t["button_fg"])  # Set default foreground
            self.style.map("Small.TButton",
                           background=[("active", t["button_active"]), ("!active", t["button_bg"])],
                           foreground=[("active", t["button_fg"]), ("!active", t["button_fg"])])
        except Exception:
            pass # Fails silently on some platforms

        # --- Recursive recolor function ---
        # This function walks through all widgets *inside* the current_frame
        # and applies colors one by one. This is needed because ttk styles
        # don't cover all widgets (like tk.Frame, tk.Label, tk.Canvas).
        def recolor(widget):
            cls = widget.winfo_class()  # Get the widget's class name (e.g., "Frame", "Label")
            
            # Frames and Labelframes: use root_bg to blend with the window
            if cls in ("Frame", "Labelframe"):
                try:
                    widget.configure(bg=t["root_bg"])
                except Exception:
                    pass
            # Labels: use root_bg and the theme's label_fg
            if cls == "Label":
                try:
                    widget.configure(bg=t["root_bg"], fg=t["label_fg"])
                except Exception:
                    pass
            # Entries
            if cls == "Entry":
                try:
                    widget.configure(bg=t["entry_bg"], fg=t["entry_fg"], insertbackground=t["entry_fg"])
                except Exception:
                    pass
            # Text widgets
            if cls == "Text":
                try:
                    # Special Case: Activity Log (green text)
                    if hasattr(self, "log_box") and widget is self.log_box:
                        widget.configure(bg=t["text_bg"], fg=self.log_text_color, insertbackground=t["entry_fg"])
                    # Special Case: Output Box (forced white/black)
                    elif hasattr(self, "output_box") and widget is self.output_box:
                        widget.configure(bg="#ffffff", fg="#000000", insertbackground="#000000")
                    # All other text widgets
                    else:
                        widget.configure(bg=t["text_bg"], fg=t["text_fg"], insertbackground=t["entry_fg"])
                except Exception:
                    pass
            # Canvas: force white background
            if cls == "Canvas":
                try:
                    widget.configure(bg="#ffffff")
                except Exception:
                    pass
            
            # Recursively call this function for all children
            for child in widget.winfo_children():
                recolor(child)

        # Start the recursive recoloring on the main frame
        if self.current_frame:
            recolor(self.current_frame)

    # ---------------------------
    # UI builders
    # ---------------------------
    def clear_window(self):
        """Destroys the current_frame to make way for a new one."""
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def create_header(self, parent, title_text, show_switch=True):
        """Creates the top header bar with a title and optional theme switch."""
        # 'parent' is the frame this header will be packed into
        header = tk.Frame(parent)
        header.pack(fill="x", pady=(12, 0), padx=12)
        
        lbl = tk.Label(header, text=title_text, font=("Helvetica", 18, "bold"))
        lbl.pack(side="left")
        
        # Only show the "Switch Theme" button if 'show_switch' is True
        # (Used on main menu, hidden on list menu)
        if show_switch:
            btn = ttk.Button(header, text="Switch Theme", command=self.switch_theme, style="Small.TButton")
            btn.pack(side="right")
        return header

    def create_main_menu(self):
        """Builds the main menu UI (the screen with 3 list-type buttons)."""
        # Clear the old frame (if any)
        self.clear_window()
        # Create the new main frame
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(expand=True, fill="both")

        # Create the header, passing 'show_switch=True'
        self.create_header(self.current_frame, "LINKED LIST VISUALIZER", show_switch=True)

        tk.Label(self.current_frame, text="Select a Linked List Type:",
                 font=("Helvetica", 14)).pack(pady=20)

        # Define the buttons and the classes they will create
        for text, cls in [("Singly Linked List", SinglyLinkedList),
                          ("Doubly Linked List", DoublyLinkedList),
                          ("Circular Linked List", CircularLinkedList)]:
            # Use a lambda function to "capture" the correct class (c) and text (t)
            # for each button's command
            btn = ttk.Button(self.current_frame, text=text,
                             command=lambda c=cls, t=text: self.setup_list(c, t))
            btn.pack(pady=8, ipadx=10, ipady=5)

        # Apply the current theme to all new widgets
        self.apply_theme()
        # Restore the persistent log history to the log_box (if it exists, which it doesn't here)
        self._restore_logs_to_widget_if_present()

    def setup_list(self, list_class, list_type):
        """
        Transition function called when a list type is selected.
        It creates the new list *object* and builds the list menu.
        """
        # Create a new, empty instance of the *selected* list class
        self.linked_list = list_class()
        self.list_type = list_type  # Store the name (e.g., "Singly Linked List")
        self.create_list_menu(list_type)  # Build the next screen

    def create_list_menu(self, list_type):
        """Builds the main list operations UI (entries, buttons, canvas, logs)."""
        self.clear_window()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(expand=True, fill="both")

        # Create header, passing 'show_switch=False'
        self.create_header(self.current_frame, list_type.upper(), show_switch=False)

        # --- Entry Frame (Value and Position) ---
        entry_frame = tk.Frame(self.current_frame)
        entry_frame.pack(pady=10)
        tk.Label(entry_frame, text="Value:").grid(row=0, column=0, padx=5)
        self.value_entry = tk.Entry(entry_frame, width=28, bd=1, relief="solid", font=("Helvetica", 11))
        self.value_entry.grid(row=0, column=1, padx=5)

        tk.Label(entry_frame, text="Position (optional):").grid(row=1, column=0, padx=5)
        self.pos_entry = tk.Entry(entry_frame, width=28, bd=1, relief="solid", font=("Helvetica", 11))
        self.pos_entry.grid(row=1, column=1, padx=5, pady=5)

        # Bind a key-release event to the entries: if the user types,
        # hide the (now outdated) visualization.
        self.value_entry.bind("<KeyRelease>", lambda e: self.clear_visual(keep_logs=True))
        self.pos_entry.bind("<KeyRelease>", lambda e: self.clear_visual(keep_logs=True))

        # --- Button Frame (Operations) ---
        btn_frame = tk.Frame(self.current_frame)
        btn_frame.pack(pady=10)

        # Button definitions: (Text, command_function)
        buttons = [
            ("Append", self.append_value),
            ("Prepend", self.prepend_value),
            ("Insert", self.insert_value),
            ("Delete", self.delete_value),
            ("Random", self.random_nodes),
            ("Clear List", self.clear_list),
            ("Back", self.create_main_menu)
        ]

        # Create buttons in a grid (4 per row)
        for i, (txt, cmd) in enumerate(buttons):
            btn = ttk.Button(btn_frame, text=txt, command=cmd, width=14)
            btn.grid(row=i // 4, column=i % 4, padx=8, pady=5)

        # --- Canvas (for visualization) ---
        self.canvas = tk.Canvas(self.current_frame, width=900, height=360, highlightthickness=0, bg="#ffffff")
        self.canvas.pack(pady=6)

        # --- Output Box (for text display) ---
        self.output_box = tk.Text(self.current_frame, height=4, width=95, state="disabled", wrap="word",
                                  bd=1, relief="solid", font=("Helvetica", 11), bg="#ffffff", fg="#000000", insertbackground="#000000")
        self.output_box.pack(pady=6)

        # --- Activity Log (Label + Button) ---
        log_label_row = tk.Frame(self.current_frame)
        log_label_row.pack(fill="x", padx=20)
        tk.Label(log_label_row, text="Activity Log:").pack(side="left", anchor="w")
        # Place "Clear Log" button on the right side of this row
        ttk.Button(log_label_row, text="Clear Log (All History)", command=self.clear_log, style="Small.TButton").pack(side="right")

        # --- Activity Log (Text Box + Scrollbar) ---
        log_frame = tk.Frame(self.current_frame)
        log_frame.pack(fill="both", expand=False, padx=20, pady=(4, 6))
        self.log_box = tk.Text(log_frame, height=8, width=95, state="disabled", wrap="word",
                               bd=1, relief="solid", font=("Helvetica", 11))
        self.log_box.pack(side="left", fill="both", expand=True)
        # Add a scrollbar linked to the log_box
        log_scroll = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_box.yview)
        log_scroll.pack(side="right", fill="y")
        self.log_box['yscrollcommand'] = log_scroll.set

        # --- Finalize UI ---
        # Apply theme to all the newly created widgets
        self.apply_theme()
        # Restore the persistent log history to the new log_box
        self._restore_logs_to_widget_if_present()


    # ---------------------------
    # Log handling (persistent)
    # ---------------------------
    def append_log(self, message):
        """Adds a timestamped message to the log_history AND the log_box widget."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        
        # Add to the persistent list
        self.log_history.append(entry)
        
        # Add to the visual widget (if it exists)
        if hasattr(self, "log_box") and self.log_box:
            try:
                self.log_box.config(state="normal")  # Must be 'normal' to edit
                self.log_box.insert(tk.END, entry + "\n")
                self.log_box.see(tk.END)  # Auto-scroll to the bottom
                self.log_box.config(state="disabled") # Set back to read-only
            except Exception:
                pass  # Fails silently if widget is destroyed

    def _restore_logs_to_widget_if_present(self):
        """Populates the log_box widget from the persistent log_history list."""
        if hasattr(self, "log_box") and self.log_box:
            try:
                self.log_box.config(state="normal")
                self.log_box.delete("1.0", tk.END)  # Clear current contents
                for e in self.log_history:  # Loop through persistent history
                    self.log_box.insert(tk.END, e + "\n")
                self.log_box.see(tk.END)  # Scroll to bottom
                self.log_box.config(state="disabled")
            except Exception:
                pass

    def clear_log(self):
        """Clears *all* log history, both persistent and visual."""
        # Clear the persistent data
        self.log_history = []
        # Clear the visual widget
        if hasattr(self, "log_box") and self.log_box:
            try:
                self.log_box.config(state="normal")
                self.log_box.delete("1.0", tk.END)
                self.log_box.config(state="disabled")
            except Exception:
                pass

    # ---------------------------
    # Linked list operations (Button commands)
    # ---------------------------
    def clear_visual(self, keep_logs=False):
        """Hides the visualization and clears the output box."""
        # Clear the canvas
        try:
            if hasattr(self, "canvas") and self.canvas:
                self.canvas.delete("all")
        except Exception:
            pass
        # Clear the text output box
        if hasattr(self, "output_box") and self.output_box:
            try:
                self.output_box.config(state="normal")
                self.output_box.delete("1.0", tk.END)
                self.output_box.config(state="disabled")
            except Exception:
                pass
        
        # 'keep_logs' is True when called from a key-release
        if not keep_logs:
            pass # Logs are only cleared by the 'Clear Log' button

    def append_value(self):
        """Command for the 'Append' button."""
        val_str = self.value_entry.get().strip()
        if not val_str:
            return messagebox.showwarning("Warning", "Enter a value!")
        
        try:
            val = int(val_str)  # Convert value to an integer
        except ValueError:
            return messagebox.showwarning("Invalid Input", "Value must be an integer.")

        self.linked_list.append(val)  # Call the list object's method
        self.display_list()  # [CHANGED] Refresh the display
        self.append_log(f"Appended value {val} to {self.list_type}.")

    def prepend_value(self):
        """Command for the 'Prepend' button."""
        val_str = self.value_entry.get().strip()
        if not val_str:
            return messagebox.showwarning("Warning", "Enter a value!")

        try:
            val = int(val_str)  # Convert value to an integer
        except ValueError:
            return messagebox.showwarning("Invalid Input", "Value must be an integer.")

        self.linked_list.prepend(val)
        self.display_list()  # [CHANGED] Refresh the display
        self.append_log(f"Prepended value {val} to {self.list_type}.")

    def insert_value(self):
        """Command for the 'Insert' button."""
        val_str = self.value_entry.get().strip()
        pos_text = self.pos_entry.get().strip()
        
        if not val_str:
            return messagebox.showwarning("Warning", "Enter a value!")

        try:
            val = int(val_str)  # Convert value to an integer
        except ValueError:
            return messagebox.showwarning("Invalid Input", "Value must be an integer.")

        try:
            # Default to position 1 if 'pos' is empty
            pos = int(pos_text) if pos_text else 1
            if pos < 1:
                pos = 1  # Treat negative numbers as 1
        except ValueError:
            # Show warning if position is invalid text
            messagebox.showwarning("Invalid Input", "Position must be an integer. Defaulting to 1.")
            pos = 1  
        
        self.linked_list.insert_at_position(pos, val)
        self.display_list()  # [CHANGED] Refresh the display
        self.append_log(f"Inserted value {val} at position {pos} in {self.list_type}.")

    def delete_value(self):
        """Command for the 'Delete' button."""
        val_str = self.value_entry.get().strip()
        if not val_str:
            return messagebox.showwarning("Warning", "Enter a value to delete!")
        
        try:
            val = int(val_str)  # Convert value to an integer
        except ValueError:
            return messagebox.showwarning("Invalid Input", "Value to delete must be an integer.")

        # The delete method returns a message if it fails (e.g., "not found")
        msg = self.linked_list.delete_by_value(val)
        
        if msg:
            # If there was an error, show it
            messagebox.showinfo("Info", msg)
            self.append_log(f"Attempted to delete {val} from {self.list_type}: {msg}")
        else:
            # If 'msg' is None, it was successful
            self.append_log(f"Deleted value {val} from {self.list_type}.")
        self.display_list()  # [CHANGED] Refresh the display

    def random_nodes(self):
        """Command for the 'Random' button."""
        if not self.linked_list:
            return
        # Ask user how many nodes to create
        count = simpledialog.askinteger("Random nodes", "How many random nodes to create?", initialvalue=5, minvalue=1, maxvalue=100)
        if count is None:
            return  # User clicked 'Cancel'
        
        for _ in range(count):
            val = random.randint(0, 999)  # Create random integer
            self.linked_list.append(val)
            
        self.display_list()  # [CHANGED] Refresh the display
        self.append_log(f"Added {count} random node(s) to {self.list_type}.") # [CHANGED] Updated log

    def clear_list(self):
        """Command for the 'Clear List' button."""
        if self.linked_list:
            self.linked_list.clear()  # Empty the backend list
        self.display_list()  # [CHANGED] Refresh the display (will show "List is empty")
        self.append_log(f"Cleared all nodes from {self.list_type}.")

    # ---------------------------
    # Theme switching (from main menu)
    # ---------------------------
    def switch_theme(self):
        """Command for the 'Switch Theme' button."""
        # Toggle the theme state variable
        self.theme = "dark" if self.theme == "pink" else "pink"

        # Rebuild the *main menu* entirely. This is the simplest
        # way to apply the new theme to everything.
        self.create_main_menu()

        # Log the action
        self.append_log(f"Theme switched to {self.theme}.")

    # ---------------------------
    # Display toggle and drawing
    # ---------------------------
    
    def display_list(self):
        """Fetches list data and calls the drawing function."""
        # Get the list of node values (e.g., ['10', '20', '30'])
        nodes = self.linked_list.get_nodes() if self.linked_list else []
        # Get the string representation (e.g., "10 -> 20 -> 30")
        text = self.linked_list.display() if self.linked_list else "List is empty."
        
        # Populate the text output box
        if hasattr(self, "output_box") and self.output_box:
            try:
                self.output_box.config(state="normal")
                self.output_box.delete("1.0", tk.END)
                self.output_box.insert(tk.END, text)
                self.output_box.config(state="disabled")
            except Exception:
                pass # Fail silently
            
        # Call the canvas drawing function
        self.animate_nodes(nodes)

    def animate_nodes(self, nodes):
        """The main drawing function. Renders nodes and arrows on the canvas."""
        canvas = getattr(self, "canvas", None)
        if not canvas:
            return  # Safety check
        
        try:
            canvas.delete("all")  # Clear previous drawings
            canvas.configure(bg="#ffffff")  # Ensure canvas is white
        except Exception:
            pass

        if not nodes:
            # Show message if list is empty
            try:
                canvas.create_text(450, 180, text="List is empty.",
                                   font=("Helvetica", 14, "italic"),
                                   fill="#000000")
            except Exception:
                pass
            return

        # --- Layout Parameters ---
        x_start, y = 60, 180  # Starting X, and constant Y
        node_d = 60           # Diameter of the node circle
        spacing = 40          # Space between nodes
        
        # Calculate total width to center the drawing
        total_w = len(nodes) * node_d + (len(nodes) - 1) * spacing
        # Start 'x' so the whole drawing is centered in the 900px canvas
        x = max(60, (900 - total_w) // 2)

        centers = []  # Store the (x, y) center of each node
        
        try:
            # --- Draw Nodes and Text ---
            for i, val in enumerate(nodes):
                # Calculate the *center* of the circle
                cx = x + i * (node_d + spacing) + node_d // 2
                cy = y
                centers.append((cx, cy))
                
                # Draw the circle (oval)
                outline_color = "#000000"
                canvas.create_oval(cx - node_d // 2, cy - node_d // 2, cx + node_d // 2, cy + node_d // 2,
                                   fill=self.node_fill, outline=outline_color, width=2)
                # Draw the value text inside the circle
                canvas.create_text(cx, cy, text=val, fill="#000000", font=("Helvetica", 12, "bold"))

            # --- Draw Forward Arrows (Singly, Doubly, Circular) ---
            for i in range(len(centers) - 1):
                x1, y1 = centers[i]   # Center of node i
                x2, y2 = centers[i+1] # Center of node i+1
                # Draw line from right-edge of node i to left-edge of node i+1
                canvas.create_line(x1 + node_d // 2, y1, x2 - node_d // 2, y2,
                                   arrow=tk.LAST, width=2, fill=self.arrow_color)

            # --- Draw Back Arrows (Doubly Only) ---
            if self.list_type == "Doubly Linked List" and len(centers) > 1:
                for i in range(len(centers) - 1):
                    x1, y1 = centers[i]
                    x2, y2 = centers[i + 1]
                    # Draw a slightly offset, dashed line pointing backwards
                    canvas.create_line(x2 - node_d // 2, y2 + 12, x1 + node_d // 2, y1 + 12,
                                       arrow=tk.LAST, dash=(4, 3), width=2, fill=self.arrow_color)

            # --- Draw Circular Arrow (Circular Only) ---
            if self.list_type == "Circular Linked List" and len(centers) > 1:
                x_first, y_first = centers[0]
                x_last, y_last = centers[-1]
                top = y - 80  # How high the arc goes
                # Draw a 4-point smooth, dashed line from last node back to first
                canvas.create_line(x_last + node_d // 2, y_last,   # Point 1: Edge of last node
                                   x_last + node_d // 2 + 20, top, # Point 2: Control point
                                   x_first - node_d // 2 - 20, top, # Point 3: Control point
                                   x_first - node_d // 2, y_first, # Point 4: Edge of first node
                                   smooth=True, width=2, arrow=tk.LAST, dash=(4, 3), fill=self.arrow_color)
                # Add text label for the arc
                canvas.create_text((x_first + x_last) / 2, top - 12,
                                   text="(back to head)", fill="#000000", font=("Helvetica", 10, "italic"))

            # --- Annotate Head and Tail ---
            if centers:
                hx, hy = centers[0]
                canvas.create_text(hx, hy - node_d // 2 - 10, text="HEAD", fill="#000000", font=("Helvetica", 9, "bold"))
                tx, ty = centers[-1]
                canvas.create_text(tx, ty + node_d // 2 + 12, text="TAIL", fill="#000000", font=("Helvetica", 9, "bold"))
        except Exception:
            pass # Fail silently if canvas is destroyed mid-draw

# -------------------------------
# Main execution
# (This code runs only when the file is executed as a script)
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()           # Create the main application window
    app = LinkedListGUI(root) # Create an instance of our GUI class
    root.mainloop()          # Start the tkinter event loop (waits for user input)