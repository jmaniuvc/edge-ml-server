FROM python:3.10.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5004

CMD ["python", "app.py"]