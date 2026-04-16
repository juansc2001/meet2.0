const tabela = document.getElementById("tabela")
const inputBusca = document.getElementById("busca-nome");

const btnFiltro = document.getElementById("btn-filtro");
    const opcoesFiltro = document.getElementById("opcoes-filtro");

    btnFiltro.addEventListener("click", () => {
        opcoesFiltro.style.display =
            opcoesFiltro.style.display === "block" ? "none" : "block";
    });

    document.addEventListener("click", function(event) {
        if (!btnFiltro.contains(event.target) && !opcoesFiltro.contains(event.target)) {
            opcoesFiltro.style.display = "none";
        }
    });


mypromisse_exibir_H = fetch('/API_exibir_horarios/')//verificar a segurança
mypromisse_exibir_H.then((response) =>{
    return response.json()
})
.then((data)=>{
    dadosGlobais = data;
    renderizarTabela(data);
})
.catch((err)=>{
    console.log(`deu algo errado ai man${err}`)
})





const servicosMap = {
    "1": "Consultoria",
    "2": "Mentoria",
    "3": "Reunião Técnica"
};




//cria a tabela com os horarios
/*
function renderizarTabela(dados) {
    tabela.innerHTML = ""; // limpa tabela antes de recriar

    dados.forEach(item => {
        const dataObj = new Date(item.horario);

        const diaSemana = dataObj.toLocaleDateString("pt-BR", { weekday: "long" });
        const dataFormatada = dataObj.toLocaleDateString("pt-BR");
        const hora = dataObj.toLocaleTimeString("pt-BR", { hour: '2-digit', minute: '2-digit' });

        const linha = `
            <tr>
                <td>${item.nome}</td>
                <td>${item.servico}</td>
                <td>${diaSemana}</td>
                <td>${dataFormatada}</td>
                <td>${hora}</td>
            </tr>
        `;

        tabela.innerHTML += linha;
    });
}*/
//cria a tabela com os horarios v2
function renderizarTabela(dados) {
    tabela.innerHTML = "";

    dados.forEach((item, index) => {
        const dataObj = new Date(item.horario);

        const diaSemana = dataObj.toLocaleDateString("pt-BR", { weekday: "long" });
        const dataFormatada = dataObj.toLocaleDateString("pt-BR");
        const hora = dataObj.toLocaleTimeString("pt-BR", { hour: '2-digit', minute: '2-digit' });

        const nomeServico = servicosMap[item.servico] || "Desconhecido";

        const tr = document.createElement("tr");

        tr.classList.add("linha-animada");

        // delay progressivo
        tr.style.animationDelay = `${index * 0.5}s`;

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





//filtros
const botoesFiltro = document.querySelectorAll("#opcoes-filtro button");
botoesFiltro[0].addEventListener("click", () => {
    const ordenado = [...dadosGlobais].sort((a, b) => 
        a.nome.localeCompare(b.nome)
    );

    renderizarTabela(ordenado);
});
botoesFiltro[1].addEventListener("click", () => {
    const ordenado = [...dadosGlobais].sort((a, b) => 
        new Date(a.horario).getDay() - new Date(b.horario).getDay()
    );

    renderizarTabela(ordenado);
});
botoesFiltro[2].addEventListener("click", () => {
    const agora = new Date();

    const ordenado = [...dadosGlobais].sort((a, b) => 
        new Date(a.horario) - new Date(b.horario)
    );

    renderizarTabela(ordenado);
});
botoesFiltro[3].addEventListener("click", () => {
    renderizarTabela(dadosGlobais);
});

//faz a busca por nome
inputBusca.addEventListener("input", () => {
    const valor = inputBusca.value.toLowerCase();

    const filtrados = dadosGlobais.filter(item =>
        item.nome.toLowerCase().includes(valor)
    );

    renderizarTabela(filtrados);
});