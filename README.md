# AsmStudio

AsmStudio is an emulator and IDE 
written entirely in Python.

---

### Usage

This software uses a proprietary assembly language. Real assembly code probably won't work correctly, and should not be run here. 

Do not trust other people's assembly code. This project was not built with security in mind.

---

### Examples

You can test some example programs [here.](./examples)

---

### Getting Started

You can install the latest version from [the releases page.](https://github.com/MGoosePlayZ/AsmStudio/releases)

Once you launch the app, open `Tools > Settings...` and select your programs path. All files in that path will show in the left panel.

Click a file to open it. The center panel will show the file's contents & info, and allow you to edit it. The program won't include your changes if you don't save.

---

### Instruction Set

The default ISA is proprietary, and has much more capabilities than normal ISA's. You can view all default instructions [here.](./docs/INSTRUCTIONS.md)

The program executes code by converting the assembly code into Python, then executing that code. You can edit the ISA [here.](./src/Instructions.py)

