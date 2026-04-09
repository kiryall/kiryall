from pathlib import Path

import pandas as pd
import streamlit as st

from src.pipeline.batch_processor import process_batch

st.set_page_config(page_title="Sefer Renamer", layout="wide")
st.title("Sefer: OCR-переименование полевых фото")

input_dir = st.text_input("Папка с фото", value="")
output_dir = st.text_input("Папка результата", value="output")
threshold = st.slider("Порог confidence для auto-OK", min_value=0.5, max_value=0.99, value=0.9)
dry_run = st.checkbox("Dry run (без физического переименования)", value=True)

if st.button("Запустить pipeline"):
    if not input_dir:
        st.error("Укажите папку с фото")
    else:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        results = process_batch(input_dir, output_dir, threshold, dry_run)
        df = pd.DataFrame([r.__dict__ for r in results])
        st.success(f"Обработано: {len(df)}")
        st.dataframe(df)
        csv_path = Path(output_dir) / "results.csv"
        st.info(f"CSV сохранён: {csv_path}")
