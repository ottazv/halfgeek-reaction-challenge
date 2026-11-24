FROM python:3.12-slim
WORKDIR /app
COPY hy2.sh .
RUN chmod +x hy2.sh
EXPOSE 8080
CMD ["bash", "hy2.sh"]




