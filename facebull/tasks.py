from celery.decorators import task
import requests
from celery.utils.log import get_task_logger
from .models import User
from django.utils.timezone import datetime

logger = get_task_logger(__name__)

def enrich_user(email):
    user = User.objects.get(email=email)
    response = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=f5f1c940ec2b4ce9a2990f1bd00014be")
    user_ip = response.json()['ip_address']
    user.ip_joined = user_ip

    country = response.json()['country_code']
    year = datetime.today().year
    month = datetime.today().month
    day = datetime.today().day
    response = requests.get(f"https://holidays.abstractapi.com/v1/?api_key=706bad8d74514e3fad53d328c7e14a19&country={country}&year={year}&month={month}&day={day}")
    if hasattr(response.json(), 'name'):
        user.holiday = True

    user.save()
    print(user.ip_joined)
    print(user.holiday)
    return user.email

@task(name="enrich_user_task")
def enrich_user_task(email):
    logger.info("User Enriched")
    return enrich_user(email)