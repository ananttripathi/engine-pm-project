# Dockerfile for Engine Predictive Maintenance - Model Deployment
# Final submission: Define a Dockerfile and list all configurations

# Base image: official Python slim
FROM python:3.10-slim

# Configuration: working directory
WORKDIR /app

# Configuration: environment variables (HF token injected at run time)
ENV PYTHONUNBUFFERED=1

# Configuration: install system dependencies if needed (none required for this app)
# RUN apt-get update && apt-get install -y --no-install-recommends ...

# Configuration: copy dependencies file
COPY requirements.txt .

# Configuration: install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Configuration: copy application code
COPY app.py .

# Configuration: expose Streamlit default port (HF Spaces uses 7860 or 8501)
EXPOSE 8501

# Configuration: run the Streamlit app
# --server.port and --server.address for container compatibility
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
