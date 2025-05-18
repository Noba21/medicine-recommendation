from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.expert import bp
from app.models import User, Prediction
from functools import wraps
from datetime import datetime

def expert_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_medical_expert():
            flash('Access denied. Medical expert privileges required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@login_required
@expert_required
def dashboard():
    # Get statistics
    total_reviews = current_user.predictions_reviewed.count()
    pending_reviews = Prediction.query.filter_by(is_reviewed=False).count()
    approved_predictions = current_user.predictions_reviewed.filter_by(is_approved=True).count()
    flagged_cases = current_user.predictions_reviewed.filter_by(needs_attention=True).count()

    # Get pending cases
    pending_cases = Prediction.query.filter_by(
        is_reviewed=False
    ).order_by(Prediction.created_at.desc()).limit(10).all()

    # Get recent activities
    recent_activities = current_user.predictions_reviewed.order_by(Prediction.updated_at.desc()).limit(10).all()
    
    now = datetime.utcnow()

    return render_template('expert/dashboard.html',
                         title='Expert Dashboard',
                         total_reviews=total_reviews,
                         pending_reviews=pending_reviews,
                         approved_predictions=approved_predictions,
                         flagged_cases=flagged_cases,
                         pending_cases=pending_cases,
                         recent_activities=recent_activities,
                         now=now)

@bp.route('/review/<int:case_id>', methods=['GET', 'POST'])
@login_required
@expert_required
def review_case(case_id):
    prediction = Prediction.query.get_or_404(case_id)
    now = datetime.utcnow()
    
    if request.method == 'POST':
        prediction.is_reviewed = True
        prediction.reviewed_by = current_user.id
        prediction.is_approved = request.form.get('approve') == 'true'
        prediction.expert_notes = request.form.get('notes')
        prediction.needs_attention = request.form.get('flag') == 'true'
        prediction.updated_at = now
        
        db.session.commit()
        flash('Review submitted successfully.', 'success')
        return redirect(url_for('expert.dashboard'))
    
    return render_template('expert/review_case.html', 
                         title='Review Case',
                         prediction=prediction,
                         now=now)
