FROM alpine
RUN apk --update add python py-pip bash ca-certificates \
    && pip install -U pip certifi
ADD requirements.txt /helpbot/requirements.txt
WORKDIR /helpbot
RUN pip install -r requirements.txt
COPY rtmbot.conf.template /helpbot/rtmbot.conf
ADD . /helpbot
CMD ["./start.sh"]
