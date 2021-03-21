# app/routes.py
import os
from app import app, db
from flask import render_template, flash, redirect, url_for
from flask import request
from werkzeug.urls import url_parse
from app.forms import LoginForm, EditProfileForm, EmptyForm, NewGameForm
#from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import environ
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, TeamModel, Game
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    teams = user.teams
    return render_template('user.html', user=user, teams=teams)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/follow/<teamid>', methods=['POST'])
@login_required
def follow(teamid):
    form = EmptyForm()
    if form.validate_on_submit():
        team = TeamModel.query.filter_by(id=teamid).first()
        if team is None:
            flash('Team with ID {} not found.'.format(teamid))
            return redirect(url_for('teams'))
        current_user.follow(team)
        db.session.commit()
        flash('You are now following {}!'.format(team.name))
        return redirect(url_for('teams'))
    else:
        return redirect(url_for('teams'))

@app.route('/unfollow/<teamid>', methods=['POST'])
@login_required
def unfollow(teamid):
    form = EmptyForm()
    if form.validate_on_submit():
        team = TeamModel.query.filter_by(id=teamid).first()
        if team is None:
            flash('Team with ID {} not found.'.format(teamid))
            return redirect(url_for('index'))
        current_user.unfollow(team)
        db.session.commit()
        flash('You are not following {} anymore.'.format(team.name))
        return redirect(url_for('teams'))
    else:
        return redirect(url_for('teams'))

# index page
@app.route('/')
@app.route('/index')
@login_required
def index():
    games = Game.query.order_by(Game.playDate)
    return render_template('index.html', title='Home', games=games)
    
@app.route('/teams')
@login_required
def teams():
    teams = TeamModel.query.order_by(TeamModel.name)
    form = EmptyForm()
    return render_template('teams.html', title='Teams', teams=teams, form=form)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def newGame():
    form = NewGameForm()
    if form.validate_on_submit():
        game = Game(
            hometeam_id=form.homeTeam.data,
            visitorteam_id=form.visitorTeam.data,
            score=form.result.data,
            playDate=form.date.data
        )
        db.session.add(game)
        db.session.commit()
        flash('Created new Game.')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        app.logger.info('Creating new Game')
    form.homeTeam.choices = [(int(g.id), g.name) for g in TeamModel.query.order_by('name')]
    form.visitorTeam.choices = [(int(g.id), g.name) for g in TeamModel.query.order_by('name')]
    return render_template('createGame.html', title='Create Game', form=form)
