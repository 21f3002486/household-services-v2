from models import SERVICEREQUEST, CUSTOMER, PROFESSIONAL, SERVICE

professionals = PROFESSIONAL.query.all()
emails = [[p.to_dict()['email_id'], p.to_dict()['user_id']] for p in professionals]
for email, id in emails:
    pending_requests = len(SERVICEREQUEST.query.filter_by(id=id, service_status='open').all())
    print(email, pending_requests)

customers = CUSTOMER.query.all()
emails = [[c.to_dict()['email_id'], c.to_dict()['user_id']] for c in customers]
for email, id in emails:
    sreqs = SERVICEREQUEST.query.filter_by(customer_id=id).all()
    requested_services = len(sreqs)
    closed_services = len([s for s in sreqs if s.to_dict()['service_status'] == 'closed'])