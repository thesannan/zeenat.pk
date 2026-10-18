from app import create_app, db
from seed_data import seed_database

app = create_app()

with app.app_context():
    db.create_all()
    seed_database(app)

if __name__ == '__main__':
    app.run()
