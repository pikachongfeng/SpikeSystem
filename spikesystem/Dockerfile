FROM python:3.6
ADD ./requirements.txt /app/
ADD ./spikesystem.gz /app/
ADD ./django_start.sh /app/
RUN pip3 install -r /app/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
WORKDIR /app/
RUN chmod +x ./django_start.sh
CMD ./django_start.sh

EXPOSE 8000
