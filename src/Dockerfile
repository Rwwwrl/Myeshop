# build stage
FROM python:3.11 as build

RUN apt update
RUN mkdir -p /usr/code/myeshop

WORKDIR /usr/code/myeshop

EXPOSE 80

COPY . .

RUN pip install -e .


# build for run pytest stage
FROM build as build_for_run_pytest

RUN pip install -r requirements/for_run_tests.txt