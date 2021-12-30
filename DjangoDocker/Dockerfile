FROM python:3

RUN python -m pip install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /BankApp
COPY . .

RUN pip install -r requirements.txt
WORKDIR ./BankApp

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]