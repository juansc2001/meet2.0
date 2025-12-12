document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("dataHora");

    // quando o usuário clicar, mudamos para datetime-local
    input.addEventListener("focus", () => {
        input.type = "datetime-local";
        input.showPicker?.(); // abre o calendário automáticamente (Chrome)
    });

    // depois que o usuário selecionar, transformar em texto amigável
    input.addEventListener("change", () => {
        const valor = input.value; // formato "2025-03-02T15:30"
        if (!valor) return;

        const data = new Date(valor);

        const dia = data.toLocaleDateString("pt-BR", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric"
        });

        const horas = data.toLocaleTimeString("pt-BR", {
            hour: "2-digit",
            minute: "2-digit"
        });

        // salva o valor real como atributo
        input.dataset.realValue = valor;

        // mostra formatado no input
        input.type = "text";
        input.value = `${dia} às ${horas}`;
    });
});