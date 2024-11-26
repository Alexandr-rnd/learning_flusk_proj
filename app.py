from incialization_module import iniciation_view
from init_app import db, admin, app
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    iniciation_view(session=db.session, admin=admin)
    with app.app_context():
        db.create_all()
    app.run()
