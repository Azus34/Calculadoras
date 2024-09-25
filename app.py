from flask import Flask, render_template, request
import numpy as np
from fractions import Fraction

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Obtener los coeficientes como fracciones
            a1 = Fraction(request.form['a1'])
            b1 = Fraction(request.form['b1'])
            c1 = Fraction(request.form['c1'])
            a2 = Fraction(request.form['a2'])
            b2 = Fraction(request.form['b2'])
            c2 = Fraction(request.form['c2'])

            # Crear matrices
            A = np.array([[float(a1), float(b1)], [float(a2), float(b2)]])
            B = np.array([float(c1), float(c2)])
            delta = np.linalg.det(A)

            if delta == 0:
                solution = "No tiene solución (delta es 0)."
                procedure = ""
                check = ""
            else:
                delta_x = np.linalg.det(np.array([[float(c1), float(b1)], [float(c2), float(b2)]]))
                delta_y = np.linalg.det(np.array([[float(a1), float(c1)], [float(a2), float(c2)]]))
                x = delta_x / delta
                y = delta_y / delta

                # Convertir resultados a fracción
                x_frac = Fraction(x).limit_denominator()
                y_frac = Fraction(y).limit_denominator()

                # Procedimiento detallado
                procedure = (
                    f"1. Delta (Δ) = det(A) = {delta:.2f}\n"
                    f"   - A = [[{a1}, {b1}], [{a2}, {b2}]]\n"
                    f"2. Delta_x (Δx) = det(A_x) = {delta_x:.2f}\n"
                    f"   - A_x = [[{c1}, {b1}], [{c2}, {b2}]]\n"
                    f"3. Delta_y (Δy) = det(A_y) = {delta_y:.2f}\n"
                    f"   - A_y = [[{a1}, {c1}], [{a2}, {c2}]]\n"
                    f"4. Solución:\n"
                    f"   - x = Δx / Δ = {delta_x:.2f} / {delta:.2f} = {x_frac}\n"
                    f"   - y = Δy / Δ = {delta_y:.2f} / {delta:.2f} = {y_frac}\n"
                )

                check1 = a1 * x_frac + b1 * y_frac
                check2 = a2 * x_frac + b2 * y_frac
                check = (
                    f"Comprobación:\n"
                    f"1. {a1} * {x_frac} + {b1} * {y_frac} = {check1} (debería ser {c1})\n"
                    f"2. {a2} * {x_frac} + {b2} * {y_frac} = {check2} (debería ser {c2})\n"
                )

                solution = {
                    'delta': delta,
                    'delta_x': delta_x,
                    'delta_y': delta_y,
                    'x': x_frac,
                    'y': y_frac
                }
        except Exception as e:
            solution = f"Error: {str(e)}"
            procedure = ""
            check = ""
        
        return render_template('index.html', solution=solution, procedure=procedure, check=check)

    return render_template('index.html', solution=None, procedure=None, check=None)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

