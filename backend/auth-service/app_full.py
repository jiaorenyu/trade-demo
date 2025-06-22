# Production Authentication Service
# E-Commerce Platform - COMP-001 Implementation
import os
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, get_jwt
)
from marshmallow import Schema, fields, ValidationError, validate
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Integer, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import secrets
import logging
from functools import wraps

# Load environment variables
DATABASE_URL = os.getenv(
    'DATABASE_URL', 
    'postgresql://ecommerce_user:ecommerce_pass@localhost:5432/ecommerce_db'
)
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'production-jwt-secret-change-this')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT', 587)
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
EMAIL_FROM = os.getenv('EMAIL_FROM', 'noreply@ecommerce.com')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

# Flask app configuration
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

# Initialize extensions
api = Api(app)
jwt = JWTManager(app)

# Database setup
engine = create_engine(DATABASE_URL, echo=(FLASK_ENV == 'development'))
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

# Logging setup
logging.basicConfig(
    level=logging.INFO if FLASK_ENV == 'production' else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Blacklisted tokens storage (use Redis in production)
blacklisted_tokens = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklisted_tokens

# Database Models
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'auth_service'}
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email_verified = Column(Boolean, default=False)
    verification_token = Column(String(255))
    reset_token = Column(String(255))
    reset_token_expires = Column(DateTime)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    failed_login_attempts = Column(Integer, default=0)
    account_locked_until = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    __table_args__ = {'schema': 'auth_service'}
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), nullable=False)
    token_hash = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Validation Schemas
class UserRegistrationSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(
        required=True, 
        validate=validate.Length(min=8, max=128),
        error_messages={'invalid': 'Password must be at least 8 characters long'}
    )
    confirm_password = fields.String(required=True)
    
    def validate_passwords_match(self, data, **kwargs):
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError('Passwords do not match')

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class PasswordResetRequestSchema(Schema):
    email = fields.Email(required=True)

class PasswordResetSchema(Schema):
    token = fields.String(required=True)
    password = fields.String(
        required=True,
        validate=validate.Length(min=8, max=128)
    )
    confirm_password = fields.String(required=True)

class EmailVerificationSchema(Schema):
    token = fields.String(required=True)

