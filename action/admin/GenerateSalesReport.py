# action/admin/GenerateSalesReport.py

from DB_utils import get_sales_report
from utils import serialize_datetimes

def generate_sales_report_action(admin, params):
    e_id = params['e_id']
    sales_report = get_sales_report(e_id)
    return serialize_datetimes(sales_report)
