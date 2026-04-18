function getCookie(name) {//função padrão para ler cookies
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("dataHora");
    const name = document.getElementById("cliente")
    const servico = document.getElementById("servico")
    let horario_marcado = ''
    const botao = document.getElementById('botao_form')

    
    // quando o usuário clicar, mudamos para datetime-local
    input.addEventListener("focus", () => {
        input.type = "datetime-local";
        input.showPicker?.(); // abre o calendário automáticamente (Chrome)
    });

    // depois que o usuário selecionar, transformar em texto amigável
    input.addEventListener("change", () => {

        
        const valor = input.value; // formato "2025-03-02T15:30"
        horario_marcado = valor;//guarda o objeto data nao formatado
        
        if (!valor) return;//evitar bug valor null, return nao retorna nada

        const data = new Date(valor);
        //aqui

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


    //envia os dados para o backend
    botao.addEventListener("click",() => {
        const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;//coleta o timezone
        const obj_form = [{//cria um objeto com os dados do formulario e transforma em json
            nome: name.value,
            servico: servico.value,
            timeZone: timezone
        },
        {horario_marcado}
        ]
        const form_json = JSON.stringify(obj_form)


        //enviando o json com fetchapi 
        fetch("http://127.0.0.1:8000/agendar_reuniao/",{
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: form_json,
            credentials: "same-origin"
        })

        console.log(`${horario_marcado}, ${name.value}, ${servico.value}`)
        console.log(form_json)
    })

});