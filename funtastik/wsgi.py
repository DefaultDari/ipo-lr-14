import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funtastik.settings')

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    import sys
    
    # Run the Django development server on port 5000
    sys.argv = ['manage.py', 'runserver', '0.0.0.0:5000']
    execute_from_command_line(sys.argv)
