// Raw Dataset from SQL / DW
const initialStudents = [
    { rank: 1, id: 1003, name: "Moussa Gaye", filiere: "Data Engineering", niveau: "Master 2", gpa: 18.33, mention: "Très Bien", status: "Admis" },
    { rank: 2, id: 1001, name: "Ibrahima Fall", filiere: "Data Engineering", niveau: "Master 1", gpa: 16.75, mention: "Très Bien", status: "Admis" },
    { rank: 3, id: 1007, name: "Babacar Kane", filiere: "Intelligence Artificielle", niveau: "Master 2", gpa: 17.00, mention: "Très Bien", status: "Admis" },
    { rank: 4, id: 1006, name: "Khadija Seck", filiere: "Intelligence Artificielle", niveau: "Master 1", gpa: 15.50, mention: "Bien", status: "Admis" },
    { rank: 5, id: 1002, name: "Aminata Ba", filiere: "Data Engineering", niveau: "Master 1", gpa: 14.63, mention: "Bien", status: "Admis" },
    { rank: 6, id: 1008, name: "Oumar Sy", filiere: "Cybersécurité", niveau: "Licence 3", gpa: 14.50, mention: "Bien", status: "Admis" },
    { rank: 7, id: 1009, name: "Awa Camara", filiere: "Data Engineering", niveau: "Master 1", gpa: 11.50, mention: "Passable", status: "Admis" },
    { rank: 8, id: 1004, name: "Mariama Cissé", filiere: "Génie Logiciel", niveau: "Licence 3", gpa: 11.75, mention: "Passable", status: "Admis" },
    { rank: 9, id: 1005, name: "Modou Sarr", filiere: "Génie Logiciel", niveau: "Master 1", gpa: 11.25, mention: "Passable", status: "Admis" },
    { rank: 10, id: 1010, name: "Jean Mendy", filiere: "Génie Logiciel", niveau: "Licence 3", gpa: 8.50, mention: "Ajourné", status: "Ajourné" }
];

const professorsData = [
    { name: "Dr. Diop Fatou", dept: "Base de Données & Data", courses: "SQL, MongoDB (4 classes)" },
    { name: "Prof. Diallo Mamadou", dept: "Informatique & Big Data", courses: "Hadoop/Spark, Data Warehousing (3 classes)" },
    { name: "Dr. Sow Aïssatou", dept: "Intelligence Artificielle", courses: "Machine Learning, Python (2 classes)" },
    { name: "Ing. Ndiaye Cheikh", dept: "Génie Logiciel", courses: "Architecture Microservices (2 classes)" },
    { name: "Dr. Faye Ousmane", dept: "Cybersécurité", courses: "Sécurité des SI (1 classe)" }
];

let filiereChartInstance = null;
let mentionChartInstance = null;

document.addEventListener("DOMContentLoaded", () => {
    renderTable(initialStudents);
    renderProfessors();
    initCharts(initialStudents);
    updateKPIs(initialStudents);
});

function updateKPIs(students) {
    document.getElementById("totalStudents").innerText = students.length;
    
    if (students.length === 0) {
        document.getElementById("avgGpa").innerText = "N/A";
        document.getElementById("passRate").innerText = "0%";
        return;
    }

    const totalGpa = students.reduce((acc, curr) => acc + curr.gpa, 0);
    const avgGpa = (totalGpa / students.length).toFixed(2);
    document.getElementById("avgGpa").innerText = `${avgGpa} / 20`;

    const passCount = students.filter(s => s.status === "Admis").length;
    const passPct = Math.round((passCount / students.length) * 100);
    document.getElementById("passRate").innerText = `${passPct} %`;
}

