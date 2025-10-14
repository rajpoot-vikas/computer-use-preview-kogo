# ---------- Build Stage ----------
FROM python:3.11-slim-bullseye AS browsey-server-build
LABEL stage=builder

# Upgrade system packages and pip to address vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Set working directory
WORKDIR /app

RUN mkdir -p /app/logs

# Copy requirements and install dependencies
COPY services/server/requirements.txt /app/requirements.txt

# COPY ./services/library/*.whl ./

RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY services/server/library/kogoos_common-0.1.0-py3-none-any.whl /app/

RUN pip3 install --no-cache-dir /app/kogoos_common-0.1.0-py3-none-any.whl


COPY services/server/workflows /app/workflows
RUN pip3 install --no-cache-dir -e /app/workflows

COPY services/server/common /app/common
RUN pip3 install --no-cache-dir -e /app/common

# ---------- Production Stage ----------
FROM python:3.11-slim-bullseye AS browsey-server
LABEL stage=prod ai.kogoos.service=browsey-server

# Upgrade system packages to address vulnerabilities in the production image
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get dist-upgrade -y && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


ENV ACCESS_LOG=${ACCESS_LOG:-/proc/1/fd/1}
ENV ERROR_LOG=${ERROR_LOG:-/proc/1/fd/2}
ENV GIT_PYTHON_REFRESH=quiet

# Install system tools and dependencies required by Playwright and Xvfb, then create app user and set permissions
RUN apt-get update && apt-get install -y \
    curl libasound2 libnss3 libx11-xcb1 libxcb-dri3-0 libxss1 net-tools vim x11-utils xvfb \
    libgbm1 libxkbcommon-x11-0 libgtk-3-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libpango-1.0-0 fonts-liberation libatk-bridge2.0-0 libdrm2 libatspi2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && adduser --system -u 1001 --home /app kogoos \
    && mkdir -p /app \
    && chown -R 1001:0 /app \
    && chmod -R g+rwX /app

# Copy installed Python dependencies from build stage
COPY --from=browsey-server-build  /usr/local /usr/local

# COPY --from=browsey-server-build /app/.local /app/.local
# ENV PATH=/root/.local:/root/.local/bin:/app/.local:/app/.local/bin:$PATH

# Set browser install path for Playwright and install using patchright
ENV PLAYWRIGHT_BROWSERS_PATH=/app/.cache/ms-playwright
RUN mkdir -p ${PLAYWRIGHT_BROWSERS_PATH} && \
    chmod -R 777 ${PLAYWRIGHT_BROWSERS_PATH} && \
    apt-get update --allow-releaseinfo-change && \
    apt-get install -y --allow-unauthenticated ca-certificates && \
    apt-get update && \
    patchright install chromium --with-deps || \
    playwright install chromium --with-deps

# Create the .cache directory and set permissions
RUN mkdir -p /app/.cache/mesa_shader_cache && \
    chmod -R 777 /app/.cache

# Create browseruse profiles directory
RUN mkdir -p /app/.config/browseruse/profiles/default && \
    chmod -R 777 /app/.config

# Set working directory and switch to non-root user
WORKDIR /app
USER kogoos

# Copy application source code 
COPY --chown=1001:0 services/server/main.py /app
COPY --chown=1001:0 services/server/api /app/api
COPY --chown=1001:0 services/server/workflows /app/workflows
COPY --chown=1001:0 services/server/common /app/common
COPY --chown=1001:0 services/server/core /app/core
COPY --chown=1001:0 services/server/static /app/static
# COPY --chown=1001:0 services/server/.env /app/.env 

EXPOSE 5010

# CMD ["bash", "-c", "Xvfb :99 -screen 0 1024x768x16 & export DISPLAY=:99 && python main.py"] 
CMD ["bash", "-c", "Xvfb :99 -screen 0 1024x768x16 & export DISPLAY=:99 && python main.py"] 
# CMD ["python", "main.py"] 
