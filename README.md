# PythonAPI-Django-MongoDB
Este Projeto traz um passo a passo de como criar uma API em Python com Django e CRUD com o banco de dados não-relacional MongoDB

----------------------------------------------------------------------------------------------------------------------------------------------------------

Instalar o Django

    pip install django

Para criar API's Rest é  preciso instalar o 'django rest framework'

    pip install djangorestframework

Por padrão de segurança o django bloqueia requisições vinda de domínios diferentes, para desativar precisa-se usar o 'django-cors-headers'

    pip install django-cors-headers

Iniciar projeto e executar o projeto no navegador

    django-admin startproject CRUD_API_Django_MongoDB
    python manage.py runserver

Criar um app (pode-se criar mais de um app) para implementar os metodos da API

    python manage.py startapp FuncionarioApp

Adicionar o app e as configurações necessárias no arquivo settings.py

    INSTALLED_APPS -> 'rest_framework', 'corsheaders', 'FuncionarioApp.apps.FuncionarioappConfig' (o app)
    MIDDLEWARE -> 'corsheaders.middleware.CorsMiddleware'

Passar instruções para todos os domínios acessar a API (Não recomendado na produção, apenas adicione os domínios necessários)

    CORS_ORIGIN_ALLOW_ALL = True
    
----------------------------------------------------------------------------------------------------------------------------------------------------------  
# Criar os models necessários no arquivo models.py do app (detalhes do departamento e outro os detalhes do funcionários)

    class Departamentos(models.Model):
        departamentoId = models.AutoField(primary_key=True)
        departamentoNome = models.CharField(max_length=500)

    class Funcionarios(models.Model):
        funcionarioId = models.AutoField(primary_key=True)
        funcionarioNome = models.CharField(max_length=500)
        departamento = models.CharField(max_length=500)
        dataAdesao = models.DateField()
        arquivoFoto = models.CharField(max_length=500)
        
----------------------------------------------------------------------------------------------------------------------------------------------------------         

    

# Conectar com o compass usando a connection string

Irei usar um shared cluster free no MongoDBAtlas com propósito de teste (usar seu ipv4)

    https://www.mongodb.com/cloud/atlas/lp/general/try?utm_source=compass&utm_medium=product
    
----------------------------------------------------------------------------------------------------------------------------------------------------------

# Criar um banco de dados para o app e conectar com o compass usando a connection string

    Ex: mongodb+srv://seunome:<suaSenha>@cluster0.rntos.mongodb.net/test
   
----------------------------------------------------------------------------------------------------------------------------------------------------------    
Instalar o database adapter 

    pip install djongo
  
Como estamos usando o Atlas precisamos instalar o dnspython

    pip install dnspython
    
----------------------------------------------------------------------------------------------------------------------------------------------------------   
# Adicionar os detalhes de conexão ao arquivo settings.py

    DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'CLIENT': {
                "host": "mongodb+srv://gustavo:<suaSenha>@cluster0.rntos.mongodb.net/?retryWrites=true&w=majority", # Conectar o cluster a sua aplicação usando a connection string
                "name": "testeDB",
                "authMechanism": "SCRAM-SHA-1" # Mecanismo de autenticação necessario em caso de conexao com o atlas cloud db
            }
        }
    }
    
----------------------------------------------------------------------------------------------------------------------------------------------------------    
# Criar arquivo serializers (Ajudam a converter tipos de dados complexos e/ou instâncias dos models em python nativo que pode ser renderizada em JSON ou XML) Ele também ajudam na deserialization (Que consiste em converter os dados passados de volta em dados complexos )

    from rest_framework import serializers
    from CRUD_API_Django_MongoDB.FuncionarioApp.models import Departamentos, Funcionarios


    class DepartamentoSerializer(serializers.ModelSerializer):
            class Meta:
                model= Departamentos
                fields= ('departamentoId','departamentoNome')

    class FuncionarioSerializer(serializers.ModelSerializer):
            class Meta:
                model = Funcionarios
                fields = ('funcionarioId', 'funcionarioNome','departamento' ,'dataAdesao', 'arquivoFoto')
                
----------------------------------------------------------------------------------------------------------------------------------------------------------                

# Escrever os metodos da API

    from django.shortcuts import render

Decorators permite outros dominios acessar os metodos da API

    from django.views.decorators.csrf import csrf_exempt


JSON parser transforma os dados em 'data models' e o JSON response retorna a resposta

    from rest_framework.parsers import JSONParser
    from django.http.response import JsonResponse