function renderTable(students) {
    const tbody = document.getElementById("studentTableBody");
    tbody.innerHTML = "";

    students.forEach((s, idx) => {
        const badgeClass = getBadgeClass(s.mention);
        const statusClass = s.status === "Admis" ? "status-admis" : "status-ajourne";

        const row = `
            <tr>
                <td><strong>#${idx + 1}</strong></td>
                <td><strong>${s.name}</strong> <br><small style="color:#9ca3af">ID: ${s.id}</small></td>
                <td>${s.filiere}</td>
                <td>${s.niveau}</td>
                <td><strong style="font-size:16px; color:#818cf8">${s.gpa.toFixed(2)}</strong></td>
                <td><span class="badge ${badgeClass}">${s.mention}</span></td>
                <td><span class="${statusClass}"><i class="fa-solid ${s.status === 'Admis' ? 'fa-check-circle' : 'fa-times-circle'}"></i> ${s.status}</span></td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

function getBadgeClass(mention) {
    switch (mention) {
        case "Très Bien": return "tb";
        case "Bien": return "b";
        case "Assez Bien": return "ab";
        case "Passable": return "p";
        default: return "aj";
    }
}

function renderProfessors() {
    const grid = document.getElementById("profGrid");
    grid.innerHTML = "";

    professorsData.forEach(p => {
        const card = `
            <div class="prof-card">
                <h4><i class="fa-solid fa-chalkboard-user"></i> ${p.name}</h4>
                <p><strong>Département:</strong> ${p.dept}</p>
                <p><strong>Cours:</strong> ${p.courses}</p>
            </div>
        `;
        grid.innerHTML += card;
    });
}

function initCharts(students) {
    // 1. Chart Moyenne par Filière
    const filieres = ["Data Engineering", "Génie Logiciel", "Intelligence Artificielle", "Cybersécurité"];
    const avgByFiliere = filieres.map(f => {
        const list = students.filter(s => s.filiere === f);
        if (list.length === 0) return 0;
        return (list.reduce((acc, c) => acc + c.gpa, 0) / list.length).toFixed(2);
    });

    const ctx1 = document.getElementById("filiereChart").getContext("2d");
    if (filiereChartInstance) filiereChartInstance.destroy();

    filiereChartInstance = new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: filieres,
            datasets: [{
                label: 'Moyenne (sur 20)',
                data: avgByFiliere,
                backgroundColor: ['#6366f1', '#06b6d4', '#10b981', '#f59e0b'],
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { min: 0, max: 20, grid: { color: 'rgba(255,255,255,0.05)' } },
                x: { grid: { display: false } }
            }
        }
    });

    // 2. Chart Mention Distribution
    const mentionsCount = { "Très Bien": 0, "Bien": 0, "Passable": 0, "Ajourné": 0 };
    students.forEach(s => {
        if (mentionsCount[s.mention] !== undefined) mentionsCount[s.mention]++;
    });

    const ctx2 = document.getElementById("mentionChart").getContext("2d");
    if (mentionChartInstance) mentionChartInstance.destroy();

    mentionChartInstance = new Chart(ctx2, {
        type: 'doughnut',
        data: {
            labels: Object.keys(mentionsCount),
            datasets: [{
                data: Object.values(mentionsCount),
                backgroundColor: ['#10b981', '#22d3ee', '#fbbf24', '#f87171'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#f3f4f6' } }
            }
        }
    });
}

function filterData() {
    const selectedFiliere = document.getElementById("filiereFilter").value;
    const selectedNiveau = document.getElementById("niveauFilter").value;

    let filtered = initialStudents.filter(s => {
        const matchFiliere = (selectedFiliere === "ALL" || s.filiere === selectedFiliere);
        const matchNiveau = (selectedNiveau === "ALL" || s.niveau === selectedNiveau);
        return matchFiliere && matchNiveau;
    });

    renderTable(filtered);
    updateKPIs(filtered);
    initCharts(filtered);
}

function searchTable() {
    const query = document.getElementById("searchInput").value.toLowerCase();
    const rows = document.querySelectorAll("#studentTableBody tr");

    rows.forEach(r => {
        const text = r.innerText.toLowerCase();
        r.style.display = text.includes(query) ? "" : "none";
    });
}
