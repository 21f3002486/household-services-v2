from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "my_secret_key"
app.config["JWT_SECRET_KEY"] = "JWT_SECRET"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)

app.config['CORS_HEADERS'] = "Content-Type"

####################################################################################

# Base User Model
class USER(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emailId = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'customer', 'professional'

    def to_dict(self): # easy to send to frontend
        return {
            'id': self.id,
            'email_id': self.emailId,
            'role': self.role
        }
        
# Customer Model
class CUSTOMER(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), unique=True, nullable=False)
    # emailId = db.Column(db.String(80), db.ForeignKey('user.emailId'), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    is_blocked = db.Column(db.Boolean, default=False)
    user = db.relationship('USER', backref=db.backref('customer')) #, foreign_keys=[user_id, emailId])

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email_id': self.user.emailId,
            'role': self.user.role,
            'address': self.address,
            'phone_number': self.phone_number,
            'is_blocked': self.is_blocked,
        }

# Professional Model
class PROFESSIONAL(db.Model):
    __tablename__ = 'professional'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), unique=True, nullable=False)
    # emailId = db.Column(db.String(80), db.ForeignKey('user.emailId'), unique=True, nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=True)
    is_approved = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    user = db.relationship('USER', backref=db.backref('professional')) #, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email_id': self.user.emailId,
            'role': self.user.role,
            'service_type': self.service_type,
            'experience': self.experience,
            'is_blocked': self.is_blocked,
            'is_approved': self.is_approved
        }

# Service Model
class SERVICE(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer, nullable=False)  
    description = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return{
            'service_id': self.id,
            'name': self.name,
            'price': self.price,
            'time_required': self.time_required,
            'description': self.description
        }

class SERVICEREQUEST(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id', ondelete="CASCADE"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete="CASCADE"), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id', ondelete="CASCADE"), nullable=True)
    date_of_request = db.Column(db.DateTime, nullable=False)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    service_status = db.Column(db.String(20), nullable=False, default="open")  # open, accepted, closed, rejected
    remarks = db.Column(db.String(200), nullable=True)

    service = db.relationship('SERVICE', backref='service_request')#, cascade="all, delete-orphan")
    customer = db.relationship('CUSTOMER', backref='service_request')#, cascade="all, delete-orphan")
    professional = db.relationship('PROFESSIONAL', backref='service_request')#, cascade="all, delete-orphan")

    def to_dict(self):
        return{
            'service_request_id': self.id,
            'service_id': self.service_id,
            'customer_id': self.customer_id,
            'professional_id': self.professional_id,
            'date_of_request': self.date_of_request,
            'date_of_completion': self.date_of_completion,
            'service_status': self.service_status,
            'remarks': self.remarks
        }

#############################################################################

