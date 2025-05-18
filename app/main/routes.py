
# File: routes.py (updated version)
from flask import render_template, flash, redirect, url_for, request, jsonify, session
from flask_login import login_required, current_user
from app.main import bp
from app.models import Prediction, Disease, Medicine, User, Message
from app import db
from datetime import datetime
from dataclasses import dataclass
from typing import List
from app.ml.predictor import DiseasePredictor

# Initialize the predictor
predictor = DiseasePredictor()

@dataclass
class ChatNotification:
    prediction_id: int
    patient_name: str
    symptoms: str
    created_at: datetime
    is_read: bool

@bp.route('/')
@bp.route('/index')
def index():
    now = datetime.now()
    return render_template('index.html', title='Home', now=now)

@bp.route('/expert_notifications')
@login_required
def expert_notifications():
    if not current_user.is_medical_expert():
        flash('Access denied. Medical experts only.', 'danger')
        return redirect(url_for('main.index'))
    
    predictions = Prediction.query.filter_by(reviewed_by=current_user.id)\
        .order_by(Prediction.created_at.desc()).all()
        
    notifications: List[ChatNotification] = []
    for pred in predictions:
        has_unread = Message.query.filter_by(
            prediction_id=pred.id,
            recipient_id=current_user.id,
            is_read=False
        ).first() is not None
        
        patient = User.query.get(pred.user_id)
        notifications.append(ChatNotification(
            prediction_id=pred.id,
            patient_name=patient.get_display_name(),
            symptoms=pred.symptoms,
            created_at=pred.created_at,
            is_read=not has_unread
        ))
    
    unread_count = sum(1 for n in notifications if not n.is_read)
    return render_template('expert_notifications.html', 
                         title='Notifications',
                         notifications=notifications,
                         unread_count=unread_count,
                         now=datetime.now())

@bp.route('/create_test_disease')
@login_required
def create_test_disease():
    test_disease = Disease.query.filter_by(name='Test Disease').first()
    if not test_disease:
        test_disease = Disease(
            name='Test Disease',
            description='This is a test disease for the chat system.'
        )
        db.session.add(test_disease)
        db.session.commit()
        flash('Test disease created successfully.', 'success')
    else:
        flash('Test disease already exists.', 'info')
    return redirect(url_for('main.predict'))

@bp.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        symptoms = request.form.getlist('symptoms')
        if not symptoms or len(symptoms) < 3:
            flash('Please select at least 3 symptoms', 'warning')
            return redirect(url_for('main.predict'))
        
        try:
            # Get prediction from model
            result = predictor.predict(symptoms)
            
            # Store extended prediction data in session for result page
            session['last_prediction'] = {
                'top_5': result['top_5'],
                'medicines': result['medicines'],
                'disease': result['top_disease']
            }
            
            # Create or get disease record (using top disease)
            disease_name = result['top_disease']
            disease = Disease.query.filter_by(name=disease_name).first()
            if not disease:
                disease = Disease(
                    name=disease_name, 
                    description="AI Predicted Disease",
                     is_ai_predicted=True
                )
                db.session.add(disease)
                db.session.commit()
            
            # Create prediction record
            prediction = Prediction(
                user_id=current_user.id,
                disease_id=disease.id,
                symptoms=",".join(symptoms),
                confidence=max(result['top_5'].values()),  # Use top disease confidence
                needs_attention=True
            )
            db.session.add(prediction)
            db.session.commit()
            
            # Save recommended medicines to the database
            if 'medicines' in result and result['medicines']:
                for medicine_name in result['medicines']:
                    # Check if this medicine already exists for this disease
                    existing_medicine = Medicine.query.filter_by(
                        name=medicine_name,
                        disease_id=disease.id
                    ).first()
                    
                    if not existing_medicine:
                        medicine = Medicine(
                            name=medicine_name,
                            description="AI Recommended Medicine",
                            dosage="Consult a doctor for proper dosage",
                            disease_id=disease.id
                        )
                        db.session.add(medicine)
                
                db.session.commit()
            
            return redirect(url_for('main.prediction_result', id=prediction.id))
            
        except ValueError as e:
            flash(str(e), 'warning')
            return redirect(url_for('main.predict'))
    
    # GET request - show prediction form
    all_symptoms = predictor.get_symptoms()
    return render_template('predict.html', 
                         title='Predict Disease', 
                         symptoms=all_symptoms)

@bp.route('/prediction/<int:id>')
@login_required
def prediction_result(id):
    prediction = Prediction.query.get_or_404(id)
    
    # Only allow access to own predictions (unless medical expert)
    if not current_user.is_medical_expert() and prediction.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    # Get prediction details from session if available
    prediction_data = session.get('last_prediction', {})
    
    # If not available in session (e.g., direct URL access), re-run prediction
    if not prediction_data or prediction.id != getattr(request, 'prediction_id', None):
        try:
            symptoms = prediction.symptoms.split(',')
            result = predictor.predict(symptoms)
            prediction_data = {
                'top_5': result['top_5'],
                'medicines': result['medicines'],
                'disease': result['top_disease']
            }
        except Exception as e:
            flash('Could not regenerate prediction details', 'error')
            prediction_data = {}
    
    # Clear session data after use
    session.pop('last_prediction', None)
    
    # Get available medical experts
    medical_experts = User.query.filter_by(role='medical_expert', is_approved=True).all()
    
    return render_template('prediction_result.html',
                         title='Prediction Result',
                         prediction=prediction,
                         medical_experts=medical_experts,
                         **prediction_data)

