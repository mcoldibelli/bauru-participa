from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from database import Base, relationship, current_timestamp

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Poll(Base):
    __tablename__ = 'polls'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)

class PollOption(Base):
    __tablename__ = 'poll_options'
    option_id = Column(Integer, primary_key=True)
    poll_id = Column(Integer, ForeignKey("polls.poll_id") ,nullable=False)
    description = Column(String(255), nullable=False)
    poll = relationship("Poll", backref="options", cascade='all,delete')

class UserVote(Base):
    __tablename__ = 'users_vote'
    vote_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    poll_option_id = Column(Integer, ForeignKey("poll_options.option_id"), nullable=False)
    vote_at = Column(DateTime, default=current_timestamp())

    user = relationship("User", backref="votes", cascade='all,delete')
    option = relationship("PollOption", backref="votes", cascade='all,delete')