import json
import tkinter as tk
from tkinter import filedialog, messagebox


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


root = tk.Tk()
root.title("JSON Formatter")
root.geometry("1000x600")
root.minsize(900, 500)

# Button bar
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, padx=10, pady=10)

format_button = tk.Button(button_frame, text="Format / Beautify", command=format_json)
minify_button = tk.Button(button_frame, text="Minify", command=minify_json)
copy_button = tk.Button(button_frame, text="Copy Output", command=copy_output)
clear_button = tk.Button(button_frame, text="Clear", command=clear_text)
load_button = tk.Button(button_frame, text="Load from File (.json)", command=load_from_file)
save_button = tk.Button(button_frame, text="Save Output to File", command=save_output_to_file)

format_button.pack(side=tk.LEFT, padx=5)
minify_button.pack(side=tk.LEFT, padx=5)
copy_button.pack(side=tk.LEFT, padx=5)
clear_button.pack(side=tk.LEFT, padx=5)
load_button.pack(side=tk.LEFT, padx=5)
save_button.pack(side=tk.LEFT, padx=5)

# Text areas
text_frame = tk.Frame(root)
text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

input_frame = tk.LabelFrame(text_frame, text="Input JSON")
output_frame = tk.LabelFrame(text_frame, text="Formatted Output")

input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
output_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

input_scrollbar = tk.Scrollbar(input_frame)
input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_scrollbar = tk.Scrollbar(output_frame)
output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

input_text = tk.Text(input_frame, wrap=tk.NONE, yscrollcommand=input_scrollbar.set)
output_text = tk.Text(output_frame, wrap=tk.NONE, yscrollcommand=output_scrollbar.set)

input_text.pack(fill=tk.BOTH, expand=True)
output_text.pack(fill=tk.BOTH, expand=True)

input_scrollbar.config(command=input_text.yview)
output_scrollbar.config(command=output_text.yview)

root.mainloop()
