import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages


st.set_page_config(page_title="Analyse de Fonction", layout="wide")
x = sp.symbols("x")

st.title("Analyse Interactive de Fonctions Mathématiques")
st.markdown("Entrez une fonction et choisissez une action : étude complète ou tracé simple.")

# ================= INPUT =================
user_input = st.text_input("Fonction en variable x (exemple: x**3 - 3*x):")

col1, col2 = st.columns(2)
analyse = col1.button("Étude complète")
tracer = col2.button("Tracé simple")

zoom = st.slider("Zoom graphique (limite X)", 1, 50, 10)

# ================= MAIN =================
if user_input:
    try:
        f = sp.sympify(user_input)
        fprime = sp.diff(f, x)
        f2prime = sp.diff(fprime, x)

        # ---------------- ETUDE ----------------
        if analyse:
            st.header("Étude complète de f(x)")

            # 1. Domaine
            try:
                domain = sp.calculus.util.function_range(f, x, sp.S.Reals)
            except:
                domain = "Non calculable automatiquement"
            st.subheader("1️. Domaine de définition")
            st.write("Df =", domain)

            # 2. Limites
            st.subheader("2️. Limites")
            lim_minus = sp.limit(f, x, -sp.oo)
            lim_plus = sp.limit(f, x, sp.oo)
            st.write(f"lim x → -∞ : {lim_minus}")
            st.write(f"lim x → +∞ : {lim_plus}")

            # 3. Dérivée et points critiques
            st.subheader("3️. Dérivée et points critiques")
            st.write("f'(x) =", fprime)
            crit_points = sp.solve(sp.Eq(fprime, 0), x)
            crit_points = [c.evalf() for c in crit_points if c.is_real]
            crit_points.sort()
            st.write("Points critiques :", crit_points)

            signe_plus = sp.solve_univariate_inequality(fprime > 0, x)
            signe_moins = sp.solve_univariate_inequality(fprime < 0, x)
            st.write("Croissance sur :", signe_plus)
            st.write("Décroissance sur :", signe_moins)

            # 4. Tableau de variation
            st.subheader("4️. Tableau de variation")
            Xtab = [-np.inf] + [float(c) for c in crit_points] + [np.inf]
            table_data = []
            for i in range(len(Xtab)-1):
                mid = (Xtab[i] + (Xtab[i+1] if Xtab[i+1] != np.inf else zoom)) / 2 if Xtab[i]!=-np.inf else -zoom
                try:
                    sign = '↗' if fprime.subs(x, mid) > 0 else '↘'
                except:
                    sign = '?'
                val_start = f.subs(x, Xtab[i]) if Xtab[i] not in [-np.inf, np.inf] else '-∞'
                val_end = f.subs(x, Xtab[i+1]) if Xtab[i+1] not in [-np.inf, np.inf] else '+∞'
                table_data.append([Xtab[i], Xtab[i+1], val_start, val_end, sign])
            df_variation = pd.DataFrame(table_data, columns=["x début", "x fin", "f(x début)", "f(x fin)", "Variation"])
            st.table(df_variation)

            # 5. Convexité et concavité
            st.subheader("5️. Convexité et concavité")
            st.write("f''(x) =", f2prime)
            convexe = sp.solve_univariate_inequality(f2prime > 0, x)
            concave = sp.solve_univariate_inequality(f2prime < 0, x)
            st.write("Convexe (∪) sur :", convexe)
            st.write("Concave (∩) sur :", concave)

            # 6. Asymptotes
            st.subheader("6️. Asymptotes")
            try:
                asymp = sp.asymptotes(f, x)
                st.write(asymp if asymp else "Pas d’asymptote trouvée")
            except:
                st.write("Pas d’asymptote calculable.")

            # 7. Graphique
            st.subheader("7️. Graphique de f(x)")
            f_lamb = sp.lambdify(x, f, "numpy")
            X = np.linspace(-zoom, zoom, 1000)
            Y = f_lamb(X)
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(X, Y, label=f"f(x) = {user_input}", color="blue")
            ax.axhline(0, color="black", linewidth=0.8)
            ax.axvline(0, color="black", linewidth=0.8)
            ax.grid(True, linestyle="--", alpha=0.6)
            ax.legend()
            st.pyplot(fig)

            # 8. Téléchargement PDF
            st.subheader("Télécharger l'étude en PDF")
            pdf_bytes = BytesIO()
            with PdfPages(pdf_bytes) as pdf:
                pdf.savefig(fig)
                fig_txt, ax_txt = plt.subplots(figsize=(8, 10))
                ax_txt.axis('off')
                info = f"Fonction : {user_input}\nDomaine : {domain}\nLimites : x→-∞:{lim_minus}, x→+∞:{lim_plus}\nDérivée : {fprime}\nPoints critiques : {crit_points}\nConvexe : {convexe}\nConcave : {concave}\nAsymptotes : {asymp if 'asymp' in locals() else 'N/A'}"
                ax_txt.text(0, 1, info, fontsize=12, verticalalignment='top')
                pdf.savefig(fig_txt)
                plt.close(fig_txt)
            pdf_bytes.seek(0)
            st.download_button("Télécharger PDF", data=pdf_bytes, file_name="Etude_fonction.pdf", mime="application/pdf")

        # ---------------- TRACÉ SIMPLE ----------------
        if tracer:
            st.header("Tracé simple de f(x)")
            f_lamb = sp.lambdify(x, f, "numpy")
            X = np.linspace(-zoom, zoom, 1000)
            Y = f_lamb(X)
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(X, Y, "b", label=f"f(x) = {user_input}")
            ax.axhline(0, color="black", linewidth=0.8)
            ax.axvline(0, color="black", linewidth=0.8)
            ax.grid(True, linestyle="--", alpha=0.6)
            ax.legend()
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Erreur : {e}")

