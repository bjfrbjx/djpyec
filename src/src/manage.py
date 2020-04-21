#  -*- coding:utf-8 -*-
"""Django's command-line utility for administrative tasks."""
import os
import sys
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djpyec.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?"
                          ) from exc
    #execute_from_command_line(sys.argv)
    execute_from_command_line(['manage.py','runserver','0.0.0.0:8080'])
    #execute_from_command_line(['manage.py',"collectstatic"])
    #execute_from_command_line(['manage.py',"startapp","login"])
    #execute_from_command_line(['manage.py',"makemigrations"])
    #execute_from_command_line(['manage.py',"migrate"])
    #execute_from_command_line(['manage.py',"createsuperuser"])
    #execute_from_command_line(['manage.py',"shell"])
if __name__ == '__main__':
    main()
