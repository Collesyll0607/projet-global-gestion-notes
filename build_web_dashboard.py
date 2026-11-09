import os
import json
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(base_dir, "dataset")

df_etud = pd.read_csv(os.path.join(dataset_dir, "etudiants_360.csv"))
df_comp = pd.read_csv(os.path.join(dataset_dir, "compositions_1347.csv"))
df_prof = pd.read_csv(os.path.join(dataset_dir, "professeurs_10.csv"))
df_mat = pd.read_csv(os.path.join(dataset_dir, "matieres_12.csv"))

# Compact array representation for fast loading:
# [id_etudiant, nom_etudiant, filiere, niveau, nom_matiere, coefficient, note, semestre, annee_academique]
comp_rows = []
for _, r in df_comp.iterrows():
    comp_rows.append([
        int(r["id_etudiant"]),
        str(r["nom_etudiant"]),
        str(r["filiere"]),
        str(r["niveau"]),
        str(r["nom_matiere"]),
        int(r["coefficient"]),
        round(float(r["note"]), 2),
        str(r["semestre"]),
        str(r["annee_academique"])
    ])

prof_records = df_prof.to_dict(orient="records")
annees = sorted(list(df_comp["annee_academique"].dropna().unique()), reverse=True)
semestres = sorted(list(df_comp["semestre"].dropna().unique()))
filieres = sorted(list(df_etud["nom_filiere"].dropna().unique()))
niveaux = sorted(list(df_etud["nom_niveau"].dropna().unique()))

html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>EduAnalytics - Systeme Decisionnel de Gestion des Notes</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Inter', sans-serif;
      background-color: #0e1117;
      color: #fafafa;
    }}
    .st-sidebar {{
      background-color: #262730;
      border-right: 1px solid rgba(250, 250, 250, 0.1);
    }}
    .st-metric {{
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      padding: 18px 20px;
      border-radius: 12px;
      border: 1px solid rgba(255,255,255,0.08);
      box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    }}
    .st-input {{
      background-color: #0e1117;
      border: 1px solid rgba(250, 250, 250, 0.2);
      color: #fafafa;
      border-radius: 0.5rem;
      padding: 0.55rem 0.75rem;
      width: 100%;
      font-size: 0.875rem;
    }}
    .st-input:focus {{
      outline: none;
      border-color: #6366f1;
    }}
    .st-card {{
      background-color: #161b26;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 12px;
    }}
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: #0e1117; }}
    ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 3px; }}
  </style>
