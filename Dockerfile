FROM python:3.8

RUN apt update -y  &&  apt upgrade -y && apt-get update
RUN apt-get install -y gcc &&  \
    apt-get install -y unixodbc-dev libgssapi-krb5-2 &&  \
    apt-get install -y nginx && \
    apt-get install -y curl && \
    apt-get install -y python3-pip &&  \
    apt-get update &&  \
    rm -rf /var/lib/apt/lists/*


RUN apt-get update

WORKDIR /app

COPY requirements.txt .
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN cp nginx.conf /etc/nginx/sites-available/ && \
    ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/nginx.conf && \
    rm /etc/nginx/sites-enabled/default && \
    chown -R www-data:www-data /var/lib/nginx


RUN python manage.py collectstatic --noinput
#RUN python manage.py makemigrations
#RUN python manage.py migrate
RUN #echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'test12345')" | python manage.py shell


#RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

#CMD ["gunicorn", "core.wsgi:application", "-b", "0.0.0.0:8000"]
#CMD ["/app/entrypoint.sh"]
CMD ["bash", "-c", "python manage.py migrate && gunicorn GlobalSensorCloud.wsgi -b 0.0.0.0:8000"]