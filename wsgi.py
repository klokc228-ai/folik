import os
from django.core.wsgi import get_wsgi_application

# Указываем настройки проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'folik.settings')

# WSGI приложение
application = get_wsgi_application()
