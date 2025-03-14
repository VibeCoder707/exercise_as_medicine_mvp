def list_all_patients(db: Session) -> List[models.Patient]:
    """List all patients in the database"""
    return db.query(models.Patient).all()