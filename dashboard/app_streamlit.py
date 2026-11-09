"""
=============================================================================
PROJET GLOBAL : Tableau de Bord Streamlit - Système Décisionnel de Gestion des Notes
Connecté en TEMPS RÉEL à phpMyAdmin (MySQL)
=============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
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
# 1. Chargement Temps Réel depuis phpMyAdmin (MySQL) avec secours CSV
# -----------------------------------------------------------------------------
@st.cache_data(ttl=5) # Actualisation automatique toutes les 5 secondes !
def load_data_realtime():
    try:
        # Connexion directe à phpMyAdmin / MySQL local
        engine = create_engine("mysql+pymysql://root:@localhost:3306/gestion_notes_db")
        df_etud = pd.read_sql("SELECT * FROM etudiants", engine)
        df_comp = pd.read_sql("SELECT * FROM compositions", engine)
        df_prof = pd.read_sql("SELECT * FROM professeurs", engine)
        df_mat = pd.read_sql("SELECT * FROM matieres", engine)
        source = "🟢 Connecté en temps réel à phpMyAdmin (MySQL)"
    except Exception as e:
        # Mode secours automatique vers les fichiers CSV si MySQL n'est pas démarré
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dataset_dir = os.path.join(base_dir, "dataset")
        df_etud = pd.read_csv(os.path.join(dataset_dir, "etudiants_360.csv"))
        df_comp = pd.read_csv(os.path.join(dataset_dir, "compositions_1347.csv"))
        df_prof = pd.read_csv(os.path.join(dataset_dir, "professeurs_10.csv"))
        df_mat = pd.read_csv(os.path.join(dataset_dir, "matieres_12.csv"))
        source = "🟡 Mode Secours : Données chargées depuis CSV"
    
    return df_etud, df_comp, df_prof, df_mat, source

df_etud, df_comp, df_prof, df_mat, statut_source = load_data_realtime()

# -----------------------------------------------------------------------------
# 2. Barre Latérale & Filtres Multi-critères
# -----------------------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/isometric-folders/100/graduation-cap.png", width=64)
st.sidebar.title("EduAnalytics")
st.sidebar.markdown("**Système Décisionnel — Collé SYLL**")
st.sidebar.caption(f"Statut : **{statut_source}**")
st.sidebar.divider()

if st.sidebar.button("🔄 Rafraîchir les données en direct"):
    st.cache_data.clear()
    st.rerun()

sel_annee = st.sidebar.selectbox("Année Académique :", options=["Toutes"] + sorted(list(df_comp["annee_academique"].unique())))
sel_semestre = st.sidebar.selectbox("Semestre :", options=["Tous"] + sorted(list(df_comp["semestre"].unique())))
sel_filiere = st.sidebar.selectbox("Filière :", options=["Toutes"] + sorted(list(df_etud["nom_filiere"].dropna().unique())))
sel_niveau = st.sidebar.selectbox("Niveau d'Étude :", options=["Tous"] + sorted(list(df_etud["nom_niveau"].dropna().unique())))

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
    filtered_comp = filtered_comp[filtered_comp["nom_etudiant"].str.contains(search_query, case=False, na=False)]

# -----------------------------------------------------------------------------
# 3. Tableau de Bord Principal
# -----------------------------------------------------------------------------
st.title("🎓 Tableau de Bord Décisionnel des Notes (360 Étudiants)")
st.caption("Données synchronisées en temps réel avec la base relationnelle MySQL / phpMyAdmin")

# KPIs
col1, col2, col3, col4 = st.columns(4)

total_evals = len(filtered_comp)
unique_students = filtered_comp["id_etudiant"].nunique()
avg_gpa = round(filtered_comp["note"].mean(), 2) if total_evals > 0 else 0.0
admis_count = len(filtered_comp[filtered_comp["note"] >= 10.0])
pass_rate = round((admis_count / max(total_evals, 1)) * 100, 1)

col1.metric("Étudiants Évalués", f"{unique_students} / 360", "Effectif total")
col2.metric("Moyenne Générale", f"{avg_gpa} / 20", "Moyenne courante")
col3.metric("Taux de Réussite", f"{pass_rate} %", f"{admis_count} / {total_evals} Évaluations")
col4.metric("Total Évaluations", f"{total_evals} Notes", "Sur 4 années")

st.divider()

# Visualisations
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📊 Moyenne des Notes par Filière")
    if total_evals > 0:
        filiere_summary = filtered_comp.groupby(["filiere"])["note"].mean().reset_index()
        st.bar_chart(filiere_summary.set_index("filiere"), y="note", color="#6366f1", use_container_width=True)
    else:
        st.warning("Aucune donnée pour les filtres sélectionnés.")

with c2:
    st.subheader("🍰 Top 5 des Matières")
    if total_evals > 0:
        mat_summary = filtered_comp.groupby("nom_matiere")["note"].mean().sort_values(ascending=False).head(5).reset_index()
        st.dataframe(mat_summary, hide_index=True, use_container_width=True)

st.divider()

# Classement des Étudiants
st.subheader("🏆 Classement et Moyennes Pondérées par Étudiant")

if total_evals > 0:
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

with st.expander("👨‍🏫 Voir le Corps Enseignant (10 Professeurs)"):
    st.dataframe(df_prof, hide_index=True, use_container_width=True)
