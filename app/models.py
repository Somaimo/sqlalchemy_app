# app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base
from app import db
from datetime import datetime
from flask_login import UserMixin
from app import login
from hashlib import md5


class PlayerModel(db.Model):
    """Data model for players."""
    __tablename__ = "sqlalchemy_app_players"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    team_id = Column(
        Integer,
        ForeignKey('sqlalchemy_app_teams.id'),
        nullable=True
    )
    name = Column(
        String(100),
        nullable=False
    )
    position = Column(
        String(100),
        nullable=False
    )

    # Relationships
    team = relationship("TeamModel", backref="players")

    def __repr__(self):
        return '<Person model {}>'.format(self.id)


class TeamModel(db.Model):
    """Data model for teams."""
    __tablename__ = "sqlalchemy_app_teams"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    name = Column(
        String(100),
        nullable=False
    )
    city_id = Column(
        Integer,
        ForeignKey('sqlalchemy_app_city.id'),
        nullable=False
    )

    create_user_id = Column(
        Integer,
        ForeignKey('sqlalchemy_app_user.id'),
        nullable=False
    )

    create_timestamp = Column(
        DateTime,
        index=True,
        default=datetime.utcnow
    )

    # Relationship
    city = relationship("CityModel", backref="team")

    def __repr__(self):
        return '<Team model {}>'.format(self.id)


class CityModel(db.Model):
    """Data Model for cities."""
    __tablename__ = "sqlalchemy_app_city"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    name = Column(
        String(100),
        nullable=False
    )


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('sqlalchemy_app_user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('sqlalchemy_app_teams.id'))
)

class Game(db.Model):
    """Data model for games."""
    __tablename__ = "sqlalchemy_app_games"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    hometeam_id = Column(
        Integer,
        ForeignKey('sqlalchemy_app_teams.id'),
        nullable=False
    )

    visitorteam_id = Column(
        Integer,
        ForeignKey('sqlalchemy_app_teams.id'),
        nullable=False
    )

    score = Column(
        String(24),
        nullable=False
    )

    playDate = Column(
        Date,
        index=True,
        nullable=False
    )

    # Relationship
    homeTeam = relationship("TeamModel", backref="homeTeam", foreign_keys=[hometeam_id])
    visitorTeam = relationship("TeamModel", backref="visitorTeam", foreign_keys=[visitorteam_id])

    def __repr__(self):
        return '<Game model {}>'.format(self.id)

class User(UserMixin, db.Model):
    """Data Model for users."""
    __tablename__ = "sqlalchemy_app_user"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))
    teams = relationship('TeamModel', backref='creator', lazy='dynamic')
    about_me = Column(String(140))
    last_seen = Column(DateTime,default=datetime.utcnow)
    followed = db.relationship(
        'TeamModel', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == TeamModel.id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
    
    def follow(self, team):
        if not self.is_following(team):
            self.followed.append(team)
    
    def unfollow(self, team):
        if self.is_following(team):
            self.followed.remove(team)
    
    def is_following(self, team):
        return self.followed.filter(
            followers.c.followed_id == team.id).count() > 0


@login.user_loader
def load_user(id):
    return User.query.get(int(id))