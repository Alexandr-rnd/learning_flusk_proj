from setup_app import initialization_view
from logger import setup_logging
from init_app import admin, app, db

logger = setup_logging(log_file_path='./logs/app.log', logger_name='app_logs')

if __name__ == '__main__':
    initialization_view(session=db.session, admin=admin)
    with app.app_context():
        db.create_all()
    app.run()
