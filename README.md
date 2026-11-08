# 🧮 Scientific Calculator

A sleek, dark-mode **scientific calculator** desktop app built with **Python and CustomTkinter**. It supports trigonometry (with inverse functions), logarithms, powers, roots, factorials and constants, with degree/radian modes and full keyboard input. It evaluates expressions **safely without `eval()`**.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-1f6feb)
![Safe eval](https://img.shields.io/badge/Parser-AST%20(safe)-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

<!-- Add a screenshot / GIF here, e.g.
<p align="center"><img src="assets/preview.gif" alt="Scientific Calculator" width="320"></p>
-->

---

## ✨ Features

- **Modern dark UI** with rounded buttons, colour-coded keys and a press "flash" effect
- **Arithmetic:** `+  −  ×  ÷  %`, brackets and `00`
- **Powers & roots:** `xʸ` (`^`), `x²`, `√`
- **Trigonometry:** `sin`, `cos`, `tan`
- **INV mode** swaps in `sin⁻¹`, `cos⁻¹`, `tan⁻¹`, `10ˣ`, `eˣ` and `x²`
- **Logarithms:** `log` (base 10) and `ln`
- **Factorial** `!` and constants **π** and **e**
- **DEG / RAD** angle modes
- **AC** (clear all) and **⌫** (backspace)
- **Keyboard support:** type numbers and operators directly
- **Safe evaluation:** expressions are parsed with Python's `ast` module and only whitelisted operations and functions are allowed, so no arbitrary code can run
- Friendly **"Error"** display for invalid input

---

## 🚀 Getting Started

**Requirements:** Python 3.8+ and CustomTkinter.

```bash
# 1. Download or clone this repository, then open the project folder
cd scientific-calculator

# 2. Install the dependency
pip install customtkinter

# 3. Run the calculator
python "Scientific Calculator - Source Code.py"
```

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
| --- | --- |
| `0–9`, `.`, `+ - * / ( ) % ^` | Type into the expression |
| `Enter` or `=` | Calculate |
| `Backspace` | Delete last character |
| `Esc` | Clear all (AC) |
| `P` | Insert π |
| `E` | Insert e |
| `R` | Insert √ |

---

## 🧠 How the Safe Evaluator Works

Instead of calling `eval()`, the calculator:

1. Converts button labels into a Python-style expression (e.g. `√` → `sqrt(`, `^` → `**`, `5!` → `factorial(5)`).
2. Parses it into an **abstract syntax tree** with `ast.parse(..., mode="eval")`.
3. Walks the tree, allowing only numbers, `+ − × ÷ % **`, unary signs and a whitelist of maths functions (`sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `log`, `log10`, `sqrt`, `exp`, `factorial`) and constants (`pi`, `e`).

Anything else is rejected, which makes the calculator safe even with unexpected input.

---

## 🛠️ Tech Stack

- **Python 3**
- **CustomTkinter:** modern, themed Tkinter widgets
- **math** and **ast** (standard library)

---

## 📂 Project Structure

```
Scientific Calculator/
├── Scientific Calculator - Source Code.py   # the app (≈400 lines)
└── assets/                                   # (add screenshots / GIF for this README)
```

---

## 🔮 Ideas for Future Improvements

- Calculation history panel
- Memory keys (M+, M−, MR, MC)
- Light / dark theme toggle
- Graph plotting for functions

---

## 👤 Author

**Somya Ranjan Sahoo** · [GitHub](https://github.com/somyaranjansahoo6422) · [Portfolio](https://somyaranjansahoo6422.github.io/projects/smaller-builds/)

If you like this project, consider giving it a ⭐!
