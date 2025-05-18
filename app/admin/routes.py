from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.admin import bp
from app.models import User, Disease, Medicine, Prediction
from functools import wraps
from datetime import datetime
from werkzeug.security import generate_password_hash

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    users = User.query.filter_by(role='patient').order_by(User.created_at.desc()).limit(5).all()
    prediction_count = Prediction.query.count()
    medical_experts = User.query.filter_by(role='medical_expert').all()
    expert_count = len(medical_experts)
    now = datetime.utcnow()
    
    return render_template('admin/dashboard.html',
                         title='Admin Dashboard',
                         users=users,
                         prediction_count=prediction_count,
                         medical_experts=medical_experts,
                         expert_count=expert_count,
                         now=now)

@bp.route('/add_expert', methods=['POST'])
@login_required
@admin_required
def add_expert():
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    specialization = request.form.get('specialization')
    license_number = request.form.get('license_number')
    password = request.form.get('password')
    
    # Debug logging
    print(f"Adding expert with email: {email}")
    
    if User.query.filter_by(email=email).first():
        flash('Email already registered.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    expert = User(
        email=email,
        full_name=full_name,
        specialization=specialization,
        license_number=license_number,
        role='medical_expert',
        is_approved=True  # Auto-approve experts created by admin
    )
    
    # Use PBKDF2-SHA256 explicitly
    expert.password_hash = generate_password_hash(
        password,
        method='pbkdf2:sha256',
        salt_length=16
    )
    print(f"Password hash created: {expert.password_hash}")
    
    db.session.add(expert)
    db.session.commit()
    
    flash('Medical expert added successfully.', 'success')
    return redirect(url_for('admin.dashboard'))

@bp.route('/approve_expert/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def approve_expert(user_id):
    expert = User.query.get_or_404(user_id)
    if expert.role != 'medical_expert':
        flash('Invalid user role.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    expert.is_approved = True
    db.session.commit()
    
    flash('Medical expert approved successfully.', 'success')
    return redirect(url_for('admin.dashboard'))

@bp.route('/delete_expert/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_expert(user_id):
    expert = User.query.get_or_404(user_id)
    if expert.role != 'medical_expert':
        flash('Invalid user role.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    db.session.delete(expert)
    db.session.commit()
    
    flash('Medical expert deleted successfully.', 'success')
    return redirect(url_for('admin.dashboard'))

@bp.route('/analytics')
@login_required
@admin_required
def analytics():
    # Get basic statistics
    total_users = User.query.count()
    total_patients = User.query.filter_by(role='patient').count()
    total_experts = User.query.filter_by(role='medical_expert').count()
    total_predictions = Prediction.query.count()
    total_diseases = Disease.query.count()
    total_medicines = Medicine.query.count()
    
    # Get top predicted diseases
    disease_counts = db.session.query(
        Disease.name, 
        db.func.count(Prediction.id).label('count')
    ).join(Prediction).group_by(Disease.name).order_by(db.desc('count')).limit(5).all()
    
    top_diseases = [{'name': name, 'count': count} for name, count in disease_counts]
    
    # Get prediction trends (by month)
    month_counts = db.session.query(
        db.func.date_format(Prediction.created_at, '%Y-%m').label('month'),
        db.func.count(Prediction.id).label('count')
    ).group_by('month').order_by('month').all()
    
    prediction_trends = [{'month': month, 'count': count} for month, count in month_counts]
    
    # Get user registration trends
    user_month_counts = db.session.query(
        db.func.date_format(User.created_at, '%Y-%m').label('month'),
        db.func.count(User.id).label('count')
    ).group_by('month').order_by('month').all()
    
    user_trends = [{'month': month, 'count': count} for month, count in user_month_counts]
    
    # Get common symptoms
    all_symptoms = []
    for prediction in Prediction.query.all():
        symptoms = prediction.symptoms.split(',')
        all_symptoms.extend([s.strip() for s in symptoms])
    
    symptom_counts = {}
    for symptom in all_symptoms:
        if symptom:
            symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1
    
    top_symptoms = sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    top_symptoms = [{'name': name, 'count': count} for name, count in top_symptoms]
    
    now = datetime.utcnow()
    return render_template('admin/analytics.html', 
                         title='Analytics Dashboard',
                         total_users=total_users,
                         total_patients=total_patients,
                         total_experts=total_experts,
                         total_predictions=total_predictions,
                         total_diseases=total_diseases,
                         total_medicines=total_medicines,
                         top_diseases=top_diseases,
                         prediction_trends=prediction_trends,
                         user_trends=user_trends,
                         top_symptoms=top_symptoms,
                         now=now)

@bp.route('/init_sample_data')
@login_required
@admin_required
def init_sample_data():
    # Add sample diseases
    diseases = [
        {
            'name': 'Common Cold',
            'description': 'A viral infection of the upper respiratory tract, causing symptoms like runny nose, sore throat, and cough.',
            'medicines': [
                {
                    'name': 'Acetaminophen',
                    'description': 'Pain reliever and fever reducer',
                    'dosage': '500mg every 4-6 hours'
                },
                {
                    'name': 'Pseudoephedrine',
                    'description': 'Decongestant',
                    'dosage': '60mg every 4-6 hours'
                }
            ]
        },
        {
            'name': 'Influenza',
            'description': 'A viral infection that attacks your respiratory system, causing fever, body aches, and fatigue.',
            'medicines': [
                {
                    'name': 'Oseltamivir',
                    'description': 'Antiviral medication',
                    'dosage': '75mg twice daily for 5 days'
                },
                {
                    'name': 'Ibuprofen',
                    'description': 'Pain reliever and fever reducer',
                    'dosage': '400mg every 4-6 hours'
                }
            ]
        },
        {
            'name': 'Migraine',
            'description': 'A neurological condition causing severe headaches, often with nausea and sensitivity to light and sound.',
            'medicines': [
                {
                    'name': 'Sumatriptan',
                    'description': 'Migraine-specific medication',
                    'dosage': '50-100mg at onset of migraine'
                },
                {
                    'name': 'Rizatriptan',
                    'description': 'Migraine relief medication',
                    'dosage': '5-10mg as needed'
                }
            ]
        }
    ]

    for disease_data in diseases:
        # Check if disease already exists
        if not Disease.query.filter_by(name=disease_data['name']).first():
            disease = Disease(
                name=disease_data['name'],
                description=disease_data['description']
            )
            db.session.add(disease)
            db.session.flush()  # Get the disease ID

            # Add medicines for this disease
            for medicine_data in disease_data['medicines']:
                medicine = Medicine(
                    name=medicine_data['name'],
                    description=medicine_data['description'],
                    dosage=medicine_data['dosage'],
                    disease_id=disease.id
                )
                db.session.add(medicine)

    db.session.commit()
    flash('Sample diseases and medicines added successfully.', 'success')
    return redirect(url_for('main.index'))
