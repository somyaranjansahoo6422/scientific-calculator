import ast
import math
import customtkinter as ctk

# APP SETTINGS
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# WINDOW
root = ctk.CTk()
root.title("Scientific Calculator")
root.geometry("470x720")
root.resizable(False, False)

# VARIABLES
expression = ""
inv_mode = False
angle_mode = "DEG"
display_var = ctk.StringVar()

# DISPLAY
display = ctk.CTkEntry(
    root,
    textvariable=display_var,
    height=75,
    corner_radius=18,
    font=("Arial", 28),
    justify="right"
)
display.pack(
    fill="x",
    padx=18,
    pady=(18, 28)
)

# BUTTON FRAME
button_frame = ctk.CTkFrame(
    root,
    fg_color="transparent"
)
button_frame.pack(
    expand=True,
    fill="both",
    padx=12,
    pady=12
)

# LAYOUTS
normal_layout = [
    ["sin", "cos", "tan", "RAD", "DEG"],
    ["log", "ln", "(", ")", "INV"],
    ["!", "AC", "%", "⌫", "/"],
    ["^", "7", "8", "9", "*"],
    ["√", "4", "5", "6", "-"],
    ["π", "1", "2", "3", "+"],
    ["e", "00", "0", ".", "="]
]

inv_layout = [
    ["sin⁻¹", "cos⁻¹", "tan⁻¹", "RAD", "DEG"],
    ["10ˣ", "eˣ", "(", ")", "INV"],
    ["!", "AC", "%", "⌫", "/"],
    ["^", "7", "8", "9", "*"],
    ["x²", "4", "5", "6", "-"],
    ["π", "1", "2", "3", "+"],
    ["e", "00", "0", ".", "="]
]

# BUTTON EFFECT
def haptic_feedback(button):

    original = button.cget("fg_color")

    button.configure(fg_color="#555555")

    button.after(
        100,
        lambda: button.configure(
            fg_color=original
        )
    )

# BUTTON COLORS
def get_button_color(btn):

    if btn in [
        "7", "8", "9",
        "4", "5", "6",
        "1", "2", "3",
        "00", "0", "."
    ]:
        return "#363636"

    elif btn in [
        "AC", "%", "⌫",
        "/", "*", "-",
        "+", "="
    ]:
        return "#ff9500"

    else:
        return "#252525"

def format_result(value):
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)

def extract_operand(text):
    if not text:
        raise ValueError("Missing operand for factorial")
    if text.endswith(")"):
        depth = 0
        for idx in range(len(text) - 1, -1, -1):
            ch = text[idx]
            if ch == ")":
                depth += 1
            elif ch == "(":
                depth -= 1
                if depth == 0:
                    return text[idx:], idx
        raise ValueError("Unmatched parenthesis in factorial operand")
    idx = len(text) - 1
    while idx >= 0 and (text[idx].isalnum() or text[idx] == "." or text[idx] == "_"):
        idx -= 1
    return text[idx + 1:], idx + 1

def preprocess_factorial(expr):
    result = ""
    i = 0
    while i < len(expr):
        if expr[i] == "!":
            operand, start = extract_operand(result)
            result = result[:start] + f"factorial({operand})"
            i += 1
        else:
            result += expr[i]
            i += 1
    return result

def eval_node(node, allowed):
    if isinstance(node, ast.Expression):
        return eval_node(node.body, allowed)
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.BinOp):
        left = eval_node(node.left, allowed)
        right = eval_node(node.right, allowed)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.Pow):
            return left ** right
        if isinstance(node.op, ast.Mod):
            return left % right
        raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
    if isinstance(node, ast.UnaryOp):
        operand = eval_node(node.operand, allowed)
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand
        raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function call")
        func_name = node.func.id
        if func_name not in allowed:
            raise ValueError(f"Function not allowed: {func_name}")
        args = [eval_node(arg, allowed) for arg in node.args]
        return allowed[func_name](*args)
    if isinstance(node, ast.Name):
        name = node.id
        if name not in allowed:
            raise ValueError(f"Name not allowed: {name}")
        return allowed[name]
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def eval_expression(expr):
    expr = preprocess_factorial(expr)
    allowed = {
        "sqrt": math.sqrt,
        "sin": lambda x: math.sin(math.radians(x)) if angle_mode == "DEG" else math.sin(x),
        "cos": lambda x: math.cos(math.radians(x)) if angle_mode == "DEG" else math.cos(x),
        "tan": lambda x: math.tan(math.radians(x)) if angle_mode == "DEG" else math.tan(x),
        "asin": lambda x: math.degrees(math.asin(x)) if angle_mode == "DEG" else math.asin(x),
        "acos": lambda x: math.degrees(math.acos(x)) if angle_mode == "DEG" else math.acos(x),
        "atan": lambda x: math.degrees(math.atan(x)) if angle_mode == "DEG" else math.atan(x),
        "log": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "factorial": math.factorial,
        "pi": math.pi,
        "e": math.e,
    }
    parsed = ast.parse(expr, mode="eval")
    return eval_node(parsed, allowed)

