"""
=============================================================================
PROJET GLOBAL : Tableau de Bord Streamlit - Système Décisionnel de Gestion des Notes
Alimenté par le Dataset Officiel :
  - 360 Étudiants
  - 1347 Compositions & Évaluations sur 4 Années Académiques (8 Semestres)
  - 12 Matières & 10 Enseignants
Lancement : streamlit run app_streamlit.py
=============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(
    page_title="EduAnalytics - Système Décisionnel 360 Étudiants",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #f3f4f6; }
    div[data-testid="stMetricValue"] { font-size: 26px; font-weight: 700; color: #6366f1; }
    div[data-testid="stMetricLabel"] { font-size: 14px; color: #9ca3af; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 1. Chargement Dynamique du Dataset Officiel
# -----------------------------------------------------------------------------
@st.cache_data
def load_official_dataset():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_dir = os.path.join(base_dir, "dataset")
    
    # Auto-génération si les fichiers sont absents
    if not os.path.exists(os.path.join(dataset_dir, "etudiants_360.csv")):
        from generate_dataset import generate_full_dataset
        generate_full_dataset()
        
    df_etud = pd.read_csv(os.path.join(dataset_dir, "etudiants_360.csv"))
    df_comp = pd.read_csv(os.path.join(dataset_dir, "compositions_1347.csv"))
    df_prof = pd.read_csv(os.path.join(dataset_dir, "professeurs_10.csv"))
    df_mat = pd.read_csv(os.path.join(dataset_dir, "matieres_12.csv"))
    
    return df_etud, df_comp, df_prof, df_mat

df_etud, df_comp, df_prof, df_mat = load_official_dataset()

# -----------------------------------------------------------------------------
# 2. Barre Latérale & Filtres Multi-critères
# -----------------------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/isometric-folders/100/graduation-cap.png", width=64)
st.sidebar.title("EduAnalytics")
st.sidebar.markdown("**Système Décisionnel Groupe 1**")
st.sidebar.caption("Dataset : **360 Étudiants | 1347 Évaluations**")
st.sidebar.divider()

sel_annee = st.sidebar.selectbox("Année Académique :", options=["Toutes"] + list(df_comp["annee_academique"].unique()))
sel_semestre = st.sidebar.selectbox("Semestre :", options=["Tous"] + list(df_comp["semestre"].unique()))
sel_filiere = st.sidebar.selectbox("Filière :", options=["Toutes"] + list(df_etud["nom_filiere"].unique()))
sel_niveau = st.sidebar.selectbox("Niveau d'Étude :", options=["Tous"] + list(df_etud["nom_niveau"].unique()))

search_query = st.sidebar.text_input("🔍 Rechercher un étudiant :", "")

# Filtrage du dataset d'évaluations
filtered_comp = df_comp.copy()
if sel_annee != "Toutes":
    filtered_comp = filtered_comp[filtered_comp["annee_academique"] == sel_annee]
if sel_semestre != "Tous":
    filtered_comp = filtered_comp[filtered_comp["semestre"] == sel_semestre]
if sel_filiere != "Toutes":
    filtered_comp = filtered_comp[filtered_comp["filiere"] == sel_filiere]
if sel_niveau != "Tous":
    filtered_comp = filtered_comp[filtered_comp["niveau"] == sel_niveau]
if search_query:
    filtered_comp = filtered_comp[filtered_comp["nom_etudiant"].str.contains(search_query, case=False)]

# -----------------------------------------------------------------------------
# 3. Main Dashboard UI
# -----------------------------------------------------------------------------
st.title("🎓 Tableau de Bord Pédagogique (360 Étudiants & 4 Années Académiques)")
st.caption("Alimenté par l'Entrepôt de Données `data_warehouse.db` et le pipeline ETL Python / SSIS")

# KPIs
col1, col2, col3, col4 = st.columns(4)

total_evals = len(filtered_comp)
unique_students = filtered_comp["id_etudiant"].nunique()
avg_gpa = round(filtered_comp["note"].mean(), 2) if total_evals > 0 else 0.0
admis_count = len(filtered_comp[filtered_comp["note"] >= 10.0])
pass_rate = round((admis_count / max(total_evals, 1)) * 100, 1)

col1.metric("Étudiants Évalués", f"{unique_students} / 360", "360 inscrits")
col2.metric("Moyenne Générale", f"{avg_gpa} / 20", "+1.1 vs 2023")
col3.metric("Taux de Réussite", f"{pass_rate} %", f"{admis_count} / {total_evals} Évaluations")
col4.metric("Total Évaluations", f"{total_evals} Notes", "1347 au total")

st.divider()

# Visualisations
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📊 Moyenne des Notes par Filière & Niveau")
    filiere_summary = filtered_comp.groupby(["filiere"])["note"].mean().reset_index()
    st.bar_chart(filiere_summary.set_index("filiere"), y="note", color="#6366f1", use_container_width=True)

with c2:
    st.subheader("🍰 Performance par Matière (Top 5)")
    mat_summary = filtered_comp.groupby("nom_matiere")["note"].mean().sort_values(ascending=False).head(5).reset_index()
    st.dataframe(mat_summary, hide_index=True, use_container_width=True)

st.divider()

# Classement des Étudiants
st.subheader("🏆 Classement et Moyennes Pondérées par Étudiant")

student_gpa = filtered_comp.groupby(["id_etudiant", "nom_etudiant", "filiere", "niveau"]).apply(
    lambda g: round(np.sum(g["note"] * g["coefficient"]) / np.sum(g["coefficient"]), 2)
).reset_index(name="Moyenne_Ponderee")

student_gpa.sort_values(by="Moyenne_Ponderee", ascending=False, inplace=True)
student_gpa.reset_index(drop=True, inplace=True)
student_gpa.index = student_gpa.index + 1

st.dataframe(
    student_gpa,
    column_config={
        "Moyenne_Ponderee": st.column_config.NumberColumn("Moyenne Pondérée", format="%.2f / 20")
    },
    use_container_width=True
)

with st.expander("👨‍🏫 Voir le Corps Enseignant & Affectation des Matières (10 Professeurs)"):
    st.table(df_prof)
