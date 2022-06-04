from rest_framework import serializers
from FuncionarioApp.models import Departamentos, Funcionarios


class DepartamentoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Departamentos
            fields = ('departamentoId', 'departamentoNome')

class FuncionarioSerializer(serializers.ModelSerializer):
        class Meta:
            model = Funcionarios
            fields = ('funcionarioId', 'funcionarioNome','departamento' ,'dataAdesao', 'arquivoFoto')