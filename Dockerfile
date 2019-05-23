FROM  docker.io/alpine:latest

ENV TZ "Asia/Shanghai"

RUN apk update \
        && apk upgrade \
        && apk add --no-cache bash \
        bash-doc \
        bash-completion \
        && rm -rf /var/cache/apk/* \
        && /bin/bash

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

RUN apk add --no-cache gcc
RUN apk update \
        && apk add --no-cache python3-lxml
        

RUN pip install flask -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
RUN pip install mysql-connector -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
RUN pip install lxml -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

#RUN apk add --update \
#  && pip install Flask \
#  && pip install mysql-connector \
#  && pip install lxml \
#  && rm -rf /var/cache/apk/*

#RUN apk add --no-cache gcc
#RUN pip3 install gunicorn
#RUN pip3 install gevent

#RUN sed '$a http://dl-cdn.alpinelinux.org/alpine/edge/community' /etc/apk/#repositories

#RUN apk update
#RUN apk add apache2
#RUN apt-get install -y vim
#RUN apk add apache2-mod-wsgi
#RUN sed -i 's/80/5000/' /etc/apache2/ports.conf


#ADD flaskapp.wsgi /var/www/mysite/
#ADD flaskapp.conf /etc/apache2/sites-available/
#RUN a2dissite flaskapp.conf

#EXPOSE 5000

RUN pip3 install PyYAML==3.13 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
RUN pip3 install jsonpickle -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
RUN pip install lxml -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

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
