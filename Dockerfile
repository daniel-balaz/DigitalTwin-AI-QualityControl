FROM python

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY main.py .
COPY .env .

EXPOSE 8000

CMD ["python", "-u", "main.py"]