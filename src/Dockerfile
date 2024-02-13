FROM python:3.11

RUN apt update
RUN mkdir -p /usr/code/myeshop

WORKDIR /usr/code/myeshop

EXPOSE 80

COPY . .

RUN pip install -e .

CMD ["python", "./eshop/manage.py", "runserver", "--noreload", "0.0.0.0:80" ]