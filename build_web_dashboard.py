import json
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
WEB_DIR = BASE_DIR / "web_demo"
WEB_DIR.mkdir(parents=True, exist_ok=True)

df_comp = pd.read_csv(DATASET_DIR / "compositions_1347.csv")
df_prof = pd.read_csv(DATASET_DIR / "professeurs_10.csv")

comp_records = df_comp[
    [
        "id_etudiant",
        "nom_etudiant",
        "filiere",
        "niveau",
        "nom_matiere",
        "coefficient",
        "note",
        "annee_academique",
        "semestre",
    ]
].to_dict(orient="records")

prof_records = df_prof.to_dict(orient="records")
annees = ["Toutes"] + sorted(df_comp["annee_academique"].unique().tolist())
semestres = ["Tous"] + sorted(df_comp["semestre"].unique().tolist())
filieres = ["Toutes"] + sorted(df_comp["filiere"].unique().tolist())
niveaux = ["Tous"] + sorted(df_comp["niveau"].unique().tolist())

html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>EduAnalytics - Système Décisionnel 360 Étudiants</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet" />
  <style>
    body {{ font-family: 'Inter', sans-serif; background-color: #0b0f19; color: #f3f4f6; }}
    .mono {{ font-family: 'JetBrains Mono', monospace; }}
  </style>
</head>
<body class="min-h-screen flex flex-col lg:flex-row">
  <!-- Barre Latérale Streamlit -->
  <aside class="w-full lg:w-72 bg-[#111827] border-b lg:border-b-0 lg:border-r border-slate-800 p-6 shrink-0 space-y-5">
    <div class="flex items-center gap-3">
      <img src="https://img.icons8.com/isometric-folders/100/graduation-cap.png" alt="EduAnalytics" class="w-14 h-14" />
      <div>
        <h2 class="text-xl font-extrabold text-white">EduAnalytics</h2>
        <p class="text-xs font-bold text-indigo-400">Système Décisionnel Groupe 1</p>
        <p class="text-[11px] text-slate-400 mt-0.5">Dataset : <strong>360 Étudiants | 1347 Évaluations</strong></p>
      </div>
    </div>

    <hr class="border-slate-800" />

    <div class="space-y-4 text-xs">
      <div>
        <label class="block text-slate-300 font-semibold mb-1.5">Année Académique :</label>
        <select id="selAnnee" onchange="renderAll()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white">
          {''.join(f'<option value="{a}">{a}</option>' for a in annees)}
        </select>
      </div>

      <div>
        <label class="block text-slate-300 font-semibold mb-1.5">Semestre :</label>
        <select id="selSemestre" onchange="renderAll()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white">
          {''.join(f'<option value="{s}">{s}</option>' for s in semestres)}
        </select>
      </div>

      <div>
        <label class="block text-slate-300 font-semibold mb-1.5">Filière :</label>
        <select id="selFiliere" onchange="renderAll()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white">
          {''.join(f'<option value="{f}">{f}</option>' for f in filieres)}
        </select>
      </div>

      <div>
        <label class="block text-slate-300 font-semibold mb-1.5">Niveau d'Étude :</label>
        <select id="selNiveau" onchange="renderAll()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white">
          {''.join(f'<option value="{n}">{n}</option>' for n in niveaux)}
        </select>
      </div>

      <div>
        <label class="block text-slate-300 font-semibold mb-1.5">🔍 Rechercher un étudiant :</label>
        <input id="searchQuery" oninput="renderAll()" type="text" placeholder="Ex: Saliou, Fatou, Moussa..." class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white" />
      </div>
    </div>

    <hr class="border-slate-800" />
    <div class="pt-2 space-y-2">
      <a href="https://github.com/Collesyll0607/projet-global-gestion-notes" target="_blank" class="block w-full text-center py-2 px-3 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition">
        Voir le Dépôt GitHub ↗
      </a>
      <a href="https://collesyll0607.github.io/" class="block w-full text-center py-2 px-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition">
        ← Portfolio Collé Syll
      </a>
    </div>
  </aside>

  <!-- Contenu Principal Streamlit -->
  <main class="flex-1 p-6 sm:p-10 space-y-8 overflow-y-auto">
    <div>
      <h1 class="text-2xl sm:text-3xl font-extrabold text-white">
        🎓 Tableau de Bord Pédagogique (360 Étudiants &amp; 4 Années Académiques)
      </h1>
      <p class="text-xs sm:text-sm text-slate-400 mt-1">
        Alimenté par l'Entrepôt de Données <code class="mono text-indigo-400">data_warehouse.db</code> et le pipeline ETL Python / SSIS
      </p>
    </div>

    <!-- 4 KPIs -->
    <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="p-5 rounded-xl bg-[#111827] border border-slate-800">
        <span class="text-xs text-slate-400">Étudiants Évalués</span>
        <div id="kpiStudents" class="text-2xl font-bold text-[#6366f1] mt-1">360 / 360</div>
        <span class="text-xs text-emerald-400 mt-1 block">↑ 360 inscrits</span>
      </div>
      <div class="p-5 rounded-xl bg-[#111827] border border-slate-800">
        <span class="text-xs text-slate-400">Moyenne Générale</span>
        <div id="kpiAvg" class="text-2xl font-bold text-[#6366f1] mt-1">13.50 / 20</div>
        <span class="text-xs text-emerald-400 mt-1 block">↑ +1.1 vs 2023</span>
      </div>
      <div class="p-5 rounded-xl bg-[#111827] border border-slate-800">
        <span class="text-xs text-slate-400">Taux de Réussite</span>
        <div id="kpiPass" class="text-2xl font-bold text-[#6366f1] mt-1">82.0 %</div>
        <span id="kpiPassSub" class="text-xs text-emerald-400 mt-1 block">Évaluations validées</span>
      </div>
      <div class="p-5 rounded-xl bg-[#111827] border border-slate-800">
        <span class="text-xs text-slate-400">Total Évaluations</span>
        <div id="kpiTotal" class="text-2xl font-bold text-[#6366f1] mt-1">1347 Notes</div>
        <span class="text-xs text-slate-400 mt-1 block">1347 au total</span>
      </div>
    </section>

    <hr class="border-slate-800" />

    <!-- Visualisations : Bar Chart par Filière + Top 5 Matières -->
    <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 p-6 rounded-xl bg-[#111827] border border-slate-800 space-y-4">
        <h3 class="text-base font-bold text-white">📊 Moyenne des Notes par Filière &amp; Niveau</h3>
        <div id="filiereChart" class="space-y-4 pt-2"></div>
      </div>

      <div class="p-6 rounded-xl bg-[#111827] border border-slate-800 space-y-4">
        <h3 class="text-base font-bold text-white">🍰 Performance par Matière (Top 5)</h3>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead>
              <tr class="border-b border-slate-800 text-slate-400">
                <th class="py-2">Matière</th>
                <th class="py-2 text-right">Moyenne</th>
              </tr>
            </thead>
            <tbody id="topMatieresBody" class="divide-y divide-slate-800/70"></tbody>
          </table>
        </div>
      </div>
    </section>

    <hr class="border-slate-800" />

    <!-- Classement des Étudiants -->
    <section class="p-6 rounded-xl bg-[#111827] border border-slate-800 space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <h3 class="text-base font-bold text-white">🏆 Classement et Moyennes Pondérées par Étudiant</h3>
        <span id="rankingCount" class="text-xs text-slate-400 mono"></span>
      </div>
      <div class="overflow-x-auto max-h-96">
        <table class="w-full text-left text-xs sm:text-sm">
          <thead class="sticky top-0 bg-[#111827] border-b border-slate-800 text-slate-400 text-xs uppercase">
            <tr>
              <th class="py-2.5 px-3">Rang</th>
              <th class="py-2.5 px-3">ID Étudiant</th>
              <th class="py-2.5 px-3">Nom Étudiant</th>
              <th class="py-2.5 px-3">Filière</th>
              <th class="py-2.5 px-3">Niveau</th>
              <th class="py-2.5 px-3">Moyenne Pondérée</th>
            </tr>
          </thead>
          <tbody id="rankingBody" class="divide-y divide-slate-800/60"></tbody>
        </table>
      </div>
    </section>

    <!-- Expander Corps Enseignant -->
    <details class="p-5 rounded-xl bg-[#111827] border border-slate-800">
      <summary class="cursor-pointer font-bold text-sm text-white">
        👨‍🏫 Voir le Corps Enseignant &amp; Affectation des Matières (10 Professeurs)
      </summary>
      <div class="mt-4 overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead>
            <tr class="border-b border-slate-800 text-slate-400">
              <th class="py-2 px-3">ID</th>
              <th class="py-2 px-3">Nom</th>
              <th class="py-2 px-3">Prénom</th>
              <th class="py-2 px-3">Département</th>
              <th class="py-2 px-3">Genre</th>
              <th class="py-2 px-3">Email</th>
            </tr>
          </thead>
          <tbody id="profBody" class="divide-y divide-slate-800/60"></tbody>
        </table>
      </div>
    </details>
  </main>

  <script>
    const RAW_COMP = {json.dumps(comp_records, ensure_ascii=False)};
    const RAW_PROF = {json.dumps(prof_records, ensure_ascii=False)};

    function renderAll() {{
      const annee = document.getElementById("selAnnee").value;
      const sem = document.getElementById("selSemestre").value;
      const fil = document.getElementById("selFiliere").value;
      const niv = document.getElementById("selNiveau").value;
      const q = document.getElementById("searchQuery").value.trim().toLowerCase();

      const filtered = RAW_COMP.filter(r =>
        (annee === "Toutes" || r.annee_academique === annee) &&
        (sem === "Tous" || r.semestre === sem) &&
        (fil === "Toutes" || r.filiere === fil) &&
        (niv === "Tous" || r.niveau === niv) &&
        (!q || r.nom_etudiant.toLowerCase().includes(q))
      );

      const totalEvals = filtered.length;
      const uniqueStudents = new Set(filtered.map(r => r.id_etudiant)).size;
      const avgGpa = totalEvals > 0 ? (filtered.reduce((s, r) => s + r.note, 0) / totalEvals).toFixed(2) : "0.00";
      const admisCount = filtered.filter(r => r.note >= 10.0).length;
      const passRate = totalEvals > 0 ? ((admisCount / totalEvals) * 100).toFixed(1) : "0.0";

      document.getElementById("kpiStudents").textContent = `${{uniqueStudents}} / 360`;
      document.getElementById("kpiAvg").textContent = `${{avgGpa}} / 20`;
      document.getElementById("kpiPass").textContent = `${{passRate}} %`;
      document.getElementById("kpiPassSub").textContent = `${{admisCount}} / ${{totalEvals}} Évaluations`;
      document.getElementById("kpiTotal").textContent = `${{totalEvals}} Notes`;

      // Moyenne par Filière
      const byFiliere = {{}};
      filtered.forEach(r => {{
        if (!byFiliere[r.filiere]) byFiliere[r.filiere] = {{ sum: 0, count: 0 }};
        byFiliere[r.filiere].sum += r.note;
        byFiliere[r.filiere].count += 1;
      }});
      const filiereHtml = Object.entries(byFiliere).map(([fName, stats]) => {{
        const m = (stats.sum / stats.count).toFixed(2);
        const pct = Math.min(100, (m / 20) * 100).toFixed(1);
        return `
          <div>
            <div class="flex justify-between text-xs mb-1">
              <span class="font-semibold text-slate-200">${{fName}}</span>
              <span class="mono font-bold text-indigo-400">${{m}} / 20</span>
            </div>
            <div class="h-3 bg-slate-800 rounded-full overflow-hidden">
              <div class="h-full bg-[#6366f1] rounded-full" style="width:${{pct}}%"></div>
            </div>
          </div>
        `;
      }}).join("");
      document.getElementById("filiereChart").innerHTML = filiereHtml || '<p class="text-xs text-slate-500">Aucune donnée</p>';

      // Top 5 Matières
      const byMat = {{}};
      filtered.forEach(r => {{
        if (!byMat[r.nom_matiere]) byMat[r.nom_matiere] = {{ sum: 0, count: 0 }};
        byMat[r.nom_matiere].sum += r.note;
        byMat[r.nom_matiere].count += 1;
      }});
      const topMat = Object.entries(byMat)
        .map(([mName, st]) => ({{ name: mName, avg: st.sum / st.count }}))
        .sort((a, b) => b.avg - a.avg)
        .slice(0, 5);
      document.getElementById("topMatieresBody").innerHTML = topMat.map(m => `
        <tr>
          <td class="py-2.5 text-slate-200">${{m.name}}</td>
          <td class="py-2.5 text-right mono font-bold text-indigo-400">${{m.avg.toFixed(2)}}</td>
        </tr>
      `).join("");

      // Classement Pondéré par Étudiant
      const byStudent = {{}};
      filtered.forEach(r => {{
        const key = r.id_etudiant;
        if (!byStudent[key]) {{
          byStudent[key] = {{
            id_etudiant: r.id_etudiant,
            nom_etudiant: r.nom_etudiant,
            filiere: r.filiere,
            niveau: r.niveau,
            weightedSum: 0,
            coefSum: 0
          }};
        }}
        byStudent[key].weightedSum += r.note * r.coefficient;
        byStudent[key].coefSum += r.coefficient;
      }});

      const ranking = Object.values(byStudent)
        .map(s => ({{ ...s, gpa: s.weightedSum / Math.max(s.coefSum, 1) }}))
        .sort((a, b) => b.gpa - a.gpa);

      document.getElementById("rankingCount").textContent = `${{ranking.length}} étudiants classés`;
      document.getElementById("rankingBody").innerHTML = ranking.slice(0, 100).map((s, idx) => `
        <tr class="hover:bg-slate-800/40">
          <td class="py-2 px-3 mono text-xs text-slate-400">#${{idx + 1}}</td>
          <td class="py-2 px-3 mono text-xs text-slate-300">${{s.id_etudiant}}</td>
          <td class="py-2 px-3 font-semibold text-white">${{s.nom_etudiant}}</td>
          <td class="py-2 px-3 text-slate-300">${{s.filiere}}</td>
          <td class="py-2 px-3"><span class="px-2 py-0.5 rounded bg-slate-800 text-xs">${{s.niveau}}</span></td>
          <td class="py-2 px-3 mono font-bold ${{s.gpa >= 10 ? 'text-indigo-400' : 'text-rose-400'}}">${{s.gpa.toFixed(2)}} / 20</td>
        </tr>
      `).join("");
    }}

    document.getElementById("profBody").innerHTML = RAW_PROF.map(p => `
      <tr>
        <td class="py-2 px-3 mono text-slate-400">${{p.id_prof}}</td>
        <td class="py-2 px-3 font-bold text-white">${{p.nom}}</td>
        <td class="py-2 px-3 text-slate-200">${{p.prenom}}</td>
        <td class="py-2 px-3 text-indigo-300">${{p.departement}}</td>
        <td class="py-2 px-3">${{p.genre}}</td>
        <td class="py-2 px-3 mono text-slate-400">${{p.email}}</td>
      </tr>
    `).join("");

    renderAll();
  </script>
</body>
</html>
"""

(WEB_DIR / "index.html").write_text(html, encoding="utf-8")
print("Generated web_demo/index.html with all 1347 evaluations and 10 professors!")
