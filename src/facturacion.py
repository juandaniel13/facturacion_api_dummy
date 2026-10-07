import uvicorn
from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import List

# 1. Definición de la aplicación FastAPI
app = FastAPI(
    title="API Dummy de Facturación",
    description="API de prueba para integración con Watsonx Assistant",
    version="1.0.0"
)

# 2. Definición del modelo de datos de la Factura
class Factura(BaseModel):
    mes_facturado: str
    valor_total_a_pagar: float
    fecha_limite_pago: str
    referencia_pago: str

# 3. Base de datos simulada (Diccionario en memoria)
db_dummy = {
    "12345": [
        {
            "mes_facturado": "Septiembre 2026",
            "valor_total_a_pagar": 125000.0,
            "fecha_limite_pago": "2026-10-15",
            "referencia_pago": "REF-9876501"
        },
        {
            "mes_facturado": "Octubre 2026",
            "valor_total_a_pagar": 125000.0,
            "fecha_limite_pago": "2026-11-15",
            "referencia_pago": "REF-9876502"
        }
    ],
    "98765": [
        {
            "mes_facturado": "Octubre 2026",
            "valor_total_a_pagar": 45000.0,
            "fecha_limite_pago": "2026-10-20",
            "referencia_pago": "REF-334455"
        }
    ]
}

# 4. Definición del Endpoint
@app.get("/api/v1/facturas/{usuario_id}", response_model=List[Factura], summary="Obtener facturas del usuario")
def listar_facturas(
    usuario_id: str = Path(..., description="ID o documento del usuario a consultar")
):
    """
    Retorna la lista de facturas pendientes para el usuario especificado.
    Si el usuario no tiene facturas o no existe, retorna una lista vacía.
    """
    return db_dummy.get(usuario_id, [])

# 5. Arranque del servidor embebido
if __name__ == "__main__":
    print("Iniciando API Dummy en http://localhost:8000")
    print("Documentación Swagger: http://localhost:8000/docs")
    print("OpenAPI JSON (Para Watsonx): http://localhost:8000/openapi.json")
    uvicorn.run(app, host="0.0.0.0", port=8000)