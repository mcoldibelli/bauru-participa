from typing import List
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
    
def list_all_polls() -> List[Poll]:
    try:
        return db.session.query(Poll).all()
    except Exception as e:
        raise e