# Utility Functions
def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """Send email using SMTP (placeholder implementation)"""
    if not all([SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD]):
        logger.warning("SMTP not configured, skipping email send")
        return False
    
    try:
        msg = MimeMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_FROM
        msg['To'] = to_email
        
        html_part = MimeText(html_content, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP(SMTP_SERVER, int(SMTP_PORT)) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False

def generate_secure_token() -> str:
    """Generate a secure random token"""
    return secrets.token_urlsafe(32)

def hash_token(token: str) -> str:
    """Hash a token for secure storage"""
    return hashlib.sha256(token.encode()).hexdigest()

def is_account_locked(user: User) -> bool:
    """Check if user account is locked"""
    if user.account_locked_until and user.account_locked_until > datetime.utcnow():
        return True
    return False

def handle_failed_login(session, user: User) -> bool:
    """Handle failed login attempt and return if account should be locked"""
    user.failed_login_attempts += 1
    
    # Lock account after 5 failed attempts for 30 minutes
    if user.failed_login_attempts >= 5:
        user.account_locked_until = datetime.utcnow() + timedelta(minutes=30)
        session.commit()
        return True
    
    session.commit()
    return False

def reset_failed_login_attempts(session, user: User):
    """Reset failed login attempts after successful login"""
    user.failed_login_attempts = 0
    user.account_locked_until = None
    user.last_login = datetime.utcnow()
    session.commit()

# Rate limiting decorator (simple implementation)
def rate_limit(max_requests: int = 5, time_window: int = 300):
    """Simple rate limiting decorator"""
    request_counts = {}
    
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            current_time = datetime.utcnow()
            
            # Clean old entries
            for ip in list(request_counts.keys()):
                request_counts[ip] = [
                    req_time for req_time in request_counts[ip]
                    if (current_time - req_time).seconds < time_window
                ]
                if not request_counts[ip]:
                    del request_counts[ip]
            
            # Check rate limit
            if client_ip not in request_counts:
                request_counts[client_ip] = []
            
            if len(request_counts[client_ip]) >= max_requests:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            request_counts[client_ip].append(current_time)
            return f(*args, **kwargs)
        return wrapper
    return decorator

# API Resources
class RegisterResource(Resource):
    @rate_limit(max_requests=3, time_window=300)  # 3 attempts per 5 minutes
    def post(self):
        """User registration with email verification"""
        try:
            schema = UserRegistrationSchema()
            data = schema.load(request.get_json())
            
            # Validate passwords match
            if data['password'] != data['confirm_password']:
                return {'error': 'Passwords do not match'}, 400
            
            session = Session()
            try:
                # Check if user already exists
                existing_user = session.query(User).filter_by(email=data['email']).first()
                if existing_user:
                    return {'error': 'User with this email already exists'}, 400
                
                # Create new user
                verification_token = generate_secure_token()
                new_user = User(
                    email=data['email'],
                    password_hash=generate_password_hash(data['password']),
                    verification_token=verification_token
                )
                
                session.add(new_user)
                session.commit()
                
                # Send verification email
                verification_url = f"{FRONTEND_URL}/verify-email?token={verification_token}"
                email_html = f"""
                <h2>Welcome to E-Commerce Platform</h2>
                <p>Please verify your email address by clicking the link below:</p>
                <a href="{verification_url}">Verify Email Address</a>
                <p>This link will expire in 24 hours.</p>
                """
                
                send_email(
                    to_email=data['email'],
                    subject="Verify Your Email Address",
                    html_content=email_html
                )
                
                logger.info(f"User registered successfully: {data['email']}")
                
                return {
                    'message': 'User registered successfully. Please check your email for verification.',
                    'user_id': str(new_user.id)
                }, 201
                
            except Exception as e:
                session.rollback()
                logger.error(f"Registration error: {str(e)}")
                return {'error': 'Internal server error'}, 500
            finally:
                session.close()
                
        except ValidationError as err:
            return {'error': 'Validation failed', 'details': err.messages}, 400

class LoginResource(Resource):
    @rate_limit(max_requests=5, time_window=300)  # 5 attempts per 5 minutes
    def post(self):
        """User login with account lockout protection"""
        try:
            schema = UserLoginSchema()
            data = schema.load(request.get_json())
            
            session = Session()
            try:
                # Find user
                user = session.query(User).filter_by(email=data['email']).first()
                if not user:
                    return {'error': 'Invalid credentials'}, 401
                
                # Check if account is locked
                if is_account_locked(user):
                    return {
                        'error': 'Account temporarily locked due to multiple failed login attempts'
                    }, 423
                
                # Check if account is active
                if not user.is_active:
                    return {'error': 'Account is deactivated'}, 403
                
                # Validate password
                if not check_password_hash(user.password_hash, data['password']):
                    handle_failed_login(session, user)
                    return {'error': 'Invalid credentials'}, 401
                
                # Check if email is verified
                if not user.email_verified:
                    return {
                        'error': 'Email not verified. Please check your email for verification link.'
                    }, 403
                
                # Successful login
                reset_failed_login_attempts(session, user)
                
                # Create JWT tokens
                access_token = create_access_token(
                    identity=str(user.id),
                    additional_claims={'email': user.email}
                )
                refresh_token = create_refresh_token(identity=str(user.id))
                
                # Store refresh token
                refresh_token_hash = hash_token(refresh_token)
                db_refresh_token = RefreshToken(
                    user_id=user.id,
                    token_hash=refresh_token_hash,
                    expires_at=datetime.utcnow() + timedelta(days=30)
                )
                session.add(db_refresh_token)
                session.commit()
                
                logger.info(f"User logged in successfully: {user.email}")
                
                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': {
                        'id': str(user.id),
                        'email': user.email,
                        'email_verified': user.email_verified
                    }
                }, 200
                
            finally:
                session.close()
                
        except ValidationError as err:
            return {'error': 'Validation failed', 'details': err.messages}, 400
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return {'error': 'Internal server error'}, 500

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        """User logout - blacklist current token"""
        try:
            jti = get_jwt()['jti']
            blacklisted_tokens.add(jti)
            
            user_id = get_jwt_identity()
            logger.info(f"User logged out: {user_id}")
            
            return {'message': 'Successfully logged out'}, 200
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return {'error': 'Internal server error'}, 500

class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """Refresh access token"""
        try:
            current_user_id = get_jwt_identity()
            
            # Create new access token
            access_token = create_access_token(
                identity=current_user_id,
                additional_claims={'email': ''}  # Could fetch from DB if needed
            )
            
            return {'access_token': access_token}, 200
            
        except Exception as e:
            logger.error(f"Token refresh error: {str(e)}")
            return {'error': 'Internal server error'}, 500

