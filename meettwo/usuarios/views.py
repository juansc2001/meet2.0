from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from usuarios.models import private_user_info
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required # pra poder usar o @login_required
from django.contrib.auth import login
from django.contrib import messages #https://docs.djangoproject.com/en/5.2/ref/contrib/messages/



def log(request):
    if(request.method == 'GET'):
        print(request.user)
        return render(request, 'login.html')
    elif(request.method == 'POST'):

        #verifica se o usuario existe e realiza o login
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        user_logado = authenticate( username = nome, password=senha)
        if user_logado == None:
            messages.add_message(
                request,
                messages.INFO,
                'usuario ou senha incorretos'
            )
        else:
            login(request, user_logado)


        return render(request, 'login.html')









#https://docs.djangoproject.com/en/5.2/topics/auth/default/
@login_required(login_url='/login/')
def cadastro(request):

    #se o usuario nao for da staff ele nao pode cadastrar novos users
    if request.user.is_staff == True:
        
        if request.method == 'GET':
            print('metodo foi get')
            return render(request, 'cadastro.html')
        
        elif request.method == 'POST':

            tel = request.POST.get('telefone')
            nome= request.POST.get('nome')
            senha = request.POST.get('senha')

            #trata o numero de telefone passado pelo usuario                
            if not tel.isnumeric():
                messages.add_message(
                    request,
                    messages.INFO,
                    'telefone informado esta errado',
                )
                return redirect('cadastrar')
            elif len(tel) > 15:
                messages.add_message(
                    request,
                    messages.INFO,
                    'numero de telefone muito grande',
                )
                return redirect('cadastrar')
            

            #verifica se o usuario cadastrado ja existe
            if User.objects.filter(username=nome).exists() :
                messages.add_message(
                    request,
                    messages.INFO,
                    'este usuario ja esta em uso'
                )
                return redirect('cadastrar')
        
            
            #verifica a senha 
            if len(senha) <= 6:
                messages.add_message(
                    request,
                    messages.INFO,
                    'senha muito curta'
                )
                return redirect('cadastrar') 

            
            
            #salva os dados e cria um usuario 
            #https://docs.djangoproject.com/en/5.2/topics/auth/default/  (User.model)
            user = User.objects.create_user(username=nome, password= senha)
            user.save()
            dados_user = private_user_info(
                usuario = user, #foreingkey só aceita um objeto do banco de dados
                telefone = tel,
            )
            dados_user.save()
            return render(request, 'cadastro.html')
    
    
    else:
        return redirect('login')