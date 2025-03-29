from database.models import Poll
from database.database import db

def create_poll(title: str, description: str) -> Poll:
    try:
        new_poll = Poll(title=title.strip(), description=description.strip())
        
        db.session.add(new_poll)
        db.session.commit()
        
        return new_poll
    except Exception as e:
        db.session.rollback()
        raise e