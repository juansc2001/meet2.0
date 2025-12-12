from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import tipos_de_servicos

def home_page(request):
    return render(request, 'home.html')


@login_required(login_url='/login/')
def servicos(request):
    if request.user.is_staff == False:#apenas admins tem acesso a essa pagina
        return redirect('home')
    

    if request.method == "GET":
        return render(request, 'servicos.html')
    elif(request.method == "POST"):
        
        form_tratado = False
        while(form_tratado == False):
            servico = request.POST.get('servico')
            tempo = request.POST.get('duracao')
            if tempo == '':# trata os dados do formulario
                #falta notify the user
                print('tempo errado')
                return redirect('servico_adm')
            elif len(servico) > 30 or len(servico) <= 1:
                #falta notify the user
                print('servico errado')
                return redirect('servico_adm')
            else:
                form_tratado = True


        #salva os dados
        servc = tipos_de_servicos(
            servico_nome = servico,
            tempo_duracao = tempo,
        )
        servc.save()
        
        return render(request, 'servicos.html')
    

def agendar(request):
    if request.method == "GET":
        opcoes_servico = tipos_de_servicos.objects.all()
        return render(request, 'agendar.html', {'servico_opc': opcoes_servico})
    
    elif request.method == "POST":

        #coleta todos os dados do formulario
        cliente_formulario = request.POST.get("cliente")
        data_formulario = request.POST.get("data")
        servico = request.POST.get('servicos_opçoes')  
        servico_selecionado = tipos_de_servicos.objects.get(id=servico)
        print(f" nome do cliente: {cliente_formulario} \n data: {data_formulario} \n servico: {servico}") #mecher no "data formulario"


        #tratar os dados do formulario
        


        return redirect('agendar_form')

    

    