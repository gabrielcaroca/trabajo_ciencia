"""
Main execution orchestrator for the Pitchfork Reviews ETL pipeline.
Handles SQLite extraction via JOINs, and ML pipeline application.
"""

import pandas as pd
import sqlite3
from pathlib import Path
import traceback

try:
    from src.audit import audit_data
    from src.optimization import optimize_memory
except ImportError:
    audit_data = lambda *args: True
    optimize_memory = lambda df: df

from src.pipeline import build_pitchfork_pipeline

def extract_from_sqlite(db_path):
    """Connects to SQLite and performs SQL joins to create the master dataset."""
    conn = sqlite3.connect(db_path)
    
    # EXTRACCIÓN OPTIMIZADA: Dejamos que el motor SQL haga los cruces en lugar de Pandas
    query = """
    SELECT 
        r.reviewid, r.score, r.url, r.pub_year,
        g.genre,
        l.label,
        c.content,
        a.artist
    FROM reviews r
    LEFT JOIN genres g ON r.reviewid = g.reviewid
    LEFT JOIN labels l ON r.reviewid = l.reviewid
    LEFT JOIN content c ON r.reviewid = c.reviewid
    LEFT JOIN artists a ON r.reviewid = a.reviewid
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Limpieza inicial de duplicados por llave primaria
    return df.drop_duplicates(subset=['reviewid']).copy()

def main():
    print("="*60)
    print("🎸 PIPELINE DE DATOS: PITCHFORK MUSIC REVIEWS")
    print("="*60)

    try:
        # 1. Extracción
        print("\n📥 Fase 1: Conexión y extracción optimizada desde SQLite")
        db_path = Path("data/raw/database.sqlite")
        
        if not db_path.exists():
            print(f"❌ Error: No se encontró la base de datos en {db_path}")
            return
            
        df_raw = extract_from_sqlite(db_path)
        print(f"✅ Extracción exitosa: {df_raw.shape[0]} reseñas cargadas.")

        # Separamos la variable objetivo (El puntaje de la reseña)
        target_col = 'score'
        y = df_raw[target_col] if target_col in df_raw.columns else None
        X = df_raw.drop(columns=[target_col], errors='ignore')

        # 2. Optimización
        print("\n⚙️  Fase 2: Optimización de memoria")
        X_opt = optimize_memory(X)

        # 3. Aplicar Pipeline
        print("\n🏗️  Fase 3: Construyendo y aplicando el pipeline...")
        pipeline = build_pitchfork_pipeline()
        
        # Procesamiento
        X_processed = pipeline.fit_transform(X_opt)
        
        # Limpieza de nombres de columnas de Scikit-Learn
        X_processed.columns = [str(col).replace('num__', '').replace('cat__', '') for col in X_processed.columns]
        
        # Reacoplamos el target (Score) al dataset final
        if y is not None:
            X_processed[target_col] = y

        # 4. Guardado
        print("\n💾 Fase 4: Guardado de dataset")
        processed_dir = Path("data/processed")
        processed_dir.mkdir(parents=True, exist_ok=True)
        output_path = processed_dir / "pitchfork_processed.csv"

        X_processed.to_csv(output_path, index=False)
        
        print("\n" + "="*60)
        print("✅ PIPELINE COMPLETADO EXITOSAMENTE")
        print("="*60)
        print(f"📊 Dimensiones finales: {X_processed.shape[0]} filas × {X_processed.shape[1]} columnas")
        print(f"📁 Guardado en: {output_path}")

    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()