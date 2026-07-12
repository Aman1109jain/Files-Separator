import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def separate_files(source_dir: str, log_callback=None):
    moved_counts = {}   # Dictionary to tell how many different files were there and how many of each type were moved
    skipped = 0         # Skips files with no extension

    for filename in os.listdir(source_dir):
        filepath = os.path.join(source_dir, filename)

        # If the item is not a file
        if not os.path.isfile(filepath):
            continue

        ext = os.path.splitext(filename)[1].lower()     # Make the extension lowercase

        # Skip files with no extension
        if ext == "":
            skipped += 1
            if log_callback:
                log_callback(f"[SKIP] No extension: {filename}", "skip")
            continue
        
        # Till here we only separate the files

        # Makes the folder name as the extension in Uppercase without dot
        folder_name = ext[1:].upper()

        destination_folder = os.path.join(source_dir, folder_name)

        # Create folder only when there is a file of that type
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Move the files
        shutil.move(filepath, os.path.join(destination_folder, filename))

        moved_counts[folder_name] = moved_counts.get(folder_name, 0) + 1

        if log_callback:
            log_callback(f"[{folder_name}] Moved: {filename}", "info")

    return moved_counts, skipped


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Separator")
        self.geometry("620x480")
        self.configure(bg="#000000")
        self._build_ui()

    def _build_ui(self):
        # __Title__
        tk.Label(self, 
                 text="File Separator",
                 font=("Helvetica", 16, "bold"),
                 bg="#000000",
                 fg="#ffffff"
                 ).pack(pady=(20, 4))
        
        tk.Label(self,
                 text="Select a folder and separate files automatically.",
                 font=("Helvetica", 10),
                 bg="#000000",
                 fg="#ffffff"
                 ).pack(pady=(0, 16))

        # __Folder picker__
        frame = tk.Frame(self, bg="#000000")
        frame.pack(fill="x", padx=30)

        self.folder_var = tk.StringVar(value="No folder selected")

        tk.Entry(frame,
                 textvariable=self.folder_var,
                 font=("Helvetica", 10),
                 state="readonly",
                 readonlybackground="#fff",
                 relief="solid",
                 bd=1, width=52
                 ).pack(side="left", ipady=5)
        
        tk.Button(frame,
                  text="Browse",
                  command=self._browse,
                  font=("Helvetica", 10),
                  bg="#4a90d9",
                  fg="white",
                  activebackground="#357abd",
                  relief="flat",
                  padx=12,
                  pady=5,
                  cursor="hand2"
                  ).pack(side="left", padx=(8, 0))

        # __Run button_
        tk.Button(self,
                  text="▶  Separate Files",
                  command=self._run,
                  font=("Helvetica", 11, "bold"),
                  bg="#27ae60", fg="white",
                  activebackground="#1e8449",
                  relief="flat",
                  padx=20,
                  pady=8,
                  cursor="hand2"
                  ).pack(pady=16)

        # __Log area__
        log_frame = tk.Frame(self, bg="#f5f5f5")
        log_frame.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        self.log = tk.Text(log_frame,
                           font=("Courier", 9),
                           bg="#1e1e1e", 
                           fg="#d4d4d4",
                           relief="flat",
                           state="disabled", 
                           wrap="word",
                           bd=0)
        
        self.log.pack(side="left",
                      fill="both",
                      expand=True)

        scroll = ttk.Scrollbar(log_frame, command=self.log.yview)
        scroll.pack(side="right", fill="y")
        self.log.config(yscrollcommand=scroll.set)

        # __Tag Colours__
        self.log.tag_config("jpg",  foreground="#6fc1ff")
        self.log.tag_config("mp4",  foreground="#c586c0")
        self.log.tag_config("skip", foreground="#808080")
        self.log.tag_config("info", foreground="#4ec9b0")
        self.log.tag_config("err",  foreground="#f44747")

        # __Status bar__
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self,
                 textvariable=self.status_var,
                 font=("Helvetica", 9),
                 bg="#dce0e8", fg="#333", 
                 anchor="w", 
                 padx=10
                 ).pack(fill="x", side="bottom", ipady=4)

    def _browse(self):
        folder = filedialog.askdirectory(title="Select folder with files")
        if folder:
            self.folder_var.set(folder)
            self.status_var.set(f"Folder selected: {folder}")

    def _log(self, message, tag="info"):
        self.log.config(state="normal")
        self.log.insert("end", message + "\n", tag)
        self.log.see("end")
        self.log.config(state="disabled")

    def _run(self):
        source = self.folder_var.get()

        if source == "No folder selected" or not os.path.isdir(source):
            messagebox.showerror("Error", "Please select a valid folder first.")
            return

        # Clear log
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")

        self._log(f"Starting in: {source}", "info")
        self._log("─" * 60, "info")

        try:
            moved_counts, skipped = separate_files(source, self._log)
        except Exception as e:
            self._log(f"ERROR: {e}", "err")
            self.status_var.set("An error occurred.")
            return

        self._log("─" * 60, "info")

        summary = []
        for ext in sorted(moved_counts):
            line = f"{ext}: {moved_counts[ext]}"
            summary.append(line)
            self._log(line, "info")

        self._log(f"Skipped: {skipped}", "skip")

        self.status_var.set("Completed")

        messagebox.showinfo(
            "Done",
            "File separation completed!\n\n"
            + "\n".join(summary)
            + f"\n\nSkipped: {skipped}"
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()