from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List
from supabase_client import supabase

app = FastAPI(title="Chinook Invoice Backend - Practica 6")

# Permite que el frontend Java (otro origen/puerto) consuma la API sin bloqueos CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class InvoiceHeader(BaseModel):
    invoice_id: int
    customer_id: int
    invoice_date: str
    billing_address: str
    billing_city: str
    billing_state: str
    billing_country: str
    billing_postal_code: str
    total: float


@app.get("/health")
def health():
    """Endpoint de health check para el monitor del frontend."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.post("/invoice")
def create_invoice(header: InvoiceHeader):
    """Graba la cabecera de la factura en la tabla 'invoice' YA EXISTENTE en Supabase
    (proyecto practica6, esquema Chinook creado en la práctica anterior)."""
    try:
        data = header.dict()
        response = supabase.table("invoice").insert(data).execute()
        if not response.data:
            raise HTTPException(status_code=500, detail="No se pudo insertar en Supabase")
        return {"status": "ok", "data": response.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/invoice/bulk")
def create_invoices_bulk(headers: List[InvoiceHeader]):
    """Sincronización masiva de cabeceras pendientes (usa upsert por invoice_id
    para que sea idempotente, tal como pide RNF-07)."""
    try:
        data = [h.dict() for h in headers]
        response = supabase.table("invoice").upsert(data, on_conflict="invoice_id").execute()
        return {"status": "ok", "inserted": len(response.data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
