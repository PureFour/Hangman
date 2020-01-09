from app import app, db
from flask import render_template, url_for, request, redirect, flash
from flask import url_for
from app.forms import SignInForm, SignUpForm
from models import User, Word
from flask_login import current_user, login_user, logout_user, login_required
import utils

@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('welcomePage.html')

@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    signInForm = SignInForm()
    if signInForm.validate_on_submit():
        user = User.query.filter_by(email=signInForm.email.data).first()
        print("found user: {}".format(user))
        if user is None or not user.check_password(signInForm.password.data):
            flash('Invalid email or password', 'danger')
            return render_template('sign_in.html', title='Sign In', form=signInForm)
        login_user(user, remember=signInForm.remember_me.data)
        print('redirecting to main game ...')
        return redirect(url_for('game'))
    else:    
        return render_template('sign_in.html', title='Sign In', form=signInForm)    

@app.route('/signOut')
def signOut():
    if current_user.is_authenticated:
        logout_user()
        flash('Sign out successful!', 'success')
        return redirect(url_for('index'))
    flash('You are not logged in!', 'warning')
    return redirect(url_for('signIn'))

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():   
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    signUpForm = SignUpForm()
    if signUpForm.validate_on_submit():
        given_mail = signUpForm.email.data
        given_password = signUpForm.password.data
        print("given_mail: {}".format(given_mail))
        print("given_password: {}".format(given_password))
        user = User(email=given_mail, score=0)
        print("user: {}".format(user))
        user.set_password(given_password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('signIn'))
    else:    
        return render_template('sign_up.html', title='Sign Up', form=signUpForm)    

@app.route('/highscores')
def highscores():
    users = User.query.order_by(User.score.desc()).all()
    print('users: ' + str(users))
    return render_template('highscores.html', users=users)  

@app.route('/game', methods=['GET', 'POST'])
def game():
    if not current_user.is_authenticated:
        flash('To play game you must login first! :P', 'warning')
        return redirect(url_for('signIn'))
    return render_template('main_game.html', current_user=current_user, is_gaming=True)

@app.route('/game/animals', methods=['GET', 'POST'])
def game_animals():
    animal_words = Word.query.filter_by(category='animals').all()
    secret_word = animal_words[utils.get_random_index(0, len(animal_words)-1)]
    
    if request.method == 'POST':
        if request.form['a'] == 'a':
            flash('you clicked ${letter}!', 'success')
            print('you clicked A!')
            return render_template('game_core.html', secret_word=secret_word, is_gaming=True)
        else:
            return render_template('game_core.html', secret_word=secret_word, is_gaming=True)
    elif request.method == 'GET':
        return render_template('game_core.html', secret_word=secret_word, is_gaming=True)

@app.route('/point')
def add_point():
    user = User.query.filter_by(email=current_user.email).first()
    user.add_point(1)
    db.session.commit()
    return redirect(url_for('index'))