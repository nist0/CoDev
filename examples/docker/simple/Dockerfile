FROM python:3.11.5-slim-bullseye AS runtime
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src
RUN groupadd --gid 1000 app && useradd --uid 1000 --gid 1000 --no-create-home app
USER app
CMD ["python", "src/main.py"]
