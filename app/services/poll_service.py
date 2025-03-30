from typing import List, Optional
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

def list_poll_by_id(poll_id: int) -> Optional[Poll]:
    try:
        return db.session.query(Poll).filter(Poll.id == poll_id).first()
    except Exception as e:
        raise e
    
def delete_poll(poll_id: int) -> bool:
    try:
        poll = db.session.query(Poll).filter(Poll.id == poll_id).first()

        if poll:
            db.session.delete(poll)
            db.session.commit()
            return True
        return False
    
    except Exception as e:
        raise e