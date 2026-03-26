import numpy as np
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# ==============================
# CLASE OPTIMIZADOR
# ==============================
class Optimizador:
    def __init__(self, funcion, a, b, precision=0.001, modo="min"):
        self.funcion = funcion
        self.a = a
        self.b = b
        self.precision = precision
        self.modo = modo
        self.iteraciones = 0
        self.historial = []

    def buscar_optimo(self):
        dx = self.precision

        x0 = self.a
        x1 = x0 + dx
        x2 = x1 + dx

        mejor_x = self.a
        mejor_valor = self.funcion(self.a)

        while x2 <= self.b:
            f0 = self.funcion(x0)
            f1 = self.funcion(x1)
            f2 = self.funcion(x2)

            self.historial.append((self.iteraciones, x1, f1))
            self.iteraciones += 1

            if self.modo == "min":
                if f1 < f0 and f1 < f2:
                    return x1, f1
                if f1 < mejor_valor:
                    mejor_valor = f1
                    mejor_x = x1
            else:
                if f1 > f0 and f1 > f2:
                    return x1, f1
                if f1 > mejor_valor:
                    mejor_valor = f1
                    mejor_x = x1

            x0 = x1
            x1 = x2
            x2 = x1 + dx

        return mejor_x, mejor_valor


# ==============================
# INTERFAZ GRÁFICA
# ==============================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Optimizador Unidimensional PRO")

        # Función
        tk.Label(root, text="Función f(x):").grid(row=0, column=0)
        self.func_entry = tk.Entry(root, width=35)
        self.func_entry.insert(0, "x**2 - 4*x + 4")
        self.func_entry.grid(row=0, column=1)

        # Intervalo
        tk.Label(root, text="a:").grid(row=1, column=0)
        self.a_entry = tk.Entry(root)
        self.a_entry.insert(0, "0")
        self.a_entry.grid(row=1, column=1)

        tk.Label(root, text="b:").grid(row=2, column=0)
        self.b_entry = tk.Entry(root)
        self.b_entry.insert(0, "5")
        self.b_entry.grid(row=2, column=1)

        # Precisión
        tk.Label(root, text="Precisión:").grid(row=3, column=0)
        self.prec_entry = tk.Entry(root)
        self.prec_entry.insert(0, "0.001")
        self.prec_entry.grid(row=3, column=1)

        # Min / Max
        self.modo = tk.StringVar(value="min")
        tk.Radiobutton(root, text="Minimizar", variable=self.modo, value="min").grid(row=4, column=0)
        tk.Radiobutton(root, text="Maximizar", variable=self.modo, value="max").grid(row=4, column=1)

        # Botón
        tk.Button(root, text="Optimizar", command=self.optimizar).grid(row=5, columnspan=2)

        # Resultado
        self.resultado = tk.Label(root, text="", justify="left")
        self.resultado.grid(row=6, columnspan=2)

        # Tabla simple
        self.tabla = tk.Text(root, height=10, width=50)
        self.tabla.grid(row=7, columnspan=2)

    def optimizar(self):
        try:
            expr = self.func_entry.get()
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            precision = float(self.prec_entry.get())
            modo = self.modo.get()

            funcion = lambda x: eval(expr, {"x": x, "np": np})

            opt = Optimizador(funcion, a, b, precision, modo)
            x_opt, y_opt = opt.buscar_optimo()

            # Aproximación analítica (numérica fina)
            x_vals = np.linspace(a, b, 10000)
            y_vals = funcion(x_vals)

            if modo == "min":
                idx = np.argmin(y_vals)
            else:
                idx = np.argmax(y_vals)

            x_real = x_vals[idx]
            y_real = y_vals[idx]

            error = abs(x_real - x_opt)

            tipo = "Mínimo" if modo == "min" else "Máximo"

            # Mostrar resultados
            self.resultado.config(text=
                f"{tipo} encontrado:\n"
                f"x = {x_opt:.5f}\n"
                f"f(x) = {y_opt:.5f}\n"
                f"Iteraciones = {opt.iteraciones}\n"
                f"Valor analítico aprox = {x_real:.5f}\n"
                f"Error = {error:.5f}"
            )

            # Mostrar tabla (primeros 10 valores)
            self.tabla.delete("1.0", tk.END)
            self.tabla.insert(tk.END, "Iteración\t x\t f(x)\n")
            for i, x, f in opt.historial[:10]:
                self.tabla.insert(tk.END, f"{i}\t {x:.4f}\t {f:.4f}\n")

            self.graficar(funcion, a, b, x_opt, y_opt, tipo)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def graficar(self, funcion, a, b, x_opt, y_opt, tipo):
        x = np.linspace(a, b, 500)
        y = funcion(x)

        plt.figure()
        plt.plot(x, y)
        plt.scatter(x_opt, y_opt)

        plt.axvline(x=x_opt, linestyle="--")
        plt.title(f"{tipo} encontrado")
        plt.xlabel("x")
        plt.ylabel("f(x)")

        plt.text(x_opt, y_opt, f"({x_opt:.2f}, {y_opt:.2f})")

        plt.show()


# ==============================
# EJECUCIÓN
# ==============================
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()