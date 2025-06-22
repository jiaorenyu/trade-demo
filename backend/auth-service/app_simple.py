# Simplified Authentication Service for Local Development
import os
import uuid
from datetime import datetime, timedelta

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from marshmallow import Schema, fields, ValidationError, validate
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from werkzeug.security import generate_password_hash, check_password_hash
import logging

# Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://ecommerce_user:ecommerce_pass@localhost:5432/ecommerce_db')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')

# Flask app setup
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
api = Api(app)
jwt = JWTManager(app)

# Database setup
engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Models
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'auth_service'}
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email_verified = Column(Boolean, default=True)  # Simplified: auto-verified
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

# Validation Schemas
class UserRegistrationSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8, max=128))

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

# API Resources
class RegisterResource(Resource):
    def post(self):
        try:
            schema = UserRegistrationSchema()
            data = schema.load(request.get_json())
            
            session = Session()
            try:
                # Check if user exists
                existing_user = session.query(User).filter_by(email=data['email']).first()
                if existing_user:
                    return {'error': 'User already exists'}, 400
                
                # Create user
                new_user = User(
                    email=data['email'],
                    password_hash=generate_password_hash(data['password'])
                )
                session.add(new_user)
                session.commit()
                
                logger.info(f"User registered: {data['email']}")
                return {
                    'message': 'User registered successfully',
                    'user_id': str(new_user.id)
                }, 201
            finally:
                session.close()
        except ValidationError as err:
            return {'error': err.messages}, 400
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return {'error': 'Internal server error'}, 500

class LoginResource(Resource):
    def post(self):
        try:
            schema = UserLoginSchema()
            data = schema.load(request.get_json())
            
            session = Session()
            try:
                user = session.query(User).filter_by(email=data['email']).first()
                if not user or not check_password_hash(user.password_hash, data['password']):
                    return {'error': 'Invalid credentials'}, 401
                
                if not user.is_active:
                    return {'error': 'Account deactivated'}, 403
                
                # Create token
                access_token = create_access_token(
                    identity=str(user.id),
                    additional_claims={'email': user.email}
                )
                
                logger.info(f"User logged in: {user.email}")
                return {
                    'access_token': access_token,
                    'user': {
                        'id': str(user.id),
                        'email': user.email
                    }
                }, 200
            finally:
                session.close()
        except ValidationError as err:
            return {'error': err.messages}, 400
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return {'error': 'Internal server error'}, 500

class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        return {
            'message': 'Access granted',
            'user_id': current_user_id
        }, 200

class HealthResource(Resource):
    def get(self):
        return {
            'status': 'healthy',
            'service': 'auth-service-simplified',
            'version': '1.0.0'
        }, 200

# Register routes
api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')
api.add_resource(ProtectedResource, '/protected')
api.add_resource(HealthResource, '/health')

if __name__ == '__main__':
    logger.info("🚀 Simplified Auth Service Starting")
    app.run(debug=True, host='0.0.0.0', port=5001)
