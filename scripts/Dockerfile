FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y wget unzip

RUN wget https://github.com/vdcsolutions/free-proxy-api/archive/refs/heads/master.zip &&\
    unzip master.zip &&\
    mv free-proxy-api-master/* /app/
#    rm master.zip

COPY config.ini /app/

RUN wget https://github.com/mertguvencli/http-proxy-list/archive/refs/heads/main.zip &&\
    unzip main.zip &&\
    ls -la &&\
    mkdir /app/http-proxy-list && \
    mv http-proxy-list-main/* /app/http-proxy-list

RUN python -m pip install --upgrade pip &&\
    python -m pip install --no-cache-dir -r /app/http-proxy-list/requirements.txt &&\
    python -m pip install --no-cache-dir -r /app/requirements.txt

RUN chmod +x /app/run.sh > logs.txt

EXPOSE 8000

CMD ["/app/run.sh"]
