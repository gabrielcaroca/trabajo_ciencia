import pandas as pd
import numpy as np

def optimize_memory(df):
    """
    Reduce el uso de memoria de un DataFrame mediante el casteo de tipos numericos.
    Compara los limites de cada columna para asignar el tipo de dato mas pequeño posible.
    """
    try:
        # Calcular memoria inicial
        original_mem = df.memory_usage(deep=True).sum() / 1024**2
        print(f"Memoria original: {original_mem:.2f} MB")
        
        df_opt = df.copy()
        
        # Iterar sobre columnas numericas (int y float)
        for col in df_opt.select_dtypes(include=['int', 'float', 'number']).columns:
            try:
                c_min = df_opt[col].min()
                c_max = df_opt[col].max()
                col_type = df_opt[col].dtype
                
                # Optimizacion de Enteros
                if str(col_type).startswith('int'):
                    if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                        df_opt[col] = df_opt[col].astype(np.int8)
                    elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                        df_opt[col] = df_opt[col].astype(np.int16)
                    elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                        df_opt[col] = df_opt[col].astype(np.int32)
                
                # Optimizacion de Flotantes
                elif str(col_type).startswith('float'):
                    if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                        df_opt[col] = df_opt[col].astype(np.float32)
                        
            except Exception as e:
                print(f"No se pudo optimizar la columna {col}: {e}")
                continue

        # Calcular memoria final
        final_mem = df_opt.memory_usage(deep=True).sum() / 1024**2
        ahorro = 100 * (original_mem - final_mem) / original_mem
        
        print(f"Memoria optimizada: {final_mem:.2f} MB")
        print(f"Ahorro total: {ahorro:.2f}%")
        
        return df_opt

    except Exception as e:
        print(f"Error general en la optimizacion: {e}")
        return df