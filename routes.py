from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from app import app, db
from forms import (
    RegistrationForm, LoginForm, ProfileForm, 
    QuestionnaireForm, MessageForm
)
from models import (
    User, Question, UserResponse, 
    Like, Match, Message
)
from matching_system import MatchingSystem

matching_system = MatchingSystem()

@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        matches = matching_system.get_top_matches(current_user.id, limit=5)
        return render_template('home.html', matches=matches)
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created! Please complete your profile.', 'success')
        return redirect(url_for('profile'))
    
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.birth_date = form.birth_date.data
        current_user.gender = form.gender.data
        current_user.looking_for = form.looking_for.data
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        
        if form.profile_photo.data:
            # Handle profile photo upload
            pass
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('questionnaire'))
    
    elif request.method == 'GET':
        form.birth_date.data = current_user.birth_date
        form.gender.data = current_user.gender
        form.looking_for.data = current_user.looking_for
        form.bio.data = current_user.bio
        form.location.data = current_user.location
    
    return render_template('profile.html', title='Profile', form=form)

@app.route("/questionnaire", methods=['GET', 'POST'])
@login_required
def questionnaire():
    questions = Question.query.all()
    form = QuestionnaireForm(questions=questions)
    
    if form.validate_on_submit():
        # Clear previous responses
        UserResponse.query.filter_by(user_id=current_user.id).delete()
        
        for question in questions:
            field_name = f'question_{question.id}'
            response = getattr(form, field_name).data
            
            user_response = UserResponse(
                user_id=current_user.id,
                question_id=question.id,
                response=response
            )
            db.session.add(user_response)
        
        db.session.commit()
        flash('Your responses have been saved!', 'success')
        return redirect(url_for('matches'))
    
    return render_template('questionnaire.html', title='Questionnaire', form=form)

@app.route("/matches")
@login_required
def matches():
    matches = matching_system.get_top_matches(current_user.id)
    return render_template('matches.html', title='Matches', matches=matches)

@app.route("/like/<int:user_id>", methods=['POST'])
@login_required
def like_user(user_id):
    if user_id == current_user.id:
        return jsonify({'error': 'Cannot like yourself'}), 400
    
    like = Like.query.filter_by(
        sender_id=current_user.id,
        receiver_id=user_id
    ).first()
    
    if like:
        return jsonify({'error': 'Already liked this user'}), 400
    
    like = Like(sender_id=current_user.id, receiver_id=user_id)
    db.session.add(like)
    
    # Check if other user has liked current user
    other_like = Like.query.filter_by(
        sender_id=user_id,
        receiver_id=current_user.id
    ).first()
    
    if other_like:
        # It's a match!
        like.is_match = True
        other_like.is_match = True
        
        match = Match(
            user1_id=current_user.id,
            user2_id=user_id,
            match_score=matching_system.calculate_match_score(
                current_user.id,
                user_id
            )
        )
        db.session.add(match)
    
    db.session.commit()
    return jsonify({'success': True, 'is_match': bool(other_like)})

@app.route("/messages/<int:user_id>", methods=['GET', 'POST'])
@login_required
def messages(user_id):
    other_user = User.query.get_or_404(user_id)
    form = MessageForm()
    
    if form.validate_on_submit():
        message = Message(
            sender_id=current_user.id,
            receiver_id=user_id,
            content=form.message.data
        )
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('messages', user_id=user_id))
    
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.created_at.asc()).all()
    
    return render_template('messages.html', 
                         title=f'Chat with {other_user.username}',
                         form=form,
                         messages=messages,
                         other_user=other_user)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/privacy")
def privacy():
    return render_template('privacy.html', title='Privacy Policy')

@app.route("/terms")
def terms():
    return render_template('terms.html', title='Terms of Service')
