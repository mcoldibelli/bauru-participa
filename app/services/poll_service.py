from typing import Dict, List, Optional

from sqlalchemy import func
from database.models import Poll, PollOption, User, UserVote
from database.database import db

class PollService:
    @staticmethod
    def get_poll(poll_id:int) -> Poll:
        poll = db.session.query(Poll).filter(Poll.id == poll_id).first()
        if not poll:
            raise Exception(f"Poll with ID {poll_id} not found")
        return poll
    
    @staticmethod
    def get_user(user_id: int) -> User:
        user = db.session.query(User).filter(User.id == user_id).first()
        if not user:
            raise Exception(f"User with ID {user_id} not found")
        return user

    @classmethod
    def create_poll(title: str, description: str) -> Poll:
        try:
            new_poll = Poll(
                title=title.strip(),
                description=description.strip()
            )
            db.session.add(new_poll)
            db.session.commit()
            return new_poll
        
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to create poll: {str(e)}")
    
    @classmethod
    def list_all_polls() -> List[Poll]:
        try:
            return db.session.query(Poll).all()
        except Exception as e:
            raise Exception("Failed to retrieve polls")

    @classmethod
    def list_poll_by_id(cls, poll_id: int) -> Optional[Poll]:
        try:
            return cls.get_poll()
        except Exception as e:
            raise Exception(f"Failed to retrieve poll {poll_id}")

    @classmethod 
    def delete_poll(cls, poll_id: int) -> bool:
        try:
            poll = cls.get_poll(poll_id)
            db.session.delete(poll)
            db.session.commit()
            return True
        
        except Exception as e:
            raise Exception(f"Failed to delete poll {poll_id}")
    
    @classmethod
    def create_poll_option(cls, poll_id, description):
        try:
            cls.get_poll(poll_id)
            new_option = PollOption(
                poll_id=poll_id,
                description=description
            )
            db.session.add(new_option)
            db.session.commit()
            return new_option

        except Exception as e:
            raise Exception(f"Failed to create poll option: {str(e)}")

    @classmethod 
    def delete_poll_option(cls, poll_id: int, option_id: int) -> bool:
        try:
            cls.get_poll(poll_id)

            result = db.session.query(PollOption).filter(
                PollOption.poll_id == poll_id,
                PollOption.option_id == option_id
            ).delete(synchronize_session=False)

        
            db.session.commit()
            return result > 0
        
        except Exception as e:
            raise e

    @classmethod
    def vote_on_poll(cls, user_id:int, poll_id: int, option_id: int) -> UserVote:
        try:
            cls.get_poll(poll_id)
            cls.get_user(user_id)

            option = db.session.query(PollOption).filter(
                PollOption.option_id == option_id,
                PollOption.poll_id == poll_id
            ).first()
            if not option:
                raise Exception(f"Option with ID {option_id} not found in poll {poll_id}")

            existing_vote = db.session.query(UserVote).join(PollOption).filter(
                UserVote.user_id == user_id,
                PollOption.poll_id == poll_id
            ).first()
            if existing_vote:
                raise Exception(f"User {user_id} has already voted on poll {poll_id}")

            new_vote = UserVote(
                user_id=user_id,
                poll_option_id=option_id
            )
            db.session.add(new_vote)
            db.session.commit()
            return new_vote
        
        except Exception as e:
            raise e

    @classmethod  
    def get_poll_results(cls, poll_id: int) -> Dict:
        try:
            cls.get_poll(poll_id)

            results = db.session.query(
                PollOption.option_id, PollOption.description, func.count(UserVote.vote_id).label('votes')
            ).outerjoin(
                UserVote, UserVote.poll_option_id == PollOption.option_id
            ).filter(
                PollOption.poll_id == poll_id
            ).group_by(
                PollOption.option_id, PollOption.description
            ).all()

            total_votes = sum(result.votes for result in results)

            options_results = [{
                "option_id": result.option_id,
                "description": result.description,
                "votes": result.votes,
                "percentage": f"{round((result.votes / total_votes * 100), 2)} %" if total_votes > 0 else 0
            } for result in results]

            return {
                "total votes": total_votes,
                "options": options_results
            }

        except Exception as e:
            raise Exception(f"Failed to get poll results: {str(e)}")