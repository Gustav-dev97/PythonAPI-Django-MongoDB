from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from FuncionarioApp.models import Departamentos, Funcionarios
from FuncionarioApp.serializers import DepartamentoSerializer, FuncionarioSerializer

from django.core.files.storage import default_storage

# Create your views here.

@csrf_exempt
def departamentoApi(request, id=0):
    if request.method== 'GET':
        departamentos = Departamentos.objects.all()
        departamentos_serializer= DepartamentoSerializer(departamentos,many=True)
        return JsonResponse(departamentos_serializer.data,safe=False)
    elif request.method=='POST':
        departamento_dados= JSONParser().parse(request)
        departamentos_serializer= DepartamentoSerializer(data=departamento_dados)
        if departamentos_serializer.is_valid():
            departamentos_serializer.save()
            return JsonResponse("Adicionado com sucesso!",safe= False)
        return JsonResponse("Algo deu errado ao adicionar o arquivo!", safe=False)
    elif request.method == 'PUT':
        departamento_dados = JSONParser().parse(request)
        departamento = Departamentos.objects.get(departamentoId= departamento_dados['departamentoId'])
        departamentos_serializer = DepartamentoSerializer(departamento,data= departamento_dados)
        if departamentos_serializer.is_valid():
            departamentos_serializer.save()
            return JsonResponse("Atualizado com sucesso!",safe= False)
        return JsonResponse("Falha ao atualizar o arquivo!", safe=False)
    elif request.method == 'DELETE':
        departamento=Departamentos.objects.get(departamentoId=id)
        departamento.delete()
        return JsonResponse("Arquivo deletado com sucesso!", safe=False)

@csrf_exempt
def funcionarioApi(request, id=0):
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

@csrf_exempt
def salvarArquivo(request):
    file= request.FILES['file']
    file_name= default_storage.save(file.name, file)
    return JsonResponse(file_name, safe=False)

