FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]


# Build
# docker build -t social-media:v1 .

# Test locally
# docker run -d -p 8080:8080 social-media:v1

# DockerHub
# docker tag social-media:v1 abhi25022004/social-media:v1
# docker push abhi25022004/social-media:v1
