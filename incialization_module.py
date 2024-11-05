from sqlalchemy.orm import Session
from flask_admin.contrib.sqla import ModelView
from models import User, Role, Post
from views import UserAdmin, RoleAdmin, PostAdmin


def iniciation_view(session: Session, admin):
    admin.add_view(UserAdmin(User, session))
    admin.add_view(RoleAdmin(Role, session))
    admin.add_view(PostAdmin(Post, session))
    return None
