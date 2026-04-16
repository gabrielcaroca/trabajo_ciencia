import pandas as pd
from pathlib import Path
from src.audit import audit_data
from src.optimization import optimize_memory
from src.pipeline import build_pitchfork_pipeline
import sqlite3
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():

    print("--- Starting Data Pipeline ---\n")

    try:
        # 1. Ruta
        db_path = Path("data/raw/database.sqlite")

        # 2. Auditoría
        if not audit_data(db_path):
            print("\nPipeline stopped due to audit failure.")
            return

        # 3. Carga SQLite 
        print("\nLoading raw data...")
        conn = sqlite3.connect(db_path)
        df_raw = pd.read_sql_query("SELECT * FROM reviews", conn)
        conn.close()

        # 4. Optimización
        print("\nOptimizing memory...")
        df_opt = optimize_memory(df_raw)

        # 5. Pipeline
        print("\nBuilding and applying preprocessing pipeline...")
        pipeline = build_pitchfork_pipeline()

        processed_matrix = pipeline.fit_transform(df_opt)

        # 6. Guardado
        print("\nSaving processed dataset...")

        df_processed = pd.DataFrame(processed_matrix)

        processed_dir = Path("data/processed")
        processed_dir.mkdir(parents=True, exist_ok=True)

        output_path = processed_dir / "processed_data.csv"
        df_processed.to_csv(output_path, index=False)

        print(f"SUCCESS: Processed dataset saved at {output_path}")
        print(f"Final dimensions: {df_processed.shape}")

    except Exception as e:
        print(f"\nFATAL ERROR: {e}")

if __name__ == "__main__":
    main()