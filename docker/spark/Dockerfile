FROM bitnami/spark:3.3.0

USER root

# Install Python dependencies
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --upgrade pip

# Install curl and Poetry
# RUN apt-get update && \
#     apt-get install -y gcc libpq-dev curl && \
#     pip install --no-cache-dir --upgrade pip && \
#     curl -sSL https://install.python-poetry.org | python3 -

# # Set up the consumer application
# WORKDIR /app
# COPY consumer/pyproject.toml consumer/poetry.lock ./
# RUN poetry config virtualenvs.create false && \
#     poetry install --no-dev

# COPY consumer/consumer /app/consumer

# ENV SPARK_MASTER_URL=spark://spark-master:7077