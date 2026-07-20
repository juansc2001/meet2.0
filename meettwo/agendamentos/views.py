from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.messages import get_messages

from . models import tipos_de_servicos, dias_inoperante, horario_de_funcionamento, horarios_agendados

import json
from django.http import JsonResponse#classe pronta no django para retornar json pro navegador
import datetime
from django.utils import timezone
from zoneinfo import ZoneInfo


#O urlencode() transforma um dicionário Python em parâmetros de URL.
from urllib.parse import urlencode

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
                messages.add_message(
                    request,
                    messages.INFO,
                    'campo tempo esta errado'
                )
                return redirect('servico_adm')
            elif len(servico) > 30 or len(servico) <= 1:
                #falta notify the user
                print('servico errado')
                messages.add_message(
                    request,
                    messages.INFO,
                    'campo serviço nao pode ser menor que um caracter'
                )
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
    
#uma solução do messages que eu implementei para o fetch da pagina agendar
def API_menssagem_agendar(request):
     return JsonResponse({
        'status': 'erro',
        'mensagem': 'Preencha todos os campos'
    })
@login_required(login_url='/login/')
def agendar(request):
    if request.method == "GET":

        #envia a menssagem site foi aberto 
        '''
        messages.add_message(
                request,
                messages.INFO,
                'site foi aberto'
            )
        '''
        
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

            #grava uma menssagem para ser exibida no começo da pagina
            #nao esta funcionando
            print('algum campo esta vazio1')
            messages.add_message(
                request,
                messages.INFO,
                'algum campo esta vazio'
            )
            return JsonResponse({
            'status': 'erro',
            'mensagem': 'Preencha todos os campos'
            })
            
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
                        messages.add_message(
                            request,
                            messages.INFO,
                            'esse dia nao funcionamos'
                        )
                        return JsonResponse({
                        'status': 'erro',
                        'mensagem': 'dia indisponivel'
                        })
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
                                messages.add_message(
                                    request,
                                    messages.INFO,
                                    'ja existe um agendamento feito esse horario'
                                )
                                return JsonResponse({
                                'status': 'erro',
                                'mensagem': 'ja existe um horario agendado'
                                })
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
                                
                            messages.add_message(
                                request,
                                messages.INFO,
                                'dados salvos com sucesso'
                            )
                            return JsonResponse({
                            'status': 'erro',
                            'mensagem': 'dados salvos'
                            })
                            
                            



            else:
                print('este horario nao funcionamos')

                messages.add_message(
                    request,
                    messages.INFO,
                    'este horario nao funcionamos'
                )
                return JsonResponse({
                'status': 'erro',
                'mensagem': 'horario de desligamento da empresa'
                })
                return redirect('agendar_form')



        return redirect('agendar_form')

    





def dia_disponivel(request):
    if request.method == 'GET':
        return render(request, 'dia_disponivel.html' )







@login_required(login_url='/login/')
def exibir_horarios(request):

    #deleta os horarios agendados que tem mais de 30 dias
    hoje = timezone.now()
    mes_passado = hoje - datetime.timedelta(days=30)
    horarios_mes_passado = horarios_agendados.objects.filter(horario_agendado_inicial__lt= mes_passado)
    horarios_mes_passado.delete()

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



@login_required(login_url='/login/')
def desmarcar(request):
    if request.method == 'GET':
        return render(request, 'desmarcar.html')

    if request.method == 'POST':
        #coleta os dados do formulario
        nome = request.POST.get('nome_cliente')
        hora_data = request.POST.get('hora_marcada')
        hora_data_formatados = datetime.datetime.strptime(hora_data, "%Y-%m-%dT%H:%M")



        #pesquisa o cliente que o usuario esta preocurando
        agendamentos_feitos = horarios_agendados.objects.filter(
            cliente=nome,
            horario_agendado_inicial =hora_data_formatados
        )
        if not agendamentos_feitos.exists():
            print('nao foi encontrado este horario marcado')
            messages.add_message(
                request,
                messages.INFO,
                'nao foi encontrado este horario marcado'
            )
            
        
        #deleta o agendamento que foi encontrado
        else:
            for agendamento in agendamentos_feitos:
                agendamento.delete()   
                messages.add_message(
                    request,
                    messages.INFO,
                    f'deletado com sucesso cliente {agendamento.cliente}'
                )
            
        
        
        return render(request, 'desmarcar.html')