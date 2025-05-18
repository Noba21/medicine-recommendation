from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, EditProfileForm, ChangePasswordForm
from app.models import User, Prediction, Message
from sqlalchemy import func

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    now = datetime.utcnow()
    if form.validate_on_submit():
        # Debug logging
        print(f"Login attempt with email: {form.email.data}")
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print(f"User found: {user.email}, Role: {user.role}")
            print(f"Stored password hash: {user.password_hash}")
            if user.check_password(form.password.data):
                print("Password check passed")
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or urlparse(next_page).netloc != '':
                    next_page = url_for('main.index')
                return redirect(next_page)
            else:
                print("Password check failed")
        else:
            print("User not found")
        flash('Invalid email or password', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html', title='Sign In', form=form, now=now)

@bp.route('/logout')
def logout():
    now = datetime.utcnow()
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    now = datetime.utcnow()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            full_name=form.full_name.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form, now=now)

@bp.route('/profile')
@login_required
def profile():
    # Get statistics for the profile page
    now = datetime.utcnow()
    
    # Common stats - count distinct prediction_id where messages exist
    active_chats_query = db.session.query(func.count(func.distinct(Message.prediction_id)))
    
    if current_user.is_medical_expert():
        active_chats_query = active_chats_query.filter(Message.recipient_id == current_user.id)
    else:
        active_chats_query = active_chats_query.filter(Message.sender_id == current_user.id)
    
    active_chats = active_chats_query.scalar() or 0
    
    # Stats for medical experts
    predictions_reviewed = Prediction.query.filter_by(reviewed_by=current_user.id).count() if current_user.is_medical_expert() else 0
    response_rate = 95  # Placeholder, calculate based on actual data if available
    
    # Stats for patients
    total_predictions = Prediction.query.filter_by(user_id=current_user.id).count()
    
    # Count distinct prediction_ids where the user has messages
    completed_consultations_query = db.session.query(func.count(func.distinct(Message.prediction_id)))
    
    if current_user.is_medical_expert():
        completed_consultations_query = completed_consultations_query.filter(
            Message.recipient_id == current_user.id,
            Prediction.is_reviewed == True
        ).join(Prediction, Message.prediction_id == Prediction.id)
    else:
        completed_consultations_query = completed_consultations_query.filter(
            Message.sender_id == current_user.id,
            Prediction.is_reviewed == True
        ).join(Prediction, Message.prediction_id == Prediction.id)
    
    completed_consultations = completed_consultations_query.scalar() or 0
    
    return render_template('profile.html', 
                          title='My Profile',
                          active_chats=active_chats,
                          predictions_reviewed=predictions_reviewed,
                          response_rate=response_rate,
                          total_predictions=total_predictions,
                          completed_consultations=completed_consultations,
                          now=now)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(original_email=current_user.email)
    now = datetime.utcnow()
    
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.full_name = form.full_name.data
        
        # Update medical expert specific fields if applicable
        if current_user.is_medical_expert():
            current_user.specialization = form.specialization.data
            current_user.license_number = form.license_number.data
        
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.full_name.data = current_user.full_name
        
        # Populate medical expert specific fields if applicable
        if current_user.is_medical_expert():
            form.specialization.data = current_user.specialization
            form.license_number.data = current_user.license_number
    
    return render_template('auth/edit_profile.html', title='Edit Profile', form=form, now=now)

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    now = datetime.utcnow()
    
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.password.data)
            db.session.commit()
            flash('Your password has been updated.', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Current password is incorrect.', 'danger')
    
    return render_template('auth/change_password.html', title='Change Password', form=form, now=now)
