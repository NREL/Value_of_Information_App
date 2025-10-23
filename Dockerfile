# ===== BUILD STAGE =====
ARG BASE_IMAGE_TAG

FROM python:${BASE_IMAGE_TAG:-3.12.2-bookworm-slim} AS build

# Create non-root user and group
ARG UID=1000
ARG GID=1000

# Install dependencies for building Python packages
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get clean \
 && groupadd -g "${GID}" python \
 && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python

# Set up environment
ENV PYTHONUNBUFFERED=1 \
    PATH="/home/python/.local/bin:$PATH"

WORKDIR /app

# Change ownership to non-root user before copying
RUN chown python:python /app

# Switch to non-root user
USER python

# Copy only files needed for production
COPY --chown=python:python requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=python:python app.py ./
COPY --chown=python:python Bayesian_Modeling.py ./
COPY --chown=python:python Naive_Bayes.py ./
COPY --chown=python:python GEOPHIRES_X.py ./
COPY --chown=python:python User_input.py ./
COPY --chown=python:python VOI.py ./
# Copy required image assets if used at runtime
COPY --chown=python:python dtree.png ./

# ===== FINAL IMAGE =====
FROM python:${BASE_IMAGE_TAG:-3.12-slim}

ARG UID=1000
ARG GID=1000

RUN groupadd -g "${GID}" python \
 && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PATH="/home/python/.local/bin:$PATH"

# Switch to non-root user
USER python

# Copy installed Python packages from build stage
COPY --from=build /home/python/.local /home/python/.local
# Copy application code
COPY --from=build /app /app

# Expose default Streamlit port
EXPOSE 8501

# Run Streamlit in production mode
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]
