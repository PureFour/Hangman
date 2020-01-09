from app import app, db
from flask import render_template, url_for, request, redirect, flash
from flask import url_for, send_from_directory
from app.forms import SignInForm, SignUpForm
from app.models import User, Word
from flask_login import current_user, login_user, logout_user, login_required
from .utils import *

##
secret_word = Word()
guessed_word = ''
guessed_letters = []
all_letters = get_alphabet()
losing_progress = 0
##

@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('welcome_page.html')

@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    signInForm = SignInForm()
    if signInForm.validate_on_submit():
        user = User.query.filter_by(email=signInForm.email.data).first()
        if user is None or not user.check_password(signInForm.password.data):
            flash('Invalid email or password', 'danger')
            return render_template('sign_in.html', title='Sign In', form=signInForm)
        login_user(user, remember=signInForm.remember_me.data)
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
        user = User(email=given_mail, score=0)
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
    return render_template('highscores.html', users=users)


@app.route('/game', methods=['GET', 'POST'])
def game():
    if not current_user.is_authenticated:
        flash('To play game you must login first!', 'warning')
        return redirect(url_for('signIn'))
    global all_letters, losing_progress
    all_letters = get_alphabet()
    losing_progress = 0    
    return render_template('categories.html', current_user=current_user, is_gaming=True)

@app.route('/game/<string:category>')
def get_random_word(category):
    global secret_word, guessed_word, all_letters, losing_progress

    db_words = Word.query.filter_by(category=category).all()
    secret_word = db_words[get_random_index(0, len(db_words) - 1)]
    guessed_word = prepare_word(secret_word.name)
    return render_template('game_core.html', guessed_word=guessed_word, letters=all_letters, secret_word=secret_word, losing_progress=losing_progress, is_gaming=True)

@app.route('/game/letter/<string:letter>')
def get_letter(letter):
    global guessed_letters, guessed_word, secret_word, all_letters, losing_progress
    guessed_letters.append(letter)

    indexes = find(letter, secret_word.name)

    if len(indexes) > 0:
        replace(all_letters, letter, letter + '1')
        for index in indexes:
            guessed_word = replace_str_index(guessed_word, index, letter) 
    else:
        replace(all_letters, letter, letter + '0')
        losing_progress += 12.5

    return render_template(
        'game_core.html',
        guessed_word=guessed_word,
        guessed_letters=guessed_letters,
        letters=all_letters,
        secret_word=secret_word,
        losing_progress=losing_progress,
        is_gaming=is_still_gaming(guessed_word, secret_word.name))


def add_point():
    user = User.query.filter_by(email=current_user.email).first()
    user.add_point(1)
    db.session.commit()

def is_still_gaming(guessed_word, secret_word):
    global losing_progress
    if losing_progress == 100:
        return False
    elif guessed_word == secret_word:
        add_point()
        return False
    else:
        return True    