import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP_TITLE = "JSON Formatter"
UI_FONT = ("Segoe UI", 10)
MONO_FONT = ("Consolas", 11)


def format_json():
    """Pretty-print JSON from input to output."""
    raw_text = input_text.get("1.0", tk.END).strip()
    if not raw_text:
        messagebox.showwarning("No Input", "Please enter JSON to format.")
        return
    try:
        parsed = json.loads(raw_text)
        formatted = json.dumps(parsed, indent=4, ensure_ascii=False)
        set_output(formatted)
    except json.JSONDecodeError as exc:
        show_json_error(exc)


def minify_json():
    """Minify JSON from input to output."""
    raw_text = input_text.get("1.0", tk.END).strip()
    if not raw_text:
        messagebox.showwarning("No Input", "Please enter JSON to minify.")
        return
    try:
        parsed = json.loads(raw_text)
        minified = json.dumps(parsed, separators=(",", ":"), ensure_ascii=False)
        set_output(minified)
    except json.JSONDecodeError as exc:
        show_json_error(exc)


def copy_output():
    """Copy output text to clipboard."""
    output_data = output_text.get("1.0", tk.END).strip()
    if not output_data:
        messagebox.showwarning("No Output", "There is no output to copy.")
        return
    root.clipboard_clear()
    root.clipboard_append(output_data)
    messagebox.showinfo("Copied", "Formatted JSON copied to clipboard.")


def clear_text():
    """Clear input and output text boxes."""
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)


def load_from_file():
    """Load JSON content from a file into the input box."""
    file_path = filedialog.askopenfilename(
        title="Open JSON File",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*")],
    )
    if not file_path:
        return
    try:
        with open(file_path, "r", encoding="utf-8") as file_handle:
            content = file_handle.read()
        input_text.delete("1.0", tk.END)
        input_text.insert(tk.END, content)
    except OSError as exc:
        messagebox.showerror("File Error", f"Unable to open file.\n{exc}")


def save_output_to_file():
    """Save output content to a JSON file."""
    output_data = output_text.get("1.0", tk.END).strip()
    if not output_data:
        messagebox.showwarning("No Output", "There is no output to save.")
        return
    file_path = filedialog.asksaveasfilename(
        title="Save JSON File",
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*")],
    )
    if not file_path:
        return
    try:
        with open(file_path, "w", encoding="utf-8") as file_handle:
            file_handle.write(output_data)
        messagebox.showinfo("Saved", "Output saved successfully.")
    except OSError as exc:
        messagebox.showerror("File Error", f"Unable to save file.\n{exc}")


def show_json_error(exc: json.JSONDecodeError):
    """Show JSON parsing error with line and column."""
    messagebox.showerror(
        "Invalid JSON",
        f"Error: {exc.msg}\nLine: {exc.lineno}, Column: {exc.colno}",
    )


def set_output(content: str):
    """Replace output box text with provided content."""
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, content)
    set_status("Output updated.")


def view_tree():
    """Open a tree view window for the output JSON."""
    output_data = output_text.get("1.0", tk.END).strip()
    if not output_data:
        messagebox.showwarning("No Output", "There is no output to view.")
        return
    try:
        parsed = json.loads(output_data)
    except json.JSONDecodeError as exc:
        show_json_error(exc)
        return

    tree_window = tk.Toplevel(root)
    tree_window.title("JSON Tree View")
    tree_window.geometry("600x500")

    tree_frame = tk.Frame(tree_window)
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tree_scroll = tk.Scrollbar(tree_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
    tree.pack(fill=tk.BOTH, expand=True)
    tree_scroll.config(command=tree.yview)

    def insert_node(parent, key, value):
        if isinstance(value, dict):
            node_id = tree.insert(parent, tk.END, text=str(key), open=False)
            for child_key, child_value in value.items():
                insert_node(node_id, child_key, child_value)
        elif isinstance(value, list):
            node_id = tree.insert(parent, tk.END, text=str(key), open=False)
            for index, item in enumerate(value):
                insert_node(node_id, f"[{index}]", item)
        else:
            display = f"{key}: {value}"
            tree.insert(parent, tk.END, text=display, open=False)

    insert_node("", "root", parsed)


def apply_theme(theme_name: str):
    """Apply a simple theme to the UI."""
    if theme_name == "Dark":
        background = "#1f2a30"
        foreground = "#e9f1f2"
        frame_bg = "#24333a"
        accent = "#14b8a6"
        button_bg = "#2b3b42"
        border = "#0f1f25"
    else:
        background = "#ffffff"
        foreground = "#1f2933"
        frame_bg = "#f4f7f9"
        accent = "#0ea5a8"
        button_bg = "#e7ecef"
        border = "#d5dadd"

    root.configure(bg=frame_bg)
    nav_frame.configure(bg=border)
    button_frame.configure(bg=frame_bg)
    text_frame.configure(bg=frame_bg)
    input_frame.configure(bg=frame_bg, fg=foreground)
    output_frame.configure(bg=frame_bg, fg=foreground)
    theme_label.configure(bg=frame_bg, fg=foreground)
    status_frame.configure(bg=frame_bg)
    status_label.configure(bg=frame_bg, fg=foreground)
    action_panel.configure(bg=frame_bg)
    left_panel.configure(bg=frame_bg)
    right_panel.configure(bg=frame_bg)
    brand_label.configure(bg=border, fg=accent)

    for button in button_frame.winfo_children():
        if isinstance(button, tk.Button):
            button.configure(bg=button_bg, fg=foreground, activebackground=frame_bg)

    for button in output_button_frame.winfo_children():
        if isinstance(button, tk.Button):
            button.configure(bg=button_bg, fg=foreground, activebackground=frame_bg)

    for button in action_panel.winfo_children():
        if isinstance(button, tk.Button):
            button.configure(
                bg=accent,
                fg="#ffffff",
                activebackground=accent,
                activeforeground="#ffffff",
            )

    input_text.configure(
        bg=background,
        fg=foreground,
        insertbackground=foreground,
        font=MONO_FONT,
    )
    output_text.configure(
        bg=background,
        fg=foreground,
        insertbackground=foreground,
        font=MONO_FONT,
    )


def on_close():
    """Handle application close event."""
    if messagebox.askokcancel("Quit", "Do you want to close the JSON Formatter?"):
        root.destroy()


def set_status(message: str):
    """Update the status bar message."""
    status_var.set(message)


root = tk.Tk()
root.title(APP_TITLE)
root.geometry("1200x700")
root.minsize(900, 500)
root.protocol("WM_DELETE_WINDOW", on_close)
root.option_add("*Font", UI_FONT)

# Top navigation bar
nav_frame = tk.Frame(root)
nav_frame.pack(fill=tk.X)

brand_label = tk.Label(nav_frame, text="{ JSON Formatter }", font=("Segoe UI", 12, "bold"))
brand_label.pack(side=tk.LEFT, padx=15, pady=8)

# Button bar
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, padx=15, pady=(10, 5))

