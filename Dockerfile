FROM python:3.8

WORKDIR /sht3x_exporter_raspberry
COPY . .

RUN pip install -e .

EXPOSE 9892

CMD ["pserve", "/sht3x_exporter_raspberry/production.ini"]