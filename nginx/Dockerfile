FROM nginx
COPY ./dist/ /usr/share/nginx/html/
VOLUME /var/log/nginx
ADD ./conf /etc/nginx
EXPOSE 80
