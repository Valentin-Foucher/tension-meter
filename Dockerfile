FROM python:3.8.6

ENV PYTHONPATH "${PYTHONPATH}:/var/:/var/app"

RUN pip install pipenv
RUN mkdir -p /var/app

WORKDIR /var/app

COPY tension_meter tension_meter
COPY Pipfile Pipfile.lock run.py ./

RUN pipenv install --system --deploy

ENTRYPOINT ["python", "run.py"]