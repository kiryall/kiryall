# Sefer OCR Renamer (MVP)

Локальное приложение для экспедиционной обработки фото:
- детекция таблички (`YOLO OBB`),
- OCR номера (`PaddleOCR`),
- группировка/суффиксы,
- пакетное переименование,
- отчёт и UI на Streamlit.

## Ключевые особенности
- Полностью офлайн (без облачных API).
- Логика 3 групп результата:
  1. high confidence — переименование без флага;
  2. low confidence — переименование с `!`;
  3. no detection/OCR — без переименования, с `!`.
- Настраиваемый `confidence_threshold` в CLI/UI.
- Docker-first: можно собрать/скачать один образ и запускать локально на любом компьютере с Docker.

## Структура данных для запуска
```text
safer/
  data/
    input/      # сюда кладём JPG
    output/     # сюда пишутся результаты
```

## Запуск через Docker (рекомендуется)
### 1) Собрать образ один раз
```bash
cd safer
docker build -t safer:latest .
```

### 2) UI-режим (Streamlit)
```bash
docker run --rm -it \
  -p 8501:8501 \
  -e APP_MODE=streamlit \
  -v $(pwd)/data:/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/output:/app/output \
  safer:latest
```
Открыть: `http://localhost:8501`.

### 3) CLI-режим
```bash
docker run --rm -it \
  -e APP_MODE=cli \
  -v $(pwd)/data:/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/output:/app/output \
  safer:latest
```
По умолчанию CLI ждёт вход в `/data/input` и пишет в `/data/output`.

## Запуск через docker compose
```bash
cd safer
docker compose up --build safer-ui
# или
mkdir -p data/input data/output
docker compose --profile cli up safer-cli
```

## Локальный запуск без Docker
```bash
cd safer
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
python scripts/run_pipeline.py --input-dir /path/to/photos --output-dir output --dry-run
streamlit run ui/streamlit_app.py
```

## Примечания по моделям
- Путь по умолчанию к детектору: `models/yolo/v1/best.pt`.
- Для OBB используется интерфейс `ultralytics.YOLO`; если модель недоступна, pipeline возвращает флаг `no_detection`.
- Для полностью автономной работы положите веса модели в `models/` до сборки образа или примонтируйте `./models:/app/models`.

## Формат отчёта
`output/results.csv`
- `input_name`
- `output_name`
- `plate_text`
- `confidence`
- `status`
- `group_id`
- `reason`