Importar os modulos criados e serializer

    from CRUD_API_Django_MongoDB.FuncionarioApp.models import Departamentos, Funcionarios
    from CRUD_API_Django_MongoDB.FuncionarioApp.serializers import DepartamentoSerializer, FuncionarioSerializer   

Criar os metodos da API para departamentos na views.py

O metodo vai usar um id opcional que usaremos no metodo DELETE

    # Create your views here.

    @csrf_exempt
    def departamentoApi(request, id=0):

        # Retorna		
        if request.method== 'GET':
            departamentos = Departamentos.object.all()
            departamentos_serializer= DepartamentoSerializer(departamentos,many=True) # Os serializers estao sendo usados para converter em formato JSON
            return JsonResponse(departamentos_serializer.data,safe=False) # parametro 'safe= False' informa o JSON que é um formato válido

        # Insere novos dados na tabela departamentos	
        elif request.method=='POST':
            departamento_dados= JSONParser().parse(request) # Passar o request
            departamentos_serializer= DepartamentoSerializer(data=departamento_dados) # Converter em model
            if departamentos_serializer.is_valid(): # Verifica a validade
                departamentos_serializer.save() # Salva no banco de dados
                return JsonResponse("Adicionado com sucesso!",safe= False) # Retorna mensagem de sucesso
            return JsonResponse("Algo deu errado ao adicionar o arquivo!", safe=False) # Retorna mensagem de falha

        # Atualiza um dado já existente na tabela
        elif request.method == 'PUT':
            departamento_dados = JSONParser().parse(request)
            departamento= Departamentos.objects.get(departamentoId= departamento_dados['departamentoId']) # Capturar o registro existente pelo Id
            departamentos_serializer=DepartamentoSerializer(departamento,data= departamento_dados) # Mapear com novos valores usando a classe serializers
            if departamentos_serializer.is_valid():
                departamentos_serializer.save()
                return JsonResponse("Atualizado com sucesso!",safe= False)
            return JsonResponse("Falha ao atualizar o arquivo!", safe=False)

        # Metodo para deletar o registro
        elif request.method == 'DELETE':
            departamento=Departamentos.objects.get(departamentoId=id) # Usaremos o Id para achar o registro
            departamento.delete() # Deleta o registro da url
            return JsonResponse("Arquivo deletado com sucesso!", safe=False) 
            
----------------------------------------------------------------------------------------------------------------------------------------------------------

# Criar arquivo urls.py que irao adicionar routes para especificar as urls aos metodos da API 

    from django.urls import re_path
    from CRUD_API_Django_MongoDB.FuncionarioApp import views

    urlpatterns = [
        re_path(r'^departamento$',views.departamentoApi),
        re_path(r'^departamento/([0-9]+)$', views.departamentoApi) # O metodo DELETE vai receber o id na url
    ]

----------------------------------------------------------------------------------------------------------------------------------------------------------

# Incluir as urls no arquivo main urls.py

    from django.contrib import admin
    from django.urls import re_path,include


    urlpatterns = [
        re_path('admin/', admin.site.urls),
        re_path(r'^',include('FuncionarioApp.urls'))
    ]

----------------------------------------------------------------------------------------------------------------------------------------------------------

# Criar metodos da API para funcionarios na views.py
    @csrf_exempt
    def departamentoApi(request, id=0):
        if request.method== 'GET':
            funcionarios = Funcionarios.objects.all()
            funcionarios_serializer= FuncionarioSerializer(funcionarios,many=True)
            return JsonResponse(funcionarios_serializer.data,safe=False)
        elif request.method=='POST':
            funcionario_dados= JSONParser().parse(request)
            funcionarios_serializer= FuncionarioSerializer(data=funcionario_dados)
            if funcionarios_serializer.is_valid():
                funcionarios_serializer.save()
                return JsonResponse("Adicionado com sucesso!",safe= False)
            return JsonResponse("Algo deu errado ao adicionar o arquivo!", safe=False)
        elif request.method == 'PUT':
            funcionario_dados = JSONParser().parse(request)
            funcionario= Funcionarios.objects.get(funcionarioId= funcionario_dados['funcionarioId'])
            funcionarios_serializer= FuncionarioSerializer(funcionario,data= funcionario_dados)
            if funcionarios_serializer.is_valid():
                funcionarios_serializer.save()
                return JsonResponse("Atualizado com sucesso!",safe= False)
            return JsonResponse("Falha ao atualizar o arquivo!", safe=False)
        elif request.method == 'DELETE':
            funcionario= Funcionarios.objects.get(funcionarioId=id)
            funcionario.delete()
            return JsonResponse("Arquivo deletado com sucesso!", safe=False)
            
