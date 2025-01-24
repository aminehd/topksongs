FROM python:3.10-slim-buster

WORKDIR /app
# Install system dependencies including git
RUN apt-get update && \
    apt-get install -y gcc libpq-dev procps openjdk-11-jdk git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Java and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-11-jdk \
        wget \
        procps \
    && rm -rf /var/lib/apt/lists/*

# Set up environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_VERSION=3.3.0
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:${SPARK_HOME}/bin
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH

# Download and set up Spark
RUN wget --no-verbose https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    tar -xf spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop3 ${SPARK_HOME} && \
    rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

# Download additional JARs needed for Kafka integration
RUN cd ${SPARK_HOME}/jars && \
    wget --no-verbose https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/${SPARK_VERSION}/spark-sql-kafka-0-10_2.12-${SPARK_VERSION}.jar && \
    wget --no-verbose https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.8.1/kafka-clients-2.8.1.jar && \
    wget --no-verbose https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar && \
    wget --no-verbose https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/${SPARK_VERSION}/spark-token-provider-kafka-0-10_2.12-${SPARK_VERSION}.jar


# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#     openjdk-11-jdk \
#     wget \
#     && rm -rf /var/lib/apt/lists/*

    
# # Set up Java environment
# ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
# ENV PATH $PATH:$JAVA_HOME/bin


# # Set up environment variables
# ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
# ENV SPARK_VERSION=3.3.0
# ENV SPARK_HOME=/opt/spark
# ENV PATH=$PATH:${SPARK_HOME}/bin

# RUN wget -q https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
#     tar -xzf spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
#     mv spark-${SPARK_VERSION}-bin-hadoop3 ${SPARK_HOME} && \
#     rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

# # Download Spark Kafka package
# RUN wget -q -P ${SPARK_HOME}/jars/ https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/${SPARK_VERSION}/spark-sql-kafka-0-10_2.12-${SPARK_VERSION}.jar && \
#     wget -q -P ${SPARK_HOME}/jars/ https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar && \
#     wget -q -P ${SPARK_HOME}/jars/ https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/${SPARK_VERSION}/spark-token-provider-kafka-0-10_2.12-${SPARK_VERSION}.jar

COPY poetry.lock pyproject.toml ./

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    pip install --no-cache-dir --upgrade pip && \
    pip install poetry

COPY . .

RUN poetry install --no-interaction --no-ansi 

ENV SPARK_MASTER_URL=spark://spark-master:7077

# Download Spark Kafka package

CMD ["poetry", "run", "python", "consumer/spark_processor.py"]


# # Set up the consumer application

