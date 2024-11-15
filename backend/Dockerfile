FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
COPY fonts/ /usr/share/fonts/truetype/
CMD ["gunicorn", "--bind", ":$PORT", "main:app"]