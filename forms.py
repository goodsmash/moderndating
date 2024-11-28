from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    birth_date = DateField('Birth Date', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('non-binary', 'Non-binary'),
        ('other', 'Other'),
        ('prefer-not-to-say', 'Prefer not to say')
    ])
    looking_for = SelectField('Looking For', choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('non-binary', 'Non-binary'),
        ('anyone', 'Anyone')
    ])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])
    location = StringField('Location', validators=[DataRequired()])
    profile_photo = FileField('Profile Photo', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Update Profile')

class QuestionnaireForm(FlaskForm):
    def __init__(self, questions, *args, **kwargs):
        super(QuestionnaireForm, self).__init__(*args, **kwargs)
        
        for question in questions:
            field_name = f'question_{question.id}'
            
            if question.question_type == 'multiple_choice':
                choices = [(option, option) for option in question.options]
                setattr(self, field_name, SelectField(
                    question.question_text,
                    choices=choices,
                    validators=[DataRequired() if question.required else Optional()]
                ))
            
            elif question.question_type == 'scale':
                choices = [(str(i), str(i)) for i in range(1, 6)]
                setattr(self, field_name, SelectField(
                    question.question_text,
                    choices=choices,
                    validators=[DataRequired() if question.required else Optional()]
                ))
            
            else:  # text type
                setattr(self, field_name, TextAreaField(
                    question.question_text,
                    validators=[DataRequired() if question.required else Optional()]
                ))
    
    submit = SubmitField('Submit Answers')

class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')
