# Analyse de Fonctions Mathématiques avec Streamlit

Cette application web permet d’analyser et de tracer des fonctions mathématiques (polynômes, exponentielles, logarithmes, etc.) en Python avec **Streamlit** et **SymPy**.

---

## Fonctionnalités

- Étude complète d’une fonction :
  - Domaine de définition
  - Limites à l’infini
  - Dérivée et points critiques
  - Tableau de variation (avec flèches visuelles)
  - Convexité et concavité
  - Asymptotes si existantes
- Tracé simple de la courbe de la fonction
- Possibilité de zoomer sur le graphique
- Export en PDF de l’étude complète (optionnel)

---

## Installation

1. Cloner le dépôt :

```bash
git clone https://github.com/DEDJIABDOUL/AnalyseFonctions.git
cd AnalyseFonctions

2. Créer un environnement virtuel et l’activer :
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows PowerShell


3. Installer les dépendances :
```bash
pip install -r requirements.txt

4. Lancer l’application
```bash
streamlit run app.py
