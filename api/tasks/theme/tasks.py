from api.tasks.theme.rating import ThemeRatingZeroingService
from conf.celery import app
from service_objects.services import ServiceOutcome


@app.task
def zeroing_rating_themes():
    ServiceOutcome(ThemeRatingZeroingService, {})