class Register(Resource):
    def post(self):
        data = request.get_json()
        emailId = data.get('emailId')
        password = data.get('password')
        role = data.get('role')

        # print('data ', data)

        if role == 'customer':
            address = data.get('address')
            phone_number = data.get('phone_number')
        elif role == 'professional':
            service_type = data.get('service_type')
            experience = data.get('experience')
        else:
            return jsonify({'message': 'Wrong Role!'})
        
        if USER.query.filter_by(emailId=emailId).first():
            return jsonify({'message': "User already exists! Try logging in"})
    
        user = USER(emailId=emailId, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        if role=='customer':
            customer = CUSTOMER(user_id=user.id, address=address, phone_number=phone_number)
            db.session.add(customer)
        elif role=='professional':
            professional = PROFESSIONAL(user_id=user.id, service_type=service_type, experience=experience)
            db.session.add(professional)
        
        db.session.commit()
        return jsonify({'message': 'User created'})

    def get(self):
        return jsonify({"message": "GET request of /register"})

class Login(Resource):
    def post(self):
        data = request.get_json()
        emailId = data.get('emailId')
        password = data.get('password')
        role = data.get('role')

        user = USER.query.filter_by(emailId=emailId).first()

        # print(user)

        if user:
            if user.password == password:
                if user.role == role:
                    access_token = create_access_token(identity={"emailId": emailId, "role": role})
                    if user.role=='customer':
                        customer = CUSTOMER.query.filter_by(user_id=user.id).first()
                        return jsonify({"message": "Login Successful", "token":access_token, "is_blocked":customer.is_blocked})
                    elif user.role=='professional':
                        professional = PROFESSIONAL.query.filter_by(user_id=user.id).first()
                        return jsonify({"message": "Login Successful", "token":access_token, "is_blocked":professional.is_blocked})
                    elif user.role == "admin":
                        return jsonify({"message": "Login Successful", "token": access_token, "is_blocked":False})
                else:
                    return jsonify({"message": "Wrong Role, try with another role or register with appropriate role"})
            else:
                return jsonify({"message": "Wrong Password"})
        else:
            return jsonify({"message": "User does not exist! Try registering"})

    def get(self):
        return jsonify({"message": "GET of /login"})
    
class GetUsers(Resource):
    def get(self):
        
        pre_customers = CUSTOMER.query.all()
        customers = [c.to_dict() for c in pre_customers]
        
        pre_professionals = PROFESSIONAL.query.all()
        professionals = [p.to_dict() for p in pre_professionals]

        return jsonify({'message': 'Successful', 'customers': customers, 'professionals': professionals})

    def post(self):

        data = request.get_json()
        user_id = data.get('user_id')
        is_blocked = data.get('is_blocked')

        role = USER.query.filter_by(id=user_id).first().role

        if role=='customer':
            customer = CUSTOMER.query.filter_by(user_id=user_id).first()
            customer.is_blocked = is_blocked
            db.session.commit()
        elif role=='professional':
            professional = PROFESSIONAL.query.filter_by(user_id=user_id).first()
            professional.is_blocked = is_blocked
            db.session.commit()
        else:
            return jsonify({'message': "some error in role"})

        return jsonify({'message': 'success'})

class IsAccepted(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        print(current_user)
        email = current_user.get('emailId')

        professional = PROFESSIONAL.query.join(USER).filter_by(emailId=email).first()

        if professional.is_approved == False:
            return jsonify({'message': "You have not been approved by the admin yet. Please wait until admin approves your profile"})
        else:
            return jsonify({'message': "Approved"})
        
class ProfessionalRequests(Resource):
    def get(self):
        pre_professionals = PROFESSIONAL.query.filter_by(is_approved=False).all()
        professionals = [pr.to_dict() for pr in pre_professionals]
        # print(type(professionals))
        # print(professionals)
        return jsonify({'message': "Got requests", 'professionals': professionals})
    
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        # print(user_id)
        profo = PROFESSIONAL.query.filter_by(user_id=user_id).first()
        # print(profo)
        profo.is_approved = True
        db.session.commit()

        return jsonify({'message': "Professional {} approved!".format(user_id)})
    
class AddService(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        name = data.get('name')
        desc = data.get('description')
        time_req = data.get('time_required')
        base_price = data.get('base_price')

        service = SERVICE(name=name, price=base_price, time_required=time_req, description=desc)
        db.session.add(service)
        db.session.commit()

        return jsonify({'message': 'Service added successfully'})

class UpdateService(Resource):
    def post(self):
        data = request.get_json()

        service_id = data.get('service_id')
        print(service_id)   
        name = data.get('name')
        time_required = data.get('time_required')
        price = data.get('price')
        description = data.get('description')

        try:
            service = SERVICE.query.filter_by(id=service_id).first()

            service.name = name
            service.time_required = time_required
            service.price = price
            service.description = description

            db.session.commit()
        except:
            print(data)

        return jsonify({'message': "Updated Service"})

class DeleteService(Resource):
    def post(self):
        data = request.get_json()
        service_id = data.get('service_id')

        # print(service_id)

        try:
            service = SERVICE.query.filter_by(id=service_id).first()
            db.session.delete(service)
            db.session.commit()
        except:
            print(service_id)
        
        return jsonify({'message': "Service has been deleted"})

class GetServicesBySearch(Resource):
    def post(self):
        data = request.get_json()
        serviceName = data.get('serviceName')

        # print('backend: got this service name: {}'.format(serviceName))

        search = '%{}%'.format(serviceName)

        result = SERVICE.query.filter(SERVICE.name.like(search)).all()

        # print(result)

        services = [s.to_dict() for s in result]

        # print(services)

        return jsonify({'message':'Got searched services', 'services':services})

class GetUsersBySearch(Resource):
    def post(self):
        data = request.get_json()

        emailId = data.get('username')

        search = '%{}%'.format(emailId)

        c = db.session.query(CUSTOMER).join(USER).filter(USER.emailId.like(search)).all()
        p = db.session.query(PROFESSIONAL).join(USER).filter(USER.emailId.like(search)).all()

        customers = [cs.to_dict() for cs in c]
        professionals = [ps.to_dict() for ps in p]

        return jsonify({'message': 'got searched users', 'customers': customers, 'professionals': professionals})

class BookService(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        # print(current_user)
        user_email_id = current_user['emailId']

        data = request.get_json()
        date = datetime.strptime(data.get('date'), "%Y-%m-%d")
        service_id = data.get('service_id')
        professional_id = data.get('professional_id')

        print('backend got this date', date)
        print('backend got service_id', service_id)
        print('backend got this professional id', professional_id)

        customer = db.session.query(CUSTOMER).join(USER).filter(USER.emailId.like(user_email_id)).first()

        print(customer)

        service_request = SERVICEREQUEST(
            service_id=service_id, 
            customer_id=customer.id, 
            professional_id=professional_id,
            date_of_request=date
        )

        db.session.add(service_request)

        print('done')

        db.session.commit()

        print('commited')

        return jsonify({'message': 'Service requested successfully'})

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        customer_email = current_user['emailId']

        customer = db.session.query(CUSTOMER).join(USER).filter(USER.emailId.like(customer_email)).first()

        pre_sreqs = SERVICEREQUEST.query.filter_by(customer_id=customer.id).all()

        sreqs = [srq.to_dict() for srq in pre_sreqs]

        return jsonify({'message': 'Here are service requests for this user', 'service_requests': sreqs})

class DeleteServiceRequest(Resource):
    def post(self):
        data = request.get_json()
        print(data)

        id = data['id']

        sreq = SERVICEREQUEST.query.filter_by(id=id).first()

        db.session.delete(sreq)

        db.session.commit()

        return jsonify({'message': 'Service request successfully deleted'})

class ProfServiceRequests(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        email = current_user['emailId']
        prof = db.session.query(PROFESSIONAL).join(USER).filter(USER.emailId.like(email)).first()

        pre_prof_ser_reqs = SERVICEREQUEST.query.filter_by(professional_id=prof.id).all()

        prof_ser_reqs = [psr.to_dict() for psr in pre_prof_ser_reqs]

        return jsonify({'message': "got professional's service requests", 'prof_ser_reqs': prof_ser_reqs})

class Request(Resource):
    def get(self):
        id = request.args.get('id')
        type = request.args.get('type')

        request = SERVICEREQUEST.query.filter_by(service_request_id=id).first()

        if type == 'accept':
            request.service_status = 'accepted'
        elif type == 'reject':
            request.service_status = 'rejected'

        db.session.commit()

        return jsonify({'message': 'Service request {} {}ed'.format(id, type)})
    
#############################################################################

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(GetUsers, '/getUsers')
api.add_resource(IsAccepted, '/isaccepted')
api.add_resource(ProfessionalRequests, '/professionalrequests')
api.add_resource(AddService, '/addservice')
api.add_resource(UpdateService, '/updateservice')
api.add_resource(DeleteService, '/deleteservice')
api.add_resource(GetServicesBySearch, '/getservices')
api.add_resource(GetUsersBySearch, '/getusersbysearch')
api.add_resource(BookService, '/bookservice')
api.add_resource(DeleteServiceRequest, '/deleteservicerequest')
api.add_resource(ProfServiceRequests, '/getprofserreqs')
api.add_resource(Request, '/request')

with app.app_context():
    db.create_all()

    # creating admin if admin does not exist
    if not USER.query.filter_by(emailId="admin@gmail.com", password="admin", role="admin").first():
        admin = USER(emailId="admin@gmail.com", password="admin", role="admin")
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
