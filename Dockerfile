FROM    finsenty/alpine-python:4.0

WORKDIR /mysite
#ONBUILD
COPY main.py /mysite
#COPY gunicorn.conf.py /mysite
COPY templates /mysite/templates
COPY static /mysite/static


EXPOSE 80
CMD ["python", "/mysite/main.py"]

#ADD mysite.wsgi /var/www/mysite/
#CMD service apache2 start && tail -F /var/log/apache2/error.log
