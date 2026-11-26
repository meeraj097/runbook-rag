FROM python:3.12-slim AS build
WORKDIR /build
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=build /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels fastapi uvicorn && rm -rf /wheels
COPY src src
COPY runbooks runbooks
USER 65534:65534
EXPOSE 8000
CMD ["uvicorn","src.app:app","--host","0.0.0.0","--port","8000"]
