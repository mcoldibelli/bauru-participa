from database.database import create_app, db
from database.models import User, Poll, PollOption, UserVote
from app.routes import register_routes

app = create_app()
app.name = 'bauru_participa'

def init_db():
    try:
        with app.app_context():
            db.create_all()
            print("Database initialized with success")
    except Exception as e:
        print(f"Error initializing database: ${str(e)}")
        raise

if __name__ == "__main__":
    init_db()
    register_routes(app)
    app.run()
