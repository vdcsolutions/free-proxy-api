FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y wget unzip

RUN wget https://github.com/vdcsolutions/free-proxy-api/archive/refs/heads/master.zip &&\
    unzip master.zip &&\
    mv free-proxy-api-master/* /app/ &&\
    rm master.zip

RUN wget https://github.com/mertguvencli/http-proxy-list/archive/refs/heads/main.zip &&\
    unzip main.zip &&\
    ls -la &&\
    mkdir /app/http_proxy_list && \
    mv http-proxy-list-main/* /app/http_proxy_list
#    rm main.zip



RUN python -m venv /opt/venv &&\
    /opt/venv/bin/pip install --upgrade pip &&\
    /opt/venv/bin/pip install --no-cache-dir -r /app/http_proxy_list/requirements.txt &&\
    /opt/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

EXPOSE 8000

CMD ["/app/run.sh"]
