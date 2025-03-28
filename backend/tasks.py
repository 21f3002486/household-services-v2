from celery import shared_task
from models import SERVICEREQUEST
import flask_excel as excel

# CELERY TASKS
@shared_task(ignore_result=False)
def make_csv_request():
    sreqs = SERVICEREQUEST.query.all()

    csv_output = excel.make_response_from_query_sets(sreqs, [
        "id",
        "service_id",
        "customer_id",
        "professional_id",
        "date_of_request",
        "service_status",
        "remarks",
        "rating"
    ], "csv")

    filename="generated_csvs/admin_report.csv"

    with open(filename, 'wb') as f:
        f.write(csv_output.data)
    
    return str(filename)