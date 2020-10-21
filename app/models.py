from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app import db


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
        nullable=False
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
    team = relationship("TeamModel", backref="player")

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