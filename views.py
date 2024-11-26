from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectField
from init_app import db, app
from models import User, Role, Post

from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from init_app import login_manager
from flask.views import MethodView
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserQuerySelectField(QuerySelectField):
    def populate_obj(self, obj: User, name: str) -> None:
        obj.role_id = self.data.id

    def iter_choices(self):
        if self.allow_blank:
            yield (u'__None', self.blank_text, self.data is None, {})

        for pk, obj in self._get_object_list():
            yield (pk, self.get_label(obj), pk == str(self.data), {})


class AutorQuerySelectField(QuerySelectField):
    def populate_obj(self, obj: Post, name: str) -> None:
        obj.author_id = self.data.id

    def iter_choices(self):
        if self.allow_blank:
            yield (u'__None', self.blank_text, self.data is None, {})

        for pk, obj in self._get_object_list():
            yield (pk, self.get_label(obj), pk == str(self.data), {})


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.name == 'Admin'


class UserAdmin(ModelView):
    column_list = ('id', 'username', 'email', 'role')
    column_labels = {'id': 'ID', 'username': 'Username', 'email': 'Email Address', 'role': 'Role'}
    column_filters = ('id', 'username', 'email', 'role')

    form_columns = ('username', 'email', 'password', 'role_id')

    form_extra_fields = {
        'role_id': UserQuerySelectField(
            label='Роль',
            query_factory=lambda: db.session.query(Role).all(),
        ),
    }


class PostAdmin(ModelView):
    column_list = ('id', 'title', 'content', 'author')
    column_labels = {'id': 'ID', 'title': 'Post Title', 'content': 'Content'}
    column_filters = ('id', 'title')

    form_columns = ('title', 'content', 'author_id')

    form_extra_fields = {
        'author_id': AutorQuerySelectField(
            label='Автор',
            query_factory=lambda: db.session.query(User).all(),
        ),
    }


class RoleAdmin(ModelView):
    column_list = ('id', 'name',)
    column_labels = {'id': 'ID', 'name': 'Role Name'}
    column_filters = ('id', 'name',)
    form_columns = ('name',)


class RegisterView(MethodView):

    def get(self):
        return render_template('register.html')

    def post(self):
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))


register_view = RegisterView.as_view('register')
app.add_url_rule('/register', view_func=register_view, methods=['GET', 'POST'])


class LoginView(MethodView):
    def get(self):
        return render_template('login.html')

    def post(self):
        try:
            user = self.get_user(request.form['username'])
            if self.validate_user(user, request.form['password']):
                return self.handle_successful_auth(user)
            else:
                flash('Invalid email or password. Please try again.', 'error')
                return render_template('login.html')
        except Exception as e:
            print(f"Exception during login: {e}")
            return render_template('login.html')

    def get_user(self, username):
        try:
            return User.query.filter_by(username=username).one()
        except Exception as e:
            print(f"Exception getting user: {e}")
            return None

    def validate_user(self, user, password):
        if not user:
            return False
        return (check_password_hash(user.password, password) or
                user.password == password)

    def handle_successful_auth(self, user):
        if user.role is None:
            flash("You are havn't any role", 'error')
            return render_template('login.html')
        elif user.role.name == 'Admin':
            login_user(user)
            return redirect(url_for('admin.index'))
        flash('You are not real ADMIN!', 'error')
        return render_template('login.html')



app.add_url_rule('/login', view_func=login_view, methods=['GET', 'POST'])


@app.route('/')
@login_required
def base_page():
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
