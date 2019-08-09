from django.contrib import admin
from . import models

admin.site.register(models.Questionario)
admin.site.register(models.Questao)
admin.site.register(models.PossivelResposta)
admin.site.register(models.RespostaQuestionario)