----------------------------------------------------------------------------------------------------------------------------------------------------------       
# Criar pasta 'Fotos' no projeto para armazenar as fotos do upload

Passar instrucoes no settings.py

    import os

    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
    MEDIA_URL= '/Fotos/'
    MEDIA_ROOT= os.path.join(BASE_DIR, "Fotos")

Adicionar routes para especificar as urls aos metodos dos funcionarios na API na urls.py

    url(r'^funcionario$',views.funcionarioApi),
    url(r'^funcionario/([0-9]+)$', views.funcionarioApi)
    
----------------------------------------------------------------------------------------------------------------------------------------------------------    
importar o 'default storage'

    from django.core.files.storage import default_storage

Adicionar metodo na views.py para salvar os arquivos

    @csrf_exempt
    def salvarArquivo(request):
        file= request.FILES['file']
        file_name= default_storage.save(file.name, file)
        return JsonResponse(file_name, safe=False)
        
----------------------------------------------------------------------------------------------------------------------------------------------------------        
Adicionar uma rota para o novo metodo no urls.py

    from django.conf.urls.static import static
    from django.conf import settings

    urlpatterns = [
        url(r'^departamento$',views.departamentoApi),
        url(r'^departamento/([0-9]+)$', views.departamentoApi),

        url(r'^funcionario$',views.funcionarioApi),
        url(r'^funcionario/([0-9]+)$', views.funcionarioApi),

        url(r'^funcionario/salvararquivo', views.salvarArquivo)
    ]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
    
----------------------------------------------------------------------------------------------------------------------------------------------------------

# Fazer Migrações 

Comando para fazer arquivos de migração para os models

    python manage.py makemigrations FuncionarioApp

Pode ocorrer problemas de compatibilidade com a versão mais recente do pymongo em caso de erro executar antes 

    pip install pymongo==3.12.3 
 
(Regredir para uma versão mais antiga)
 
 
Fazer o Push das mudanças para o banco de dados

    python manage.py migrate FuncionarioApp
    
    
Recomendo fazer este passo por último para que as migrações sejam feitas corretamente (mas caso tenha tido algum problema exclua o banco de dados e exclua a pasta 'migrations' e execute os comandos para refazer as migrações novamente)    

----------------------------------------------------------------------------------------------------------------------------------------------------------

# Iteragir com a API(exemplos):

Método POST departamentos:

    http://127.0.0.1:8000/departamento

    {
        "departamentoNome": "T.I"
    }

--------------------------------------------------------------------------------------------------------------

Método GET departamentos:

    http://127.0.0.1:8000/departamento

--------------------------------------------------------------------------------------------------------------

Método PUT departamentos:

    {
        "departamentoId": 1,
        "departamentoNome": "Administracao"
    }

--------------------------------------------------------------------------------------------------------------

Método DELETE departamentos:

    http://127.0.0.1:8000/departamento/<id>

    Exemplo -> http://127.0.0.1:8000/departamento/1

--------------------------------------------------------------------------------------------------------------

Método POST funcionario:

    http://127.0.0.1:8000/funcionario

    {
        "funcionarioNome": "Gustavo",
        "departamento": "T.I",
        "dataAdesao": "2022-06-04",
        "arquivoFoto": "logo.png"
    }

--------------------------------------------------------------------------------------------------------------

Método GET funcionario:

    http://127.0.0.1:8000/funcionario

--------------------------------------------------------------------------------------------------------------

Método PUT funcionario:

    http://127.0.0.1:8000/funcionario

    {
        "funcionarioId": 1,
        "funcionarioNome": "Gustavo Batista",
        "departamento": "Administracao",
        "dataAdesao": "2020-08-02",
        "arquivoFoto": "logo2.png"
    }

--------------------------------------------------------------------------------------------------------------

Método DELETE funcionario:

    http://127.0.0.1:8000/funcionario/<id>

    Exemplo -> http://127.0.0.1:8000/funcionario/1

--------------------------------------------------------------------------------------------------------------

Método POST Arquivo:

    Exemplo:

    http://127.0.0.1:8000/funcionario/salvararquivo

    KEY: file
    Value: GustavoLogoS.png

(O arquivo irá para a pasta 'Fotos' do projeto)

-----------------------------------------------------------------------------------------------------------------------------

Se precisar entrar em contato comigo pode encontrar pelos meios de comunicação abaixo:

	e-Mail: gustavo.dev97@gmail.com
	GitHub: github.com/Gustav-dev97
	

Muito Obrigado! :)

