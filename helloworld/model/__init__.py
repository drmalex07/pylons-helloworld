"""The application's model objects"""
from sqlalchemy import func

from helloworld.model.meta import Session, Base

from helloworld.model.vote import Vote

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)
