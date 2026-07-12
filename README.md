# File Separator

A simple Python desktop application built with **Tkinter** that automatically organizes files into folders based on their file extensions.
Instead of manually sorting files, this application scans a selected folder, detects each file's extension, creates a folder for that extension (only if needed),
and moves the files into their respective folders.

## Features

* Automatically separates files by their extension.
* Supports **all file types** (e.g., `.jpg`, `.png`, `.pdf`, `.docx`, `.xlsx`, `.mp4`, `.mp3`, `.zip`, etc.).
* Creates folders **only when that file type exists**.
* Leaves files without an extension untouched.
* Displays a live log showing every file that is moved.
* Shows a summary of moved and skipped files after completion.
* Simple and user-friendly graphical interface built with Tkinter.

## Example

### Before

```
Downloads/
│
├── photo.jpg
├── report.pdf
├── song.mp3
├── movie.mp4
├── notes.docx
├── archive.zip
└── presentation.pptx
```

### After

```
Downloads/
│
├── JPG/
│   └── photo.jpg
│
├── PDF/
│   └── report.pdf
│
├── MP3/
│   └── song.mp3
│
├── MP4/
│   └── movie.mp4
│
├── DOCX/
│   └── notes.docx
│
├── ZIP/
│   └── archive.zip
│
└── PPTX/
    └── presentation.pptx
```


## Author

**Aman Jain**

Python Desktop Application using Tkinter for automatic file organization.

---

## License

This project is open source and available to all.
