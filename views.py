from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectField
from init_app import db, app
from models import User, Role, Post

from flask import render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


class UserQuerySelectField(QuerySelectField):
    def populate_obj(self, obj: User, name: str) -> None:
        obj.role_id = self.data.id

    def iter_choices(self):
        if self.allow_blank:
            yield (u'__None', self.blank_text, self.data is None, {})

        for pk, obj in self._get_object_list():
            yield (pk, self.get_label(obj), pk == str(self.data), {})


class PostQuerySelectField(QuerySelectField):
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
        'author_id': PostQuerySelectField(
            label='Автор',
            query_factory=lambda: db.session.query(User).all(),
        ),
    }


class RoleAdmin(ModelView):
    column_list = ('id', 'name',)
    column_labels = {'id': 'ID', 'name': 'Role Name'}
    column_filters = ('id', 'name',)
    form_columns = ('name',)


login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = None
        try:
            user = User.query.filter_by(username=request.form['username']).one()
        except Exception as e:
            print(f"Exception getting user: {e}")
        try:
            if (user and check_password_hash(user.password, request.form['password']) or user.password ==
                    request.form['password']):
                if user.role is None:
                    pass
                elif user.role.name == 'Admin':
                    login_user(user)
                    return redirect(url_for('admin.index'))
                flash('You are not real ADMIN!', 'error')
                return render_template('login.html')
            else:
                flash('Invalid email or password. Please try again.', 'error')
                return render_template('login.html')
        except Exception as e:
            print(f"Exception login: {e}")
    else:
        return render_template('login.html')


@app.route('/')
@login_required
def base_page():
    logout_user()
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