clear_button = tk.Button(button_frame, text="Clear", command=clear_text)
save_button = tk.Button(button_frame, text="Save Output", command=save_output_to_file)
tree_button = tk.Button(button_frame, text="Tree View", command=view_tree)

clear_button.pack(side=tk.LEFT, padx=5)
save_button.pack(side=tk.LEFT, padx=5)
tree_button.pack(side=tk.LEFT, padx=5)

theme_label = tk.Label(button_frame, text="Theme:")
theme_label.pack(side=tk.LEFT, padx=(20, 5))
theme_choice = tk.StringVar(value="Light")
theme_menu = ttk.Combobox(
    button_frame,
    textvariable=theme_choice,
    values=["Light", "Dark"],
    width=8,
    state="readonly",
)
theme_menu.pack(side=tk.LEFT, padx=5)

# Text areas with adjustable pane
text_frame = tk.Frame(root)
text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))

content_frame = tk.Frame(text_frame)
content_frame.pack(fill=tk.BOTH, expand=True)

paned = tk.PanedWindow(content_frame, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
paned.pack(fill=tk.BOTH, expand=True)

left_panel = tk.Frame(paned)
right_panel = tk.Frame(paned)

paned.add(left_panel, stretch="always")
paned.add(right_panel, stretch="always")

input_frame = tk.LabelFrame(left_panel, text="Input JSON")
input_frame.pack(fill=tk.BOTH, expand=True)

action_panel = tk.Frame(left_panel)
action_panel.pack(fill=tk.X, pady=10)

upload_button = tk.Button(action_panel, text="Upload Data", command=load_from_file)
validate_button = tk.Button(action_panel, text="Validate", command=format_json)
format_action_button = tk.Button(action_panel, text="Format / Beautify", command=format_json)
minify_action_button = tk.Button(action_panel, text="Minify / Compact", command=minify_json)

upload_button.pack(fill=tk.X, pady=4)
validate_button.pack(fill=tk.X, pady=4)
format_action_button.pack(fill=tk.X, pady=4)
minify_action_button.pack(fill=tk.X, pady=4)

output_frame = tk.LabelFrame(right_panel, text="Formatted Output")
output_frame.pack(fill=tk.BOTH, expand=True)

output_text_frame = tk.Frame(output_frame)

output_button_frame = tk.Frame(output_frame)
output_button_frame.pack(fill=tk.X, padx=5, pady=5)

copy_button = tk.Button(output_button_frame, text="Copy Output", command=copy_output)
fold_button = tk.Button(
    output_button_frame,
    text="Fold Output",
    command=lambda: output_text_frame.pack_forget(),
)
unfold_button = tk.Button(
    output_button_frame,
    text="Unfold Output",
    command=lambda: output_text_frame.pack(fill=tk.BOTH, expand=True),
)

copy_button.pack(side=tk.LEFT, padx=5)
fold_button.pack(side=tk.LEFT, padx=5)
unfold_button.pack(side=tk.LEFT, padx=5)

input_scrollbar = tk.Scrollbar(input_frame)
input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

input_text = tk.Text(input_frame, wrap=tk.NONE, yscrollcommand=input_scrollbar.set)
input_text.pack(fill=tk.BOTH, expand=True)

input_scrollbar.config(command=input_text.yview)

output_text_frame.pack(fill=tk.BOTH, expand=True)

output_scrollbar = tk.Scrollbar(output_text_frame)
output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text = tk.Text(output_text_frame, wrap=tk.NONE, yscrollcommand=output_scrollbar.set)
output_text.pack(fill=tk.BOTH, expand=True)

output_scrollbar.config(command=output_text.yview)

# Status bar
status_var = tk.StringVar(value="Ready")
status_frame = tk.Frame(root)
status_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
status_label = tk.Label(status_frame, textvariable=status_var, anchor="w")
status_label.pack(fill=tk.X)

theme_menu.bind("<<ComboboxSelected>>", lambda event: apply_theme(theme_choice.get()))
apply_theme(theme_choice.get())
set_status("Ready")

root.mainloop()
