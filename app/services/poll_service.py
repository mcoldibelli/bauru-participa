from typing import List, Optional
from database.models import Poll, PollOption
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
    
def create_poll_option(poll_id, description):
    try:
        poll = db.session.query(Poll).filter(Poll.id == poll_id).first()

        if not poll:
            raise Exception(f"Poll with ID {poll_id} not found")
        
        new_option = PollOption(poll_id=poll_id, description=description)
        db.session.add(new_option)
        db.session.commit()

        return new_option

    except Exception as e:
        raise Exception(f"Failed to create poll option: {str(e)}")

def list_poll_options(poll_id: int) -> List[PollOption]:
    try:
        poll = db.session.query(Poll).filter(Poll.id == poll_id).first()

        if not poll:
            raise Exception(f"Poll with ID {poll_id} not found")

        return poll.options

    except Exception as e:
        raise Exception(f"Failed to list poll options: {str(e)}")
    
def delete_poll_option(poll_id: int, option_id: int) -> bool:
    try:
        poll = db.session.query(Poll).filter(Poll.id == poll_id).first()

        if not poll:
            raise Exception(f"Poll with ID {poll_id} not found")

        result = db.session.query(PollOption).filter(
            PollOption.poll_id == poll_id,
            PollOption.option_id == option_id
        ).delete(synchronize_session=False)

       
        db.session.commit()
        return result > 0
    
    except Exception as e:
        raise e