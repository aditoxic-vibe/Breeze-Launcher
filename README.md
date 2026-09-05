# 🌬️ Breeze Launcher

A lightweight, modern Linux application launcher designed to be fast, clean and easy to customize.

Breeze Launcher aims to work across many Linux distributions without requiring a specific desktop environment.

## ✨ Features

* 🚀 Fast application launcher
* 🔎 Application search
* 🎨 Modern customizable interface
* 🧩 Cinnamon-friendly
* 🐧 Designed for multiple Linux distributions
* 💻 Works with common Linux desktop environments
* ⚙️ Easy to modify
* 📦 Open source
* 🪶 Lightweight design

## 🐧 Supported Linux distributions

Breeze Launcher is designed to work on most Linux distributions that provide Python 3 and the required GUI dependencies.

Tested/targeted distributions include:

* Arch Linux
* Fedora
* Debian
* Ubuntu
* Linux Mint
* Pop!_OS
* openSUSE
* Other Linux distributions with compatible Python dependencies

> Breeze Launcher is not tied to `apt`, so the installation commands depend on your distribution.

---

# 📥 Installation

## 1. Clone the repository

```bash
git clone https://github.com/aditoxic-vibe/Breeze-Launcher.git
cd Breeze-Launcher
```

## 2. Check Python

Make sure Python 3 is installed:

```bash
python3 --version
```

If Python is installed, continue to the next step.

---

# 📦 Dependencies

Breeze Launcher requires Python 3 and the GUI libraries used by the launcher.

### Arch Linux

```bash
sudo pacman -S python
```

### Fedora

```bash
sudo dnf install python3
```

### Debian / Ubuntu / Linux Mint / Pop!_OS

```bash
sudo apt install python3
```

### openSUSE

```bash
sudo zypper install python3
```

> Additional Python or GUI dependencies may be required depending on the current Breeze Launcher version.

---

# ▶️ Running Breeze Launcher

From the repository directory:

```bash
python3 src/chapter3.py
```

If everything is configured correctly, Breeze Launcher should start.

---

# 🛠️ Troubleshooting

### `python3: command not found`

Python 3 is not installed or is not available in your PATH.

Install it using the package manager for your distribution.

### `No such file or directory: src/chapter3.py`

Make sure you are inside the Breeze Launcher directory:

```bash
cd Breeze-Launcher
```

Then run:

```bash
python3 src/chapter3.py
```

### GUI/dependency errors

Make sure your distribution has the required Python GUI packages installed.

If the launcher fails to start, open an issue on GitHub and include the complete terminal error.

---

# 🔨 Development

Want to modify Breeze Launcher?

Clone the repository:

```bash
git clone https://github.com/aditoxic-vibe/Breeze-Launcher.git
cd Breeze-Launcher
```

Run the launcher directly:

```bash
python3 src/chapter3.py
```

You can edit the source code and test your changes locally.

## 🧪 Testing changes

Changes do **not** need to be uploaded to GitHub immediately.

Recommended workflow:

```text
Edit
 ↓
Run Breeze Launcher
 ↓
Test
 ↓
Fix
 ↓
Test again
 ↓
When ready → commit
 ↓
Push to GitHub
```

---

# 📤 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a branch for your changes.
3. Make your changes.
4. Test Breeze Launcher.
5. Commit your changes.
6. Open a pull request.

Example:

```bash
git checkout -b my-feature
```

After making and testing your changes:

```bash
git add .
git commit -m "Add my feature"
git push
```

---

# 📁 Project structure

```text
Breeze-Launcher/
├── src/
│   └── chapter3.py
├── README.md
├── LICENSE
└── .gitignore
```

---

# 📜 License

Breeze Launcher is licensed under the **MIT License**.

See [`LICENSE`](LICENSE) for the complete license text.

---

# 🌬️ Breeze Launcher

**Lightweight. Fast. Clean. Linux.**

Made with ❤️ by **aditoxic-vibe**
