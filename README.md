# 3DS Custom Install - Modern GUI

Installs a title (`.cia`) directly to an SD card for the Nintendo 3DS. 
This is a modernized fork of the original `custom-install` project, featuring a completely redesigned graphical interface, real-time logging, and robust error handling.

## ✨ New features in this version

* **Modern Interface:** A sleek, responsive dark-mode GUI built with CustomTkinter.
* **Smart Error Handling:** Automatically detects missing keys (`MissingSeedError`) for newer games, skipping them safely without crashing the entire installation process.
* **Real-Time Logging:** Built-in console viewer to monitor the injection process step-by-step.
* **Offline Database:** Automatically fetches and caches the 3DS Title Database for offline identification of installed apps.
* **Multi-Language:** Native support for English and Spanish.
* **Standalone Executable:** No need to install Python. Just download, extract, and run.

---

## 🚀 Quickstart (Windows Standalone)

You do **NOT** need to install Python to use this tool if you are on Windows.

1. [Dump your `boot9.bin` and `movable.sed`](https://wiki.hacks.guide/wiki/3DS:Dump_system_files) from your 3DS system.
2. Download the latest `.zip` release from the **Releases** tab.
3. Extract the folder to your PC.
4. Run `3DS Custom Installer.exe`.
5. Select your SD card, your system files, and the `.cia` files you want to install.

### System Files Required:
* **`movable.sed`**: Required to encrypt the files for your specific console.
* **`boot9.bin`**: Required for crypto operations.
* **`seeddb.bin`** *(Optional but recommended)*: Needed for newer games (2015+) and updates that use seeds. If missing, the program will skip these specific games but will continue installing classic base games.

## 🏁 Final step (Crucial)
After the PC installation is complete, the program will place a tool called `custom-install-finalize.3dsx` in your SD card's `3ds` folder.
**You must run `custom-install-finalize` through the Homebrew Launcher on your 3DS** to install the necessary tickets and make the games appear on your HOME Menu.

---

## 💻 For developers (Running from source)

If you want to modify the source code or run it on macOS/Linux, you will need Python installed.

### Setup
1. Clone this repository.
2. Install the required Python packages:
```bash
   pip install customtkinter Pillow pyctr
```
3. Run the GUI:
```bash
python gui_ctk.py
```

### Building the Windows Standalone (.exe)
To compile your own executable using PyInstaller, use the following command to avoid pathing issues with the internal libraries:

```bash
pyinstaller --noconsole --onedir --windowed --icon=icon.ico gui_ctk.py
```
*Note: After building, make sure to manually copy the `custominstall` folder and the `icon.ico` file into the generated `dist/gui_ctk/` directory.*

---

## 📜 License & Credits

* **Modern GUI & Backend Rework** by [Cytek0x](https://github.com/Cytek0x).
* **Core Logic & Original CLI** by [ihaveamac](https://github.com/ihaveamac/custom-install).
* **[save3ds](https://github.com/wwylele/save3ds)** by wwylele (used to interact with the Title Database).
* Thanks to @nek0bit for redesigning the original `custominstall.py` to work as a module.
* Thanks to @LyfeOnEdge for the second version of the classic GUI. Special thanks to CrafterPika and archbox for testing.
* Thanks to @BpyH64 for researching how to generate the cmacs.
* Interface Icons provided by [Icons8](https://icons8.com).