</head>
<body class="min-h-screen flex flex-col lg:flex-row">
  <!-- Barre Laterale Streamlit -->
  <aside class="st-sidebar w-full lg:w-80 lg:min-h-screen p-6 flex-shrink-0 flex flex-col justify-between">
    <div>
      <div class="flex items-center gap-3 mb-2">
        <div class="w-12 h-12 rounded-xl bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-center text-2xl">
          🎓
        </div>
        <div>
          <h2 class="text-xl font-extrabold tracking-tight text-white">EduAnalytics</h2>
          <p class="text-xs font-semibold text-slate-300">Système Décisionnel — Collé SYLL</p>
        </div>
      </div>
      <div class="mt-2 mb-5 px-3 py-2 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-xs text-emerald-300 font-medium">
        🟢 Synchronisé MySQL (phpMyAdmin) &amp; Dataset Officiel (360 Étudiants | 1347 Évaluations)
      </div>

      <hr class="border-white/10 my-4" />

      <h3 class="text-sm font-bold text-white mb-4 flex items-center gap-2">
        <span>🔍</span> Filtres Analytiques
      </h3>

      <div class="space-y-4">
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1.5">Année Académique :</label>
          <select id="selAnnee" class="st-input"></select>
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1.5">Semestre :</label>
          <select id="selSemestre" class="st-input"></select>
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1.5">Filière :</label>
          <select id="selFiliere" class="st-input"></select>
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1.5">Niveau d'Étude :</label>
          <select id="selNiveau" class="st-input"></select>
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1.5">🔍 Rechercher un étudiant :</label>
          <input type="text" id="searchQuery" placeholder="Ex: Diop, Ndiaye, Fall..." class="st-input" />
        </div>
        <button id="resetBtn" class="w-full py-2 px-3 rounded-lg bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 border border-indigo-500/30 text-xs font-semibold transition">
          Réinitialiser tous les filtres
        </button>
      </div>
    </div>

    <div class="mt-8 pt-4 border-t border-white/10 text-xs text-slate-400 space-y-2">
      <div class="flex items-center justify-between">
        <span>Architecture :</span>
        <span class="text-slate-200 font-semibold">MySQL / ETL / Streamlit</span>
      </div>
      <div class="flex items-center justify-between">
        <span>Auteure :</span>
        <span class="text-indigo-400 font-semibold">Collé Syll (UASZ)</span>
      </div>
      <a href="https://github.com/Collesyll0607/projet-global-gestion-notes" target="_blank" rel="noopener noreferrer"
         class="mt-2 w-full inline-flex items-center justify-center gap-2 py-2 px-3 rounded-lg bg-white/5 hover:bg-white/10 text-white font-semibold transition">
        Voir le Code Source GitHub ↗
      </a>
    </div>
  </aside>

  <!-- Contenu Principal -->
  <main class="flex-1 p-6 lg:p-10 max-w-7xl mx-auto w-full">
    <header class="mb-6">
      <h1 class="text-2xl lg:text-3xl font-extrabold text-white tracking-tight">
        🎓 Tableau de Bord Décisionnel des Notes (360 Étudiants)
      </h1>
      <p class="text-sm text-slate-400 mt-1">
        Données synchronisées avec la base relationnelle <code class="text-indigo-400 bg-indigo-950/60 px-1.5 py-0.5 rounded">MySQL / phpMyAdmin</code>, l'Entrepôt de Données <code class="text-indigo-400 bg-indigo-950/60 px-1.5 py-0.5 rounded">data_warehouse.db</code> et le pipeline ETL Python
      </p>
    </header>

    <!-- 4 KPIs -->
    <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div class="st-metric">
        <p class="text-xs font-medium text-slate-400">Étudiants Évalués</p>
        <p id="kpiStudents" class="text-2xl font-extrabold text-white mt-1">360 / 360</p>
        <span class="inline-block mt-2 text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded">↑ Effectif total</span>
      </div>
      <div class="st-metric">
        <p class="text-xs font-medium text-slate-400">Moyenne Générale</p>
        <p id="kpiGpa" class="text-2xl font-extrabold text-white mt-1">-- / 20</p>
        <span class="inline-block mt-2 text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded">↑ Moyenne courante</span>
      </div>
      <div class="st-metric">
        <p class="text-xs font-medium text-slate-400">Taux de Réussite</p>
        <p id="kpiPassRate" class="text-2xl font-extrabold text-white mt-1">-- %</p>
        <span id="kpiPassSub" class="inline-block mt-2 text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded">-- Évaluations</span>
      </div>
      <div class="st-metric">
        <p class="text-xs font-medium text-slate-400">Total Évaluations</p>
        <p id="kpiTotalEvals" class="text-2xl font-extrabold text-white mt-1">1347 Notes</p>
        <span class="inline-block mt-2 text-xs font-semibold text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded">Sur 4 années</span>
      </div>
    </section>

    <hr class="border-white/10 my-6" />

    <!-- Graphiques d'Analyse Croisee -->
    <section class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      <div class="lg:col-span-2 st-card p-5">
        <h2 class="text-base font-bold text-white mb-4">📊 Moyenne des Notes par Filière</h2>
        <div class="h-72">
          <canvas id="filiereChart"></canvas>
        </div>
      </div>

      <div class="st-card p-5 flex flex-col">
        <h2 class="text-base font-bold text-white mb-4">🍰 Top 5 des Matières</h2>
        <div class="overflow-x-auto flex-1">
          <table class="w-full text-left text-sm">
            <thead>
              <tr class="border-b border-white/10 text-xs text-slate-400 uppercase">
                <th class="py-2.5 px-3">Matière</th>
                <th class="py-2.5 px-3 text-right">Moyenne</th>
              </tr>
            </thead>
            <tbody id="topMatieresBody" class="divide-y divide-white/5"></tbody>
          </table>
        </div>
      </div>
    </section>

    <hr class="border-white/10 my-6" />

    <!-- Classement des Etudiants -->
    <section class="st-card p-5 mb-8">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
        <div>
          <h2 class="text-base font-bold text-white">🏆 Classement et Moyennes Pondérées par Étudiant</h2>
          <p id="rankingCountLabel" class="text-xs text-slate-400 mt-0.5">Calcul pondéré par les coefficients des matières</p>
        </div>
        <div class="flex items-center gap-2">
          <button id="prevPage" class="px-3 py-1 rounded bg-white/5 hover:bg-white/10 text-xs font-semibold disabled:opacity-40">◀ Précédent</button>
          <span id="pageInfo" class="text-xs text-slate-300 font-medium">Page 1</span>
          <button id="nextPage" class="px-3 py-1 rounded bg-white/5 hover:bg-white/10 text-xs font-semibold disabled:opacity-40">Suivant ▶</button>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead>
            <tr class="border-b border-white/10 text-xs text-slate-400 uppercase bg-white/[0.02]">
              <th class="py-3 px-3">Rang</th>
              <th class="py-3 px-3">ID Étudiant</th>
              <th class="py-3 px-3">Nom de l'Étudiant</th>
              <th class="py-3 px-3">Filière</th>
              <th class="py-3 px-3">Niveau</th>
              <th class="py-3 px-3 text-right">Moyenne Pondérée</th>
            </tr>
          </thead>
          <tbody id="studentRankingBody" class="divide-y divide-white/5"></tbody>
        </table>
      </div>
    </section>

    <!-- Expander Corps Enseignant -->
    <details class="st-card p-5 group">
      <summary class="cursor-pointer font-bold text-sm text-white flex items-center justify-between list-none">
        <span>👨‍🏫 Voir le Corps Enseignant &amp; Affectation des Matières (10 Professeurs)</span>
        <span class="text-slate-400 group-open:rotate-180 transition-transform">▼</span>
      </summary>
      <div class="mt-4 overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead>
            <tr class="border-b border-white/10 text-xs text-slate-400 uppercase">
              <th class="py-2.5 px-3">ID</th>
              <th class="py-2.5 px-3">Nom &amp; Prénom</th>
              <th class="py-2.5 px-3">Grade</th>
              <th class="py-2.5 px-3">Spécialité</th>
              <th class="py-2.5 px-3">Email</th>
            </tr>
          </thead>
          <tbody id="profBody" class="divide-y divide-white/5"></tbody>
        </table>
      </div>
    </details>
  </main>

  <script>
    // [id_etudiant, nom_etudiant, filiere, niveau, nom_matiere, coefficient, note, semestre, annee_academique]
    const COMP_ROWS = {json.dumps(comp_rows, ensure_ascii=False)};
    const PROFESSEURS = {json.dumps(prof_records, ensure_ascii=False)};
    const ANNEES = {json.dumps(annees, ensure_ascii=False)};
    const SEMESTRES = {json.dumps(semestres, ensure_ascii=False)};
    const FILIERES = {json.dumps(filieres, ensure_ascii=False)};
    const NIVEAUX = {json.dumps(niveaux, ensure_ascii=False)};

    function fillSelect(id, allLabel, items) {{
      const el = document.getElementById(id);
      el.innerHTML = `<option value="ALL">${{allLabel}}</option>` +
        items.map(i => `<option value="${{i}}">${{i}}</option>`).join('');
    }}

    fillSelect('selAnnee', 'Toutes', ANNEES);
    fillSelect('selSemestre', 'Tous', SEMESTRES);
    fillSelect('selFiliere', 'Toutes', FILIERES);
    fillSelect('selNiveau', 'Tous', NIVEAUX);

    const profBody = document.getElementById('profBody');
    profBody.innerHTML = PROFESSEURS.map(p => `
      <tr class="hover:bg-white/[0.02]">
        <td class="py-2.5 px-3 text-slate-400">#${{p.id_professeur}}</td>
        <td class="py-2.5 px-3 font-semibold text-white">${{p.prenom || ''}} ${{p.nom || p.nom_professeur || ''}}</td>
        <td class="py-2.5 px-3 text-indigo-300">${{p.grade || 'Enseignant-Chercheur'}}</td>
        <td class="py-2.5 px-3 text-slate-300">${{p.specialite || p.departement || 'Informatique & Data'}}</td>
        <td class="py-2.5 px-3 text-slate-400">${{p.email || ''}}</td>
      </tr>
    `).join('');

    let chartInstance = null;
    let currentRanking = [];
    let currentPage = 1;
    const pageSize = 15;

    function renderRankingPage() {{
      const tbody = document.getElementById('studentRankingBody');
      const totalPages = Math.max(1, Math.ceil(currentRanking.length / pageSize));
      if (currentPage > totalPages) currentPage = totalPages;
      const start = (currentPage - 1) * pageSize;
      const slice = currentRanking.slice(start, start + pageSize);

      tbody.innerHTML = slice.map((s, idx) => {{
        const rank = start + idx + 1;
        const badgeColor = s.gpa >= 14 ? 'text-emerald-400 bg-emerald-500/10' : (s.gpa >= 10 ? 'text-indigo-300 bg-indigo-500/10' : 'text-rose-400 bg-rose-500/10');
        return `
          <tr class="hover:bg-white/[0.02]">
            <td class="py-2.5 px-3 font-bold text-slate-400">${{rank}}</td>
            <td class="py-2.5 px-3 text-slate-300">${{s.id_etudiant}}</td>
            <td class="py-2.5 px-3 font-semibold text-white">${{s.nom_etudiant}}</td>
            <td class="py-2.5 px-3 text-slate-300">${{s.filiere}}</td>
            <td class="py-2.5 px-3 text-slate-300">${{s.niveau}}</td>
            <td class="py-2.5 px-3 text-right">
              <span class="px-2.5 py-1 rounded-md font-bold text-xs ${{badgeColor}}">${{s.gpa.toFixed(2)}} / 20</span>
            </td>
          </tr>
        `;
      }}).join('');

      document.getElementById('pageInfo').textContent = `Page ${{currentPage}} / ${{totalPages}} (${{currentRanking.length}} étudiants)`;
      document.getElementById('prevPage').disabled = currentPage <= 1;
      document.getElementById('nextPage').disabled = currentPage >= totalPages;
    }}

    function updateDashboard() {{
      const annee = document.getElementById('selAnnee').value;
      const semestre = document.getElementById('selSemestre').value;
      const filiere = document.getElementById('selFiliere').value;
      const niveau = document.getElementById('selNiveau').value;
      const q = document.getElementById('searchQuery').value.trim().toLowerCase();

      const filtered = COMP_ROWS.filter(r => {{
        if (annee !== 'ALL' && r[8] !== annee) return false;
        if (semestre !== 'ALL' && r[7] !== semestre) return false;
        if (filiere !== 'ALL' && r[2] !== filiere) return false;
        if (niveau !== 'ALL' && r[3] !== niveau) return false;
        if (q && !r[1].toLowerCase().includes(q)) return false;
        return true;
      }});

      const totalEvals = filtered.length;
      const uniqueStudents = new Set(filtered.map(r => r[0])).size;
      const avgGpa = totalEvals > 0 ? (filtered.reduce((a, b) => a + b[6], 0) / totalEvals) : 0;
      const admisCount = filtered.filter(r => r[6] >= 10.0).length;
      const passRate = totalEvals > 0 ? ((admisCount / totalEvals) * 100) : 0;

      document.getElementById('kpiStudents').textContent = `${{uniqueStudents}} / 360`;
      document.getElementById('kpiGpa').textContent = `${{avgGpa.toFixed(2)}} / 20`;
      document.getElementById('kpiPassRate').textContent = `${{passRate.toFixed(1)}} %`;
      document.getElementById('kpiPassSub').textContent = `${{admisCount}} / ${{totalEvals}} Évaluations`;
      document.getElementById('kpiTotalEvals').textContent = `${{totalEvals}} Notes`;

      // Moyenne par Filiere
      const byFiliere = {{}};
      filtered.forEach(r => {{
        if (!byFiliere[r[2]]) byFiliere[r[2]] = {{ sum: 0, count: 0 }};
        byFiliere[r[2]].sum += r[6];
        byFiliere[r[2]].count += 1;
      }});
      const filLabels = Object.keys(byFiliere);
      const filValues = filLabels.map(k => +(byFiliere[k].sum / byFiliere[k].count).toFixed(2));

      if (chartInstance) chartInstance.destroy();
      const ctx = document.getElementById('filiereChart').getContext('2d');
      chartInstance = new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: filLabels,
          datasets: [{{
            label: 'Moyenne (/20)',
            data: filValues,
            backgroundColor: '#6366f1',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            y: {{ beginAtZero: true, max: 20, grid: {{ color: 'rgba(255,255,255,0.06)' }}, ticks: {{ color: '#94a3b8' }} }},
            x: {{ grid: {{ display: false }}, ticks: {{ color: '#cbd5e1' }} }}
          }}
        }}
      }});

      // Top 5 Matieres
      const byMat = {{}};
      filtered.forEach(r => {{
        if (!byMat[r[4]]) byMat[r[4]] = {{ sum: 0, count: 0 }};
        byMat[r[4]].sum += r[6];
        byMat[r[4]].count += 1;
      }});
      const topMats = Object.keys(byMat)
        .map(k => ({{ nom_matiere: k, note: byMat[k].sum / byMat[k].count }}))
        .sort((a, b) => b.note - a.note)
        .slice(0, 5);

      document.getElementById('topMatieresBody').innerHTML = topMats.map(m => `
        <tr class="hover:bg-white/[0.02]">
          <td class="py-2.5 px-3 font-medium text-slate-200">${{m.nom_matiere}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-indigo-400">${{m.note.toFixed(2)}} / 20</td>
        </tr>
      `).join('');

      // Classement Pondere par Etudiant
      const byStu = {{}};
      filtered.forEach(r => {{
        const key = r[0];
        if (!byStu[key]) {{
          byStu[key] = {{
            id_etudiant: r[0],
            nom_etudiant: r[1],
            filiere: r[2],
            niveau: r[3],
            wSum: 0,
            cSum: 0
          }};
        }}
        byStu[key].wSum += r[6] * r[5];
        byStu[key].cSum += r[5];
      }});

      currentRanking = Object.values(byStu)
        .map(s => ({{ ...s, gpa: s.cSum > 0 ? (s.wSum / s.cSum) : 0 }}))
        .sort((a, b) => b.gpa - a.gpa);

      currentPage = 1;
      renderRankingPage();
    }}

    ['selAnnee', 'selSemestre', 'selFiliere', 'selNiveau'].forEach(id => {{
      document.getElementById(id).addEventListener('change', updateDashboard);
    }});
    document.getElementById('searchQuery').addEventListener('input', updateDashboard);
    document.getElementById('resetBtn').addEventListener('click', () => {{
      ['selAnnee', 'selSemestre', 'selFiliere', 'selNiveau'].forEach(id => document.getElementById(id).value = 'ALL');
      document.getElementById('searchQuery').value = '';
      updateDashboard();
    }});
    document.getElementById('prevPage').addEventListener('click', () => {{
      if (currentPage > 1) {{ currentPage--; renderRankingPage(); }}
    }});
    document.getElementById('nextPage').addEventListener('click', () => {{
      currentPage++; renderRankingPage();
    }});

    updateDashboard();
  </script>
</body>
</html>
"""

out_dir = os.path.join(base_dir, "web_demo")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "index.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

# Also copy to root index.html so whichever branch GitHub Pages uses, index.html is served!
root_index = os.path.join(base_dir, "index.html")
with open(root_index, "w", encoding="utf-8") as f:
    f.write(html)

print("Generated web_demo/index.html and root index.html successfully:", len(html), "bytes")
