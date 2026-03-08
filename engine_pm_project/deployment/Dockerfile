# Dockerfile for Engine Predictive Maintenance - Model Deployment
# Final submission: Define a Dockerfile and list all configurations
# Pinned base image for better HF build cache and faster rebuilds

FROM python:3.10.14-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Install dependencies first (layer cached when requirements unchanged)
# Constrain numpy<2 so joblib can load sklearn models (BitGenerator compatibility)
COPY requirements.txt constraints.txt ./
RUN pip install --no-cache-dir -r requirements.txt -c constraints.txt

# Application code last (changes most often)
COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

