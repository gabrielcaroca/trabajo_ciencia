import hashlib
import json
import os
from pathlib import Path


def generate_file_hash(file_path):
    """
    Genera hash SHA-256 del archivo en bloques (eficiente en memoria)
    """
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except IOError as e:
        print(f"Error al leer archivo: {e}")
        return None


def audit_data(db_path):
    """
    Verifica integridad del archivo comparando con metadata.json
    """
    try:
        target_file = Path(db_path)
        metadata_path = target_file.parent / "metadata.json"

        # 1. Verificar existencia del archivo
        if not target_file.exists():
            print(f"Error: no existe {db_path}")
            return False

        print("\n--- AUDITORIA DE DATOS ---")
        print(f"Archivo: {target_file.name}")

        # 2. Generar hash
        calculated_hash = generate_file_hash(target_file)
        if not calculated_hash:
            return False

        print(f"SHA-256: {calculated_hash}")

        # 3. Si existe metadata → comparar
        if metadata_path.exists():
            try:
                with open(metadata_path, "r") as f:
                    saved_metadata = json.load(f)
            except json.JSONDecodeError:
                print("Metadata corrupta. Se regenerará.")
                metadata_path.unlink()  # borrar archivo corrupto
                return audit_data(db_path)

            if saved_metadata.get("hash_sha256") == calculated_hash:
                print("Integridad verificada")
                return True
            else:
                print("ALERTA: el archivo fue modificado")
                return False

        # 4. Si no existe metadata → crearla
        else:
            new_metadata = {
                "file": target_file.name,
                "hash_sha256": calculated_hash,
                "size_mb": round(os.path.getsize(target_file) / (1024 * 1024), 2)
            }

            with open(metadata_path, "w") as f:
                json.dump(new_metadata, f, indent=4)

            print("Metadata creada correctamente")
            return True

    except Exception as e:
        print(f"Error en auditoria: {e}")
        return False