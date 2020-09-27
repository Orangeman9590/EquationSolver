import functools
import os
import tkinter as tk
from concurrent import futures

app = tk.Tk()

thread_pool = futures.ThreadPoolExecutor(max_workers=1)


def tk_after(target) :
    @functools.wraps(target)
    def wrapper(self, *args, **kwargs) :
        args = (self,) + args
        self.after(0, target, *args, **kwargs)

    return wrapper


def submit_to_pool_executor(executor) :
    def decorator(target) :
        @functools.wraps(target)
        def wrapper(*args, **kwargs) :
            return executor.submit(target, *args, **kwargs)

        return wrapper

    return decorator


class MainFrame(tk.Frame) :

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.master.geometry('400x200')
        self.master.title("Equation Solver")
        self.entry = tk.StringVar()
        self.port1 = tk.StringVar()
        self.duration = tk.StringVar()
        label = tk.Label(
            self.master, text="Enter Linear Equation (Example: 2x-3=12)", fg='white', bg='black')
        label.pack()
        entry = tk.Entry(self.master, textvariable=self.entry)
        entry.insert(-1, "5x+3=2x+15")
        entry.pack()
        self.button = tk.Button(
            self.master, text="Solve Variable", command=self.on_button)
        self.button.pack()
        self.text = tk.Text(self.master)
        self.text.config(state=tk.DISABLED)
        self.text.pack(padx=5, pady=5)
        self.master.configure(bg='black')

    @tk_after
    def button_state(self, enabled=True) :
        state = tk.NORMAL
        if not enabled :
            state = tk.DISABLED
        self.button.config(state=state)

    @tk_after
    def clear_text(self) :
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.config(state=tk.DISABLED)

    @tk_after
    def insert_text(self, text) :
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, text)
        self.text.config(state=tk.DISABLED)


    def solve(self, equation) :
        for char in equation:
            if char.isalnum() and not char.isdigit():
                var = char
        self.clear_text()
        expression = equation.replace('=', '-(') + ')'
        self.insert_text(equation + '\n')
        expression = expression.replace(var, '*' + var)
        tog = eval(expression.replace(var, '1j'))
        tog_eq = str(-tog.real / tog.imag)
        self.insert_text(var+'= '+tog_eq)

    def on_button(self) :
        self.s()

    @submit_to_pool_executor(thread_pool)
    def s(self) :
        eq = self.entry.get()
        self.solve(eq)


if __name__ == '__main__' :
    main_frame = MainFrame()
    app.mainloop()
