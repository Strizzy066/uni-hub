FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Update the package lists for the apt package manager
RUN apt-get update

# Install system dependencies:
# - libpq-dev provides PostgreSQL client libraries
# - python3-dev includes Python headers needed for building some Python packages
# - gcc is the GNU Compiler Collection for compiling C code
RUN apt-get install libpq-dev python3-dev gcc -y

# Create a new group 'app' and a non-root system user 'app' belonging to that group.
# RUN addgroup app && adduser --system --ingroup app app

# Set the working directory to /app within the container.
WORKDIR /app

# Copy the requirements.txt file to the current working directory in the container.
COPY requirements.txt .

# Upgrade pip and install the Python dependencies listed in requirements.txt.
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code into the working directory.
COPY . .

# Give executable permission to the entrypoint script so it can be run when the container starts.
RUN chmod +x ./entrypoint.sh

# Switch the context to the non-root user 'app' for following commands, improving security.
# USER app

# Expose port 8000 to allow external access to the application.
EXPOSE 8000

# Entrypoint script
ENTRYPOINT ["./entrypoint.sh"]