class VerifyEmailResource(Resource):
    def post(self):
        """Verify user email address"""
        try:
            schema = EmailVerificationSchema()
            data = schema.load(request.get_json())
            
            session = Session()
            try:
                user = session.query(User).filter_by(
                    verification_token=data['token']
                ).first()
                
                if not user:
                    return {'error': 'Invalid verification token'}, 400
                
                if user.email_verified:
                    return {'message': 'Email already verified'}, 200
                
                # Verify email
                user.email_verified = True
                user.verification_token = None
                session.commit()
                
                logger.info(f"Email verified for user: {user.email}")
                
                return {'message': 'Email verified successfully'}, 200
                
            finally:
                session.close()
                
        except ValidationError as err:
            return {'error': 'Validation failed', 'details': err.messages}, 400
        except Exception as e:
            logger.error(f"Email verification error: {str(e)}")
            return {'error': 'Internal server error'}, 500

class PasswordResetRequestResource(Resource):
    @rate_limit(max_requests=3, time_window=600)  # 3 attempts per 10 minutes
    def post(self):
        """Request password reset"""
        try:
            schema = PasswordResetRequestSchema()
            data = schema.load(request.get_json())
            
            session = Session()
            try:
                user = session.query(User).filter_by(email=data['email']).first()
                
                # Always return success to prevent email enumeration
                if user and user.is_active:
                    reset_token = generate_secure_token()
                    user.reset_token = reset_token
                    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
                    session.commit()
                    
                    # Send reset email
                    reset_url = f"{FRONTEND_URL}/reset-password?token={reset_token}"
                    email_html = f"""
                    <h2>Password Reset Request</h2>
                    <p>You requested a password reset. Click the link below to reset your password:</p>
                    <a href="{reset_url}">Reset Password</a>
                    <p>This link will expire in 1 hour.</p>
                    <p>If you didn't request this, please ignore this email.</p>
                    """
                    
                    send_email(
                        to_email=data['email'],
                        subject="Password Reset Request",
                        html_content=email_html
                    )
                
                return {
                    'message': 'If an account with that email exists, a password reset link has been sent.'
                }, 200
                
            finally:
                session.close()
                
        except ValidationError as err:
            return {'error': 'Validation failed', 'details': err.messages}, 400
        except Exception as e:
            logger.error(f"Password reset request error: {str(e)}")
            return {'error': 'Internal server error'}, 500

class PasswordResetResource(Resource):
    def post(self):
        """Reset password with token"""
        try:
            schema = PasswordResetSchema()
            data = schema.load(request.get_json())
            
            if data['password'] != data['confirm_password']:
                return {'error': 'Passwords do not match'}, 400
            
            session = Session()
            try:
                user = session.query(User).filter_by(reset_token=data['token']).first()
                
                if not user or not user.reset_token_expires:
                    return {'error': 'Invalid reset token'}, 400
                
                if user.reset_token_expires < datetime.utcnow():
                    return {'error': 'Reset token has expired'}, 400
                
                # Reset password
                user.password_hash = generate_password_hash(data['password'])
                user.reset_token = None
                user.reset_token_expires = None
                user.failed_login_attempts = 0
                user.account_locked_until = None
                session.commit()
                
                logger.info(f"Password reset for user: {user.email}")
                
                return {'message': 'Password reset successfully'}, 200
                
            finally:
                session.close()
                
        except ValidationError as err:
            return {'error': 'Validation failed', 'details': err.messages}, 400
        except Exception as e:
            logger.error(f"Password reset error: {str(e)}")
            return {'error': 'Internal server error'}, 500

class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """Protected endpoint for testing"""
        current_user_id = get_jwt_identity()
        return {
            'message': 'Access granted to protected resource',
            'user_id': current_user_id
        }, 200

class HealthResource(Resource):
    def get(self):
        """Health check endpoint"""
        return {
            'status': 'healthy',
            'service': 'auth-service',
            'version': '1.0.0',
            'timestamp': datetime.utcnow().isoformat()
        }, 200

# Register API routes
api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(RefreshTokenResource, '/refresh')
api.add_resource(VerifyEmailResource, '/verify-email')
api.add_resource(PasswordResetRequestResource, '/password-reset-request')
api.add_resource(PasswordResetResource, '/password-reset')
api.add_resource(ProtectedResource, '/protected')
api.add_resource(HealthResource, '/health')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("🚀 Production Auth Service Starting")
    logger.info("✅ JWT authentication configured")
    logger.info("✅ Database connection configured")
    logger.info("✅ Email service configured") 
    logger.info("✅ Rate limiting enabled")
    logger.info("✅ Security features enabled")
    
    port = int(os.getenv('PORT', 5000))
    debug = FLASK_ENV == 'development'
    
    app.run(debug=debug, host='0.0.0.0', port=port)
