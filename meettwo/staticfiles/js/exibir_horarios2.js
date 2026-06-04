const tabela = document.getElementById("tabela");
const inputBusca = document.getElementById("busca-nome");

const btnFiltro = document.getElementById("btn-filtro");
const opcoesFiltro = document.getElementById("opcoes-filtro");

let dadosGlobais = [];

const servicosMap = {
    "1": "Consultoria",
    "2": "Mentoria",
    "3": "Reunião Técnica"
};

// =====================
// MENU DE FILTROS
// =====================

btnFiltro.addEventListener("click", () => {
    opcoesFiltro.style.display =
        opcoesFiltro.style.display === "block"
            ? "none"
            : "block";
});

document.addEventListener("click", (event) => {
    if (
        !btnFiltro.contains(event.target) &&
        !opcoesFiltro.contains(event.target)
    ) {
        opcoesFiltro.style.display = "none";
    }
});

// =====================
// BUSCAR DADOS
// =====================

fetch("/API_exibir_horarios/")
    .then(response => response.json())
    .then(data => {
        dadosGlobais = data;
        renderizarTabela(data);
    })
    .catch(err => {
        console.error("Erro ao carregar dados:", err);
    });

// =====================
// RENDERIZAR TABELA
// =====================

function renderizarTabela(dados) {

    tabela.innerHTML = "";

    dados.forEach((item, index) => {

        const dataObj = new Date(item.horario);

        const diaSemana = dataObj.toLocaleDateString(
            "pt-BR",
            { weekday: "long" }
        );

        const dataFormatada =
            dataObj.toLocaleDateString("pt-BR");

        const hora =
            dataObj.toLocaleTimeString(
                "pt-BR",
                {
                    hour: "2-digit",
                    minute: "2-digit"
                }
            );

        const nomeServico =
            servicosMap[item.servico] || "Desconhecido";

        const tr = document.createElement("tr");

        tr.classList.add("linha-animada");
        tr.style.animationDelay = `${index * 0.05}s`;

        tr.innerHTML = `
            <td>${item.nome}</td>
            <td>${nomeServico}</td>
            <td>${diaSemana}</td>
            <td>${dataFormatada}</td>
            <td>${hora}</td>
        `;

        tabela.appendChild(tr);
    });
}

// =====================
// FILTROS
// =====================

const botoesFiltro =
    document.querySelectorAll("#opcoes-filtro button");

// Por Nome

botoesFiltro[0].addEventListener("click", () => {

    const ordenado = [...dadosGlobais].sort((a, b) =>
        a.nome.localeCompare(b.nome)
    );

    renderizarTabela(ordenado);
});

// Por Dia da Semana

botoesFiltro[1].addEventListener("click", () => {

    const ordenado = [...dadosGlobais].sort((a, b) =>
        new Date(a.horario).getDay() -
        new Date(b.horario).getDay()
    );

    renderizarTabela(ordenado);
});

// Dia Mais Próximo

botoesFiltro[2].addEventListener("click", () => {

    console.log('clickou')
    const ordenado = [...dadosGlobais].sort((a, b) =>
        new Date(a.horario) - new Date(b.horario)
    );

    renderizarTabela(ordenado);
});

// Ordem de Adição

botoesFiltro[3].addEventListener("click", () => {

    renderizarTabela(dadosGlobais);
});

// =====================
// BUSCA POR NOME
// =====================

inputBusca.addEventListener("input", () => {

    const texto =
        inputBusca.value.toLowerCase();

    const filtrados =
        dadosGlobais.filter(item =>
            item.nome.toLowerCase().includes(texto)
        );

    renderizarTabela(filtrados);
});