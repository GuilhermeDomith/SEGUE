import re
from django.db import models
from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, tipo_usuario_id, is_staff, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError(_('Users must have email address'))
        if not password:
            raise ValueError(_('Users must have password'))

        email = self.normalize_email(email)
        user = self.model(
            tipo_usuario_id= tipo_usuario_id,
            username=username,  email=email,
            is_staff=is_staff,  is_active=True,
            last_login=now,     date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, tipo_usuario_id=None,  **extra_fields):
        return self._create_user(username, email, password, tipo_usuario_id, False, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        # Verificar se a fixtures foram executadas, ou seja, se a tebela TipoUsuario
        # do banco foi populada com os tipos de usuários possíveis.
        tipo_usuario = TipoUsuario.objects.get(tipo='admin')
        return self._create_user(username, email, password, tipo_usuario.pk, True, **extra_fields)



class TipoUsuario(models.Model):
    tipo = models.CharField('tipo', max_length=30, unique=True)

    class Meta:
        verbose_name = _('Tipo de usuário')
        verbose_name_plural = _('Tipos de usuário')

    def __repr__(self):
        return '%d - %s'%(self.pk, self.tipo)
    
    def __str__(self):
        return '%d - %s'%(self.pk, self.tipo)



class User(AbstractBaseUser):
    
    username = models.CharField(_('username'), max_length=50)
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    is_trusty = models.BooleanField('Email Verificado', default=False, help_text=_('Indica que o email do usuário foi verificado.'))

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def save(self, *args, **kwargs):
        self.is_staff = ('admin' in self.tipo_usuario.tipo)
        super().save(*args, **kwargs)

    def is_tipo(self, tipo_usuario=None):
        return tipo_usuario.lower() in self.tipo_usuario.tipo.lower()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def has_perm(self, perm, obj=None):
        '''Não será usado, mas precisa ser implementado'''
        return True

    def has_module_perms(self, app_label):
        '''Não será usado, mas precisa ser implementado'''
        return True


