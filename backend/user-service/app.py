# Production User Service - E-Commerce Platform
import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError, validate
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.dialects.postgresql import UUID as PGUUID
import logging

# Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://ecommerce_user:ecommerce_pass@localhost:5432/ecommerce_db')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'production-jwt-secret-change-this')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

api = Api(app)
jwt = JWTManager(app)

engine = create_engine(DATABASE_URL, echo=(FLASK_ENV == 'development'))
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Models
class Profile(Base):
    __tablename__ = 'profiles'
    __table_args__ = {'schema': 'user_service'}
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), unique=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    preferred_language = Column(String(10), default='en')
    preferred_currency = Column(String(3), default='USD')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Address(Base):
    __tablename__ = 'addresses'
    __table_args__ = {'schema': 'user_service'}
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), nullable=False)
    type = Column(String(20), nullable=False)
    is_primary = Column(Boolean, default=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    address_line_1 = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country_code = Column(String(2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Validation Schemas
class ProfileSchema(Schema):
    first_name = fields.String(validate=validate.Length(max=100))
    last_name = fields.String(validate=validate.Length(max=100))
    phone = fields.String(validate=validate.Length(max=20))
    preferred_language = fields.String(validate=validate.OneOf(['en', 'es', 'zh']))
    preferred_currency = fields.String(validate=validate.OneOf(['USD', 'EUR', 'CNY']))

class AddressSchema(Schema):
    type = fields.String(required=True, validate=validate.OneOf(['billing', 'shipping', 'both']))
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    address_line_1 = fields.String(required=True)
    city = fields.String(required=True)
    postal_code = fields.String(required=True)
    country_code = fields.String(required=True, validate=validate.Length(equal=2))

# API Resources
class ProfileResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        session = Session()
        try:
            profile = session.query(Profile).filter_by(user_id=user_id).first()
            if not profile:
                profile = Profile(user_id=user_id)
                session.add(profile)
                session.commit()
            
            return {
                'id': str(profile.id),
                'user_id': str(profile.user_id),
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'phone': profile.phone,
                'preferred_language': profile.preferred_language,
                'preferred_currency': profile.preferred_currency
            }, 200
        finally:
            session.close()
    
    @jwt_required()
    def put(self):
        try:
            schema = ProfileSchema()
            data = schema.load(request.get_json())
            user_id = get_jwt_identity()
            
            session = Session()
            try:
                profile = session.query(Profile).filter_by(user_id=user_id).first()
                if not profile:
                    profile = Profile(user_id=user_id)
                    session.add(profile)
                
                for field, value in data.items():
                    setattr(profile, field, value)
                
                session.commit()
                return {'message': 'Profile updated successfully'}, 200
            finally:
                session.close()
        except ValidationError as err:
            return {'error': err.messages}, 400

class AddressListResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        session = Session()
        try:
            addresses = session.query(Address).filter_by(user_id=user_id).all()
            return {
                'addresses': [
                    {
                        'id': str(addr.id),
                        'type': addr.type,
                        'is_primary': addr.is_primary,
                        'first_name': addr.first_name,
                        'last_name': addr.last_name,
                        'address_line_1': addr.address_line_1,
                        'city': addr.city,
                        'postal_code': addr.postal_code,
                        'country_code': addr.country_code
                    } for addr in addresses
                ]
            }, 200
        finally:
            session.close()
    
    @jwt_required()
    def post(self):
        try:
            schema = AddressSchema()
            data = schema.load(request.get_json())
            user_id = get_jwt_identity()
            
            session = Session()
            try:
                new_address = Address(user_id=user_id, **data)
                session.add(new_address)
                session.commit()
                
                return {
                    'message': 'Address created successfully',
                    'address_id': str(new_address.id)
                }, 201
            finally:
                session.close()
        except ValidationError as err:
            return {'error': err.messages}, 400

class HealthResource(Resource):
    def get(self):
        return {
            'status': 'healthy',
            'service': 'user-service',
            'version': '1.0.0'
        }, 200

# Register routes
api.add_resource(ProfileResource, '/profile')
api.add_resource(AddressListResource, '/addresses')
api.add_resource(HealthResource, '/health')

if __name__ == '__main__':
    logger.info("🚀 User Service Starting")
    port = int(os.getenv('PORT', 5001))
    app.run(debug=(FLASK_ENV == 'development'), host='0.0.0.0', port=port)
