# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin
# from app import db, login_manager

# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     username = db.Column(db.String(64), unique=True)  
#     password_hash = db.Column(db.String(256))  # Increased length for hash
#     role = db.Column(db.String(20), nullable=False, default='patient')
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     # Additional fields for medical experts
#     full_name = db.Column(db.String(100))
#     specialization = db.Column(db.String(100))
#     license_number = db.Column(db.String(50))
#     is_approved = db.Column(db.Boolean, default=False)

#     # Define relationships with explicit foreign keys
#     # Predictions made by this user as a patient
#     predictions_made = db.relationship('Prediction',
#                                      foreign_keys='Prediction.user_id',
#                                      backref=db.backref('patient', lazy=True),
#                                      lazy='dynamic')
    
#     # Predictions reviewed by this user as a medical expert
#     predictions_reviewed = db.relationship('Prediction',
#                                          foreign_keys='Prediction.reviewed_by',
#                                          backref=db.backref('expert', lazy=True),
#                                          lazy='dynamic')
    
#     # Messages sent by this user
#     messages_sent = db.relationship('Message',
#                                   foreign_keys='Message.sender_id',
#                                   backref='sender',
#                                   lazy='dynamic')
    
#     # Messages received by this user
#     messages_received = db.relationship('Message',
#                                       foreign_keys='Message.recipient_id',
#                                       backref='recipient',
#                                       lazy='dynamic')

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(
#             password,
#             method='pbkdf2:sha256',
#             salt_length=16
#         )

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

#     def is_admin(self):
#         return self.role == 'admin'

#     def is_medical_expert(self):
#         return self.role == 'medical_expert'

#     def is_patient(self):
#         return self.role == 'patient'

#     def get_display_name(self):
#         return self.full_name or self.username or self.email.split('@')[0]

# class Disease(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), unique=True, nullable=False)
#     description = db.Column(db.Text)
#     predictions = db.relationship('Prediction', backref='disease', lazy='dynamic')
#     medicines = db.relationship('Medicine', backref='disease', lazy='dynamic')

# class Medicine(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)
#     dosage = db.Column(db.String(100))
#     disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'), nullable=False)

# class Prediction(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'), nullable=False)
#     symptoms = db.Column(db.Text, nullable=False)
#     confidence = db.Column(db.Float, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     # Expert review fields
#     is_reviewed = db.Column(db.Boolean, default=False)
#     is_approved = db.Column(db.Boolean, default=False)
#     needs_attention = db.Column(db.Boolean, default=False)
#     expert_notes = db.Column(db.Text)
#     reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
#     # Chat messages for this prediction
#     messages = db.relationship('Message', backref='prediction', lazy='dynamic')

# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     prediction_id = db.Column(db.Integer, db.ForeignKey('prediction.id'), nullable=False)
#     body = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     is_read = db.Column(db.Boolean, default=False)

# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))


from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True)  
    password_hash = db.Column(db.String(256))  # Increased length for hash
    role = db.Column(db.String(20), nullable=False, default='patient')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional fields for medical experts
    full_name = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    license_number = db.Column(db.String(50))
    is_approved = db.Column(db.Boolean, default=False)

    # Relationships
    predictions_made = db.relationship('Prediction',
                                     foreign_keys='Prediction.user_id',
                                     backref=db.backref('patient', lazy=True),
                                     lazy='dynamic')
    
    predictions_reviewed = db.relationship('Prediction',
                                         foreign_keys='Prediction.reviewed_by',
                                         backref=db.backref('expert', lazy=True),
                                         lazy='dynamic')
    
    messages_sent = db.relationship('Message',
                                  foreign_keys='Message.sender_id',
                                  backref='sender',
                                  lazy='dynamic')
    
    messages_received = db.relationship('Message',
                                      foreign_keys='Message.recipient_id',
                                      backref='recipient',
                                      lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=16
        )

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def is_medical_expert(self):
        return self.role == 'medical_expert'

    def is_patient(self):
        return self.role == 'patient'

    def get_display_name(self):
        return self.full_name or self.username or self.email.split('@')[0]

class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    is_ai_predicted = db.Column(db.Boolean, default=False)  # Added for AI predictions
    
    # Relationships
    predictions = db.relationship('Prediction', backref='disease', lazy='dynamic')
    medicines = db.relationship('Medicine', backref='disease', lazy='dynamic')

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    dosage = db.Column(db.String(100))
    disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'), nullable=False)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)  # Stored as comma-separated string
    confidence = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Expert review fields
    is_reviewed = db.Column(db.Boolean, default=False,index=True)
    is_approved = db.Column(db.Boolean, default=False)
    needs_attention = db.Column(db.Boolean, default=False)
    expert_notes = db.Column(db.Text)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'),index=True)
    
    # Chat messages for this prediction
    messages = db.relationship('Message', backref='prediction', lazy='dynamic')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prediction_id = db.Column(db.Integer, db.ForeignKey('prediction.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False,index=True)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))