@bp.route('/start_chat/<int:prediction_id>/<int:expert_id>')
@login_required
def start_chat(prediction_id, expert_id):
    prediction = Prediction.query.get_or_404(prediction_id)
    expert = User.query.get_or_404(expert_id)
    
    if current_user.id != prediction.user_id:
        flash('You do not have permission to start this chat.', 'danger')
        return redirect(url_for('main.history'))
    
    if not expert.is_medical_expert() or not expert.is_approved:
        flash('Invalid medical expert selected.', 'danger')
        return redirect(url_for('main.history'))
    
    prediction.reviewed_by = expert.id
    db.session.commit()
    return redirect(url_for('main.chat', prediction_id=prediction_id))

@bp.route('/chat/<int:prediction_id>')
@login_required
def chat(prediction_id):
    prediction = Prediction.query.get_or_404(prediction_id)
    
    if not (current_user.id == prediction.user_id or 
            (current_user.is_medical_expert() and current_user.id == prediction.reviewed_by)):
        flash('You do not have permission to access this chat.', 'danger')
        return redirect(url_for('main.index'))
    
    patient = User.query.get(prediction.user_id)
    expert = User.query.get(prediction.reviewed_by) if prediction.reviewed_by else None
    
    messages = Message.query.filter_by(prediction_id=prediction_id)\
        .order_by(Message.created_at.asc()).all()
    
    unread_messages = Message.query.filter_by(
        prediction_id=prediction_id,
        recipient_id=current_user.id,
        is_read=False
    ).all()
    
    # Get recommended medicines for this prediction
    recommended_medicines = Medicine.query.filter_by(disease_id=prediction.disease_id).all()
    
    for message in unread_messages:
        message.is_read = True
    db.session.commit()
    
    return render_template('chat.html', 
                         title='Chat',
                         prediction=prediction,
                         messages=messages,
                         patient=patient,
                         expert=expert,
                         recommended_medicines=recommended_medicines,
                         now=datetime.now())

@bp.route('/send_message/<int:prediction_id>', methods=['POST'])
@login_required
def send_message(prediction_id):
    prediction = Prediction.query.get_or_404(prediction_id)
    
    if not (current_user.id == prediction.user_id or 
            (current_user.is_medical_expert() and current_user.id == prediction.reviewed_by)):
        return jsonify({'error': 'Unauthorized'}), 403
    
    message_body = request.form.get('message')
    if not message_body:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    recipient_id = prediction.reviewed_by if current_user.id == prediction.user_id else prediction.user_id
    
    message = Message(
        sender_id=current_user.id,
        recipient_id=recipient_id,
        prediction_id=prediction_id,
        body=message_body
    )
    
    db.session.add(message)
    db.session.commit()
    
    return jsonify({
        'id': message.id,
        'body': message.body,
        'sender_name': message.sender.get_display_name(),
        'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'is_sender': True
    })

@bp.route('/history')
@login_required
def history():
    now = datetime.now()
    view = request.args.get('view', 'predictions')
    
    # Get all predictions for this user
    predictions_query = Prediction.query.filter_by(user_id=current_user.id)
    
    if view == 'chats':
        # For the chats view, only show predictions with an assigned medical expert
        predictions = predictions_query.filter(Prediction.reviewed_by.isnot(None))\
            .order_by(Prediction.created_at.desc()).all()
        title = 'My Chats'
        template = 'chat_list.html'
    else:
        # For the regular history view, show all predictions
        predictions = predictions_query.order_by(Prediction.created_at.desc()).all()
        title = 'Prediction History'
        template = 'history.html'
    
    return render_template(template, title=title, predictions=predictions, now=now, view=view)

@bp.route('/profile')
@login_required
def profile():
    now = datetime.now()
    if current_user.is_medical_expert():
        predictions_reviewed = Prediction.query.filter_by(reviewed_by=current_user.id).count()
        active_chats = Prediction.query.filter_by(
            reviewed_by=current_user.id,
            is_reviewed=False
        ).count()
        
        total_assigned = max(predictions_reviewed, 1)
        responded = Message.query.filter_by(sender_id=current_user.id).distinct(Message.prediction_id).count()
        response_rate = int((responded / total_assigned) * 100)
        
        return render_template('profile.html', 
                             title='Profile',
                             predictions_reviewed=predictions_reviewed,
                             active_chats=active_chats,
                             response_rate=response_rate,
                             now=now)
    else:
        total_predictions = Prediction.query.filter_by(user_id=current_user.id).count()
        active_chats = Prediction.query.filter_by(
            user_id=current_user.id,
            is_reviewed=False
        ).count()
        completed_consultations = Prediction.query.filter_by(
            user_id=current_user.id,
            is_reviewed=True
        ).count()
        
        return render_template('profile.html',
                             title='Profile',
                             total_predictions=total_predictions,
                             active_chats=active_chats,
                             completed_consultations=completed_consultations,
                             now=now)

@bp.route('/about')
def about():
    now = datetime.now()
    return render_template('about.html', title='About', now=now)