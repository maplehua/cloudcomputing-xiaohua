from flask.ext.wtf import Form, TextField, IntegerField, widgets
from flask.ext.admin import Admin, AdminIndexView, BaseView
from flask.ext.admin.base import MenuLink
from flask.ext.admin.contrib.mongoengine import ModelView, filters
from flask.ext.login import current_user

class AuthenticatedMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated()

class NotAuthenticatedMenuLink(MenuLink):
    def is_accessible(self):
        return not current_user.is_authenticated()

class AdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated()

class UserView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated()

class PaperMetaView(ModelView):
    column_list = ('title', 'booktitle', 'journal', 'authors')
    column_filters = ('year','booktitle', 'journal', 'title')

    def is_accessible(self):
        return current_user.is_authenticated()

class ScholarMetaView(ModelView):
    column_list = ('ban', 'name', 'native_name', 'affiliation', 'homepage', 'email')
    column_filters = ('ban', 'name_low_case', 'affiliation', 'homepage', 'email')

    def is_accessible(self):
        return current_user.is_authenticated()

def config_admin():
    from .models import User, PaperMeta, ScholarMeta

    admin = Admin(name='Academi', index_view = AdminView())

    admin.add_view(UserView(User))
    admin.add_view(PaperMetaView(PaperMeta))
    admin.add_view(ScholarMetaView(ScholarMeta))

    admin.add_link(MenuLink(name = 'Go Back', url = '/'))
    admin.add_link(MenuLink(name = 'Logout', url = '/logout'))
    return admin
