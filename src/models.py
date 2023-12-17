import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'

    ID = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    followers_from = relationship("Follower", back_populates="user_from")
    followers_to = relationship("Follower", back_populates="user_to")
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="author")

class Follower(Base):
    __tablename__ = 'Follower'

    user_from_id = Column(Integer, ForeignKey('User.ID'), nullable=False, primary_key=True)
    user_to_id = Column(Integer, ForeignKey('User.ID'), nullable=False, primary_key=True)
    user_from = relationship("User", foreign_keys=[user_from_id], back_populates="followers_to")
    user_to = relationship("User", foreign_keys=[user_to_id], back_populates="followers_from")

class Media(Base):
    __tablename__ = 'Media'

    ID = Column(Integer, primary_key=True)
    type = Column(Enum, nullable=False)
    url = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('Post.ID'), nullable=False)
    post = relationship("Post", back_populates="media")

class Post(Base):
    __tablename__ = 'Post'

    ID = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.ID'), nullable=False)
    user = relationship("User", back_populates="posts")
    media = relationship("Media", back_populates="post")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = 'Comment'

    ID = Column(Integer, primary_key=True)
    comment_text = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('User.ID'), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.ID'), nullable=False)
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
