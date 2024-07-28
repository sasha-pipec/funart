import environ
env = environ.Env()
DATABASES = {"default": env.db()}
DATABASES["default"]['TEST'] = {'NAME': 'mytestdatabase'}

