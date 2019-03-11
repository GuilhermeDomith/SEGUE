from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, TipoUsuario

class UserAdmin(BaseUserAdmin):
    # Forms para alterar e adicionar usuário
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # Especifíca os atributos as serem exibidos na lista de usuários.
    list_display = ('email', 'tipo_usuario')
    # Especifíca os filtros a serem exibidos.
    list_filter = ('tipo_usuario',)
    # Especifíca a ordem e os campos a serem exibidos na tela de add e change usuário.
    fieldsets = (
        (None, {'fields': ('username', 'tipo_usuario', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_trusty')}),
    )

    # Os campos abaixo deverão ser fornecidos no primeiro instante ao 
    # clicar em criar novo usuário, no app Admin.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('tipo_usuario', 'email', 'password')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('tipo_usuario', 'email',)
    filter_horizontal = ()




admin.site.register(User, UserAdmin)
#admin.site.register(TipoUsuario)
admin.site.unregister(Group)
