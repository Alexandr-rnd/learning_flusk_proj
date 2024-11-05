from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectField
from init_app import db
from models import User, Role
from wtforms import SelectField


class CustomQuerySelectField(QuerySelectField):
    def populate_obj(self, obj: User, name: str) -> None:
        obj.role_id = self.data.id

    def iter_choices(self):
        if self.allow_blank:
            yield (u'__None', self.blank_text, self.data is None, {})

        for pk, obj in self._get_object_list():
            yield (pk, self.get_label(obj), pk == str(self.data), {})


class UserAdmin(ModelView):
    column_list = ('id', 'username', 'email', 'role_id')
    column_labels = {'id': 'ID', 'username': 'Username', 'email': 'Email Address', 'role_id': 'Role'}
    column_filters = ('id', 'username', 'email', 'role_id')

    form_columns = ('username', 'email', 'password', 'role_id')

    form_extra_fields = {
        'role_id': CustomQuerySelectField(
            label='Роль',
            query_factory=lambda: db.session.query(Role).all(),
        ),
    }


class RoleAdmin(ModelView):
    column_list = ('id', 'name',)
    column_labels = {'id': 'ID', 'name': 'Role Name'}
    column_filters = ('id', 'name',)
    form_columns = ('name',)


class PostAdmin(ModelView):
    column_list = ('id', 'title', 'content', 'author')
    column_labels = {'id': 'ID', 'title': 'Post Title', 'content': 'Content'}
    column_filters = ('id', 'title')

    form_columns = ('title', 'content', 'author_id')

    form_extra_fields = {
        'author_id': CustomQuerySelectField(
            label='Автор',
            query_factory=lambda: db.session.query(User).all(),
        ),
    }
