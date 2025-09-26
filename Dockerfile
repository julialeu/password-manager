# --- Python image ---
FROM python:3.13-slim

# Work directory
WORKDIR /app

# --- Install dependencies ---
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# --- Copy the app code ---
COPY ./app /app/app

# --- Expose port  and run the app ---
# EXPOSE 8000
EXPOSE 10000

# Command to  run the app once the container is running
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]