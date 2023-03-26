FROM python:3.9
ENV ALLOWED_HOSTS=url-or-hostname-without-port-and-http-s
ENV CORS_ALLOWED_ORIGINS="http://your-url:3000"
ENV CSRF_TRUSTED_ORIGINS="http://your-url:3000"
COPY . .
RUN pip install -r requirements.txt
RUN python manage.py migrate
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
