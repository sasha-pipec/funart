from conf.celery import app


@app.task
def search_new_data():
    return 'Новые данные'


