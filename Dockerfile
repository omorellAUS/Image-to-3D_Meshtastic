FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-runtime

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/VAST-AI-Research/TripoSR.git /TripoSR
ENV PYTHONPATH="/TripoSR:${PYTHONPATH}"

COPY . .

EXPOSE 7860

CMD ["python", "app/main.py"]
