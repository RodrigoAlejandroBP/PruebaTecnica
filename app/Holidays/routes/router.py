from .router import holidays_router 


@holidays_router.get("/2")
async def get_products():
    return {"message": "Get all products"}


@holidays_router.get("/holidays/{init_date}")
def obtener_feriado_por_fecha(fecha: date, db: Session = Depends(get_db)):
    feriado = db.query(Holiday).filter(Holiday.fecha == fecha).first()
    if Holiday is None:
        raise HTTPException(status_code=404, detail="Feriado no encontrado")
    return Holiday

@holidays_router.get("/holidays/between/{init_date}/{end_date}")
def obtener_holidays_entre_fechas(fecha_inicio: date, fecha_fin: date, db: Session = Depends(get_db)):
    holidays = db.query(Holiday).filter(Holiday.fecha.between(fecha_inicio, fecha_fin)).all()
    return holidays

# ... otros endpoints para crear, actualizar y eliminar holidays