# CALCULATION
def press(value):
    global expression
    global inv_mode
    global angle_mode
    if expression == "Error" and value not in ["AC", "⌫"]:
        expression = ""
    if value == "AC":
        expression = ""
    elif value == "⌫":
        expression = expression[:-1]
    elif value == "=":
        try:
            expression = format_result(
                eval_expression(expression)
            )
        except Exception:
            expression = "Error"

    elif value == "π":
        expression += "pi"

    elif value == "e":
        expression += "e"

    elif value == "√":
        expression += "sqrt("

    elif value == "x²":
        expression += "**2"

    elif value == "^":
        expression += "**"

    elif value == "%":
        expression += "/100"

    elif value == "!":
        expression += "!"

    elif value == "INV":
        toggle_inv()
        return

    elif value == "RAD":
        angle_mode = "RAD"
        rebuild_buttons()
        return

    elif value == "DEG":
        angle_mode = "DEG"
        rebuild_buttons()
        return

    elif value == "sin":
        expression += "sin("

    elif value == "cos":
        expression += "cos("

    elif value == "tan":
        expression += "tan("

    elif value == "sin⁻¹":
        expression += "asin("

    elif value == "cos⁻¹":
        expression += "acos("

    elif value == "tan⁻¹":
        expression += "atan("

    elif value == "log":
        expression += "log10("

    elif value == "ln":
        expression += "log("

    elif value == "10ˣ":
        expression += "10**"

    elif value == "eˣ":
        expression += "exp("

    else:
        expression += str(value)

    display_var.set(expression)


# -----------------------------
# EVALUATOR
# -----------------------------


# -----------------------------
# INV TOGGLE
# -----------------------------
def toggle_inv():
    global inv_mode
    inv_mode = not inv_mode
    rebuild_buttons()


# -----------------------------
# BUTTON BUILDER
# -----------------------------
def rebuild_buttons():

    for widget in button_frame.winfo_children():
        widget.destroy()

    layout = inv_layout if inv_mode else normal_layout

    for r, row in enumerate(layout):

        for c, btn in enumerate(row):

            if btn in ["RAD", "DEG"]:
                color = "#ff9500" if btn == angle_mode else "#252525"
            else:
                color = get_button_color(btn)

            b = ctk.CTkButton(
                button_frame,
                text=btn,
                corner_radius=16,
                height=58,
                fg_color=color,
                hover_color="#4a4a4a",
                text_color="white",
                font=("Arial", 16, "bold"),
                command=lambda x=btn: press(x)
            )

            b.grid(
                row=r,
                column=c,
                padx=6,
                pady=6,
                sticky="nsew"
            )

            b.bind(
                "<Button-1>",
                lambda e, btn=b: haptic_feedback(btn)
            )

    for i in range(7):
        button_frame.rowconfigure(i, weight=1)

    for j in range(5):
        button_frame.columnconfigure(j, weight=1)


# -----------------------------
# START APP

def handle_key(event):
    key = event.keysym
    char = event.char

    if key in ("Return", "KP_Enter") or char == "=":
        press("=")
        return

    if key == "BackSpace":
        press("⌫")
        return

    if key == "Escape":
        press("AC")
        return

    if char in "0123456789.+-*/()%^":
        press(char)
        return

    if char.lower() == "p":
        press("π")
        return

    if char.lower() == "r":
        press("√")
        return

    if char.lower() == "e":
        press("e")
        return


root.bind_all("<Key>", handle_key)
rebuild_buttons()
root.mainloop()
