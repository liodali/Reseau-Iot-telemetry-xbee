from django.contrib import admin

# Register your models here.

from django.contrib import admin
from myApp.models import Profil, Utilisateur


class ProfilAdmin(admin.ModelAdmin):
    list_display   = ('cin', 'get_username', 'get_firstname', 'get_lastname', 'get_email', 'avatar')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Nom d\'utilisateur'

    def get_firstname(self, obj):
        return obj.user.first_name
    get_firstname.short_description = 'Nom'

    def get_lastname(self, obj):
        return obj.user.last_name
    get_lastname.short_description = 'Prenom'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

class UtilisateurAdmin(admin.ModelAdmin):
    list_display   = ('get_cin', 'get_firstname', 'get_lastname', 'get_email', 'get_avatar')

    def get_cin(self, obj):
        return obj.personne.cin
    get_cin.short_description = 'Cin'

    def get_avatar(self, obj):
        return obj.personne.avatar
    get_avatar.short_description = 'Avatar'

    def get_firstname(self, obj):
        return obj.personne.user.first_name
    get_firstname.short_description = 'Nom'

    def get_lastname(self, obj):
        return obj.personne.user.last_name
    get_lastname.short_description = 'Prenom'

    def get_email(self, obj):
        return obj.personne.user.email
    get_email.short_description = 'Email'


admin.site.register(Profil, ProfilAdmin)
admin.site.register(Utilisateur, UtilisateurAdmin)
