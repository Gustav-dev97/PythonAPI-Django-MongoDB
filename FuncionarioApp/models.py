from django.db import models

# Create your models here.

class Departamentos(models.Model):
    departamentoId = models.AutoField(primary_key=True)
    departamentoNome = models.CharField(max_length=500)

class Funcionarios(models.Model):
    funcionarioId = models.AutoField(primary_key=True)
    funcionarioNome = models.CharField(max_length=500)
    departamento = models.CharField(max_length=500)
    dataAdesao = models.DateField()
    arquivoFoto = models.CharField(max_length=500)