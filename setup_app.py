from sqlalchemy.orm import Session
from views import UserAdmin, RoleAdmin, PostAdmin
from flask_admin.menu import MenuLink

from models import User, Role, Post


def initialization_view(session: Session, admin):
    admin.add_view(UserAdmin(User, session))
    admin.add_view(RoleAdmin(Role, session))
    admin.add_view(PostAdmin(Post, session))
    admin.add_link(MenuLink(name='Logout', url='/logout'))
