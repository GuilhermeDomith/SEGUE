from django.contrib import admin
from .models import Questionario, Questao, PossivelResposta

admin.site.register(Questionario)
admin.site.register(Questao)
admin.site.register(PossivelResposta)
