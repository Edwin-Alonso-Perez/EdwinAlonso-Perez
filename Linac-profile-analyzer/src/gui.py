"""
Interfaz gráfica para analizar perfiles de dosis de un acelerador lineal.
"""

from __future__ import annotations

import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from metrics import (
    DEFAULT_DOSE_COLUMN,
    DEFAULT_PROFILE_COLUMN,
    calcular_penumbra,
    calcular_planitud,
    calcular_simetria,
    calcular_tamano_campo,
    normalizar,
)
from processing import leer_archivo_perfil, recortar_por_tamano_campo


class AnalizadorPerfilApp:
    """Aplicación principal con interfaz de Tkinter."""

    def __init__(self) -> None:
        self.ventana = tk.Tk()
        self.ventana.title("Parámetros de Datos para Perfil")

        self.campo_size = None
        self.canvas_grafica = None

        self._crear_interfaz()

    def _crear_interfaz(self) -> None:
        titulo = tk.Label(
            self.ventana,
            text="Análisis de Perfil de Dosis",
            font=("Arial", 14, "bold"),
        )
        titulo.pack(pady=15)

        boton = tk.Button(
            self.ventana,
            text="Cargar y Procesar Datos",
            command=self.procesar_datos,
            font=("Arial", 12),
        )
        boton.pack(pady=5)

        frame_resultados = tk.Frame(self.ventana)
        frame_resultados.pack(pady=10)

        self.valor_campo_nominal = self._crear_fila_resultado(
            frame_resultados, "Tamaño de campo (nominal):", 0
        )
        self.valor_sim = self._crear_fila_resultado(frame_resultados, "Simetría:", 1)
        self.valor_plan = self._crear_fila_resultado(frame_resultados, "Planitud:", 2)
        self.valor_pares = self._crear_fila_resultado(frame_resultados, "Pares usados:", 3)
        self.valor_campo_calc = self._crear_fila_resultado(
            frame_resultados, "Tamaño de campo (50%):", 4
        )
        self.valor_penumbra = self._crear_fila_resultado(
            frame_resultados, "Penumbra (80–20%):", 5
        )

        self.frame_grafica = tk.Frame(
            self.ventana,
            bd=2,
            relief="sunken",
            width=450,
            height=300,
        )
        self.frame_grafica.pack(padx=10, pady=10)
        self.frame_grafica.pack_propagate(False)

    @staticmethod
    def _crear_fila_resultado(frame: tk.Frame, texto: str, fila: int) -> tk.Label:
        etiqueta = tk.Label(frame, text=texto, font=("Arial", 12, "bold"))
        etiqueta.grid(row=fila, column=0, sticky="w", padx=5)

        valor = tk.Label(frame, text="", font=("Arial", 12))
        valor.grid(row=fila, column=1, sticky="w")
        return valor

    def procesar_datos(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Selecciona el archivo",
            filetypes=(
                ("All files", "*.*"),
                ("Archivos CSV", "*.csv"),
                ("Archivos de texto", "*.txt"),
            ),
        )
        if not file_path:
            return

        try:
            datos = leer_archivo_perfil(file_path)

            self.campo_size = simpledialog.askfloat(
                "Tamaño de Campo",
                "Ingrese el tamaño del campo en cm (ejemplo: 10 para 10×10):",
            )


            datos_n = normalizar(datos)
            datos_c = recortar_por_tamano_campo(datos, self.campo_size)
            datos_c_normalizados = normalizar(datos_c)

            planitud = calcular_planitud(datos_c_normalizados)
            simetria, pares = calcular_simetria(datos_c)

            campo, (x_izq, x_der) = calcular_tamano_campo(datos_n)
            penumbra = calcular_penumbra(datos_n)

            self._actualizar_resultados(
                planitud=planitud,
                simetria=simetria,
                pares=pares,
                campo=campo,
                x_izq=x_izq,
                x_der=x_der,
                penumbra=penumbra,
            )
            self._dibujar_grafica(datos_n, file_path)

        except Exception as exc:
            messagebox.showerror("Error al procesar datos", str(exc))

    def _actualizar_resultados(
        self,
        planitud,
        simetria,
        pares,
        campo,
        x_izq,
        x_der,
        penumbra,
    ) -> None:
        if pares:
            par_str = (
                f"({pares[0][0]:.3f}, {pares[0][1]:.2f}) y "
                f"({pares[1][0]:.3f}, {pares[1][1]:.2f})"
            )
        else:
            par_str = "N/A"

        self.valor_sim.config(text=f"{simetria:.4f}" if simetria is not None else "N/A")
        self.valor_plan.config(text=f"{planitud:.4f}" if planitud is not None else "N/A")
        self.valor_pares.config(text=par_str)

        if self.campo_size:
            self.valor_campo_nominal.config(
                text=f"{int(self.campo_size)}×{int(self.campo_size)}"
            )
        else:
            self.valor_campo_nominal.config(text="N/A")

        if campo is not None:
            self.valor_campo_calc.config(text=f"{campo:.3f} cm ({x_izq:.2f}, {x_der:.2f})")
        else:
            self.valor_campo_calc.config(text="N/A")

        pen_izq, pen_der = penumbra
        if (pen_izq is not None) and (pen_der is not None):
            self.valor_penumbra.config(text=f"Izq: {pen_izq:.3f} cm, Der: {pen_der:.3f} cm")
        else:
            self.valor_penumbra.config(text="N/A")

    def _dibujar_grafica(self, datos_n, file_path: str) -> None:
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(datos_n[DEFAULT_PROFILE_COLUMN], datos_n[DEFAULT_DOSE_COLUMN])

        nombre_archivo = os.path.basename(file_path)
        nombre_sin_ext = os.path.splitext(nombre_archivo)[0]

        ax.set_title(f"Perfil: {nombre_sin_ext}")
        ax.set_xlabel("Perfil [cm]")
        ax.set_ylabel(f"{nombre_sin_ext} (normalizado)")
        ax.grid(True)
        fig.tight_layout()

        for widget in self.frame_grafica.winfo_children():
            widget.destroy()

        self.canvas_grafica = FigureCanvasTkAgg(fig, master=self.frame_grafica)
        self.canvas_grafica.draw()
        self.canvas_grafica.get_tk_widget().pack()

    def ejecutar(self) -> None:
        self.ventana.mainloop()
