FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./
COPY prompts/ ./prompts/

ENV PYTHONUNBUFFERED=1 AWS_REGION=us-west-2 AGENT_STEP=3
EXPOSE 8080
CMD ["python", "agent.py"]
