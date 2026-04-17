from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import tipos_de_servicos, dias_inoperante, horario_de_funcionamento, horarios_agendados
import json
from django.http import JsonResponse#classe pronta no django para retornar json pro navegador
import datetime
from django.utils import timezone
from zoneinfo import ZoneInfo

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
    

@login_required(login_url='/login/')
def agendar(request):
    if request.method == "GET":
        opcoes_servico = tipos_de_servicos.objects.all()
        return render(request, 'agendar.html', {'servico_opc': opcoes_servico})
    
    elif request.method == "POST":
        


        #coleta os dados json do formulario
        formulario_inf = request.body
        lista_objts = json.loads(formulario_inf)
        horario = lista_objts[1]
        informacoes = lista_objts[0]



        #trata os dados json do formulario e transforma em dicionario
        if(horario['horario_marcado'] == '' or informacoes['servico'] == '' or informacoes['nome'] == ''):
            #enviar uma menssagem ao usuario, preencha todo o formulario, e reevia o formulario
            print('algum campo esta vazio')
            return redirect('agendar_form')
        else:
            HH = datetime.datetime.strptime(horario['horario_marcado'] , '%Y-%m-%dT%H:%M')
            HH_timezone = timezone.make_aware(HH,ZoneInfo(informacoes['timeZone']))

        agendamento = {'nome': informacoes['nome'], 'servico': informacoes['servico'], 'horarios': HH, 'horario_timezone': HH_timezone}


         
        


        #verifica se o agendamento foi feito dentro do horario que a loja funciona
        horario_funcionamento = horario_de_funcionamento.objects.all()
        horario_agendado = agendamento['horarios']
        for H in horario_funcionamento:
            HH_inicio = H.horario_de_funcionamento_inicio
            HH_fim = H.horario_de_funcionamento_fim
            H_agendado = horario_agendado.time()
            if H_agendado >= HH_inicio and H_agendado <= HH_fim :
                print(f"agendado dentro do horario de funcionamento{H.horario_de_funcionamento_inicio},{H.horario_de_funcionamento_fim}")






                #verifica se o agendamento foi feito em dias que a empresa funciona
                dt_agendado = horario_agendado.date()
                dias_funciona = dias_inoperante.objects.all()
                for DT_disponiveis in dias_funciona:
                    if dt_agendado == DT_disponiveis.dia_funcionando_inteiro:
                        print('este dia nao funcionamos')
                        return redirect('agendar_form')                    
                    else:
                        print("esse dia funciona")
                        
                        
                        





                        
                        #verifica se ja nao existe um agendamento naquele horario marcado pelo user
                        servico_selecionado_user = tipos_de_servicos.objects.filter(id = agendamento['servico'])
                        for servico in servico_selecionado_user:
                            tempo_duracao_servico = servico.tempo_duracao
                            tempo_duracao_servico = datetime.timedelta(
                                hours= tempo_duracao_servico.hour,
                                minutes= tempo_duracao_servico.minute,
                                seconds= tempo_duracao_servico.second,
                            )
                        Horario_data_agendado_user = agendamento['horarios']
                        horario_agendado_final_user = Horario_data_agendado_user + tempo_duracao_servico
                        horarios_marcados = horarios_agendados.objects.all()
                        
                        #coloquei essas datetime.time com timezone pq estava dando problema
                        Horario_data_agendado_user_dt_aware = timezone.make_aware(Horario_data_agendado_user, ZoneInfo("America/Sao_Paulo"))
                        horario_agendado_final_user_dt_aware = timezone.make_aware(horario_agendado_final_user, ZoneInfo("America/Sao_Paulo"))

                        conflito = True
                        if len(horarios_marcados) == 0:
                            conflito = False
                        for agendado in horarios_marcados:
                            #Preferi converter para naive, pois o formato aware estava causando conflitos. Não achei ideal desativar o fuso horário de toda a aplicação apenas para evitar que os horários viessem como datetime aware do banco de dados.
                            horario_agendado_inicial_naive = agendado.horario_agendado_inicial.replace(tzinfo=None)
                            horario_agendado_final_naive = agendado.horario_agendado_final.replace(tzinfo=None)

                            if(horario_agendado_inicial_naive < horario_agendado_final_user) and (Horario_data_agendado_user < horario_agendado_final_naive):
                                print('ja existe um agendamento feito esse horario')
                                conflito = True
                                break
                            else:                                
                                print('semconflito')
                                conflito = False
                        

                        usuario_agendou_salva = agendamento['horario_timezone']
                        usuario_agendou_salva_fim = agendamento['horario_timezone'] + tempo_duracao_servico
                        #essa parte é responsavel por agendar o horario
                        if(conflito == False):
                            salvando_dados = horarios_agendados(
                                cliente = agendamento['nome'],
                                horario_agendado_inicial = Horario_data_agendado_user,
                                horario_agendado_final = horario_agendado_final_user,
                                servico = agendamento['servico'],
                            )
                            salvando_dados.save()



            else:
                print('este horario nao funcionamos')
                return redirect('agendar_form')



        return redirect('agendar_form')

    





def dia_disponivel(request):
    if request.method == 'GET':
        return render(request, 'dia_disponivel.html' )







@login_required(login_url='/login/')
def exibir_horarios(request):
    return render(request, 'exibir_horarios.html')



def API_exibir_horarios(request):
    #API que manda um json dos dados agendados pro frontend
    dados = horarios_agendados.objects.all()
    lista_agendados = []
    for dado in dados:
        agenda = {
            'nome': dado.cliente,
            'horario': dado.horario_agendado_inicial,
            'servico': dado.servico,
            #seria interesante ter o numero de telefone do usuario
        }
        lista_agendados.append(agenda)
    return JsonResponse(lista_agendados, safe=False)
    