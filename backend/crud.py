from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
import models
import schemas
from datetime import datetime, timedelta

# --- Schedules ---
def get_schedules(db: Session):
    return db.query(models.Schedule).order_by(models.Schedule.created_at.desc()).all()

def get_schedule(db: Session, schedule_id: int):
    return db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()

def create_schedule(db: Session, schedule: schemas.ScheduleCreate):
    db_schedule = models.Schedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def update_schedule(db: Session, schedule_id: int, schedule: schemas.ScheduleCreate):
    db_obj = get_schedule(db, schedule_id)
    if db_obj:
        for key, value in schedule.dict().items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
    return db_obj

def delete_schedule(db: Session, schedule_id: int):
    db_obj = get_schedule(db, schedule_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
        return True
    return False

def set_schedule_default(db: Session, schedule_id: int):
    schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not schedule: return False
    
    db.query(models.Schedule).update({"is_default": False})
    schedule.is_default = True
    db.commit()
    return True

# --- Event Types ---
def get_event_types(db: Session):
    return db.query(models.EventType).order_by(models.EventType.created_at.desc()).all()

def get_event_type_by_slug(db: Session, slug: str):
    return db.query(models.EventType).filter(models.EventType.slug == slug).first()

def get_event_type(db: Session, event_type_id: int):
    return db.query(models.EventType).filter(models.EventType.id == event_type_id).first()

def create_event_type(db: Session, event_type: schemas.EventTypeCreate):
    evt_dict = event_type.dict()
    if evt_dict.get("schedule_id") is None:
        default_schedule = db.query(models.Schedule).filter(models.Schedule.is_default == True).first()
        if default_schedule:
            evt_dict["schedule_id"] = default_schedule.id
            
    db_event_type = models.EventType(**evt_dict)
    db.add(db_event_type)
    db.commit()
    db.refresh(db_event_type)
    return db_event_type

def update_event_type(db: Session, event_type_id: int, event_type: schemas.EventTypeCreate):
    db_obj = get_event_type(db, event_type_id)
    if db_obj:
        for key, value in event_type.dict().items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
    return db_obj

def delete_event_type(db: Session, event_type_id: int):
    db_obj = get_event_type(db, event_type_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
        return True
    return False

# --- Availability ---
def get_availabilities(db: Session, schedule_id: int = None):
    query = db.query(models.Availability)
    if schedule_id:
        query = query.filter(models.Availability.schedule_id == schedule_id)
    return query.order_by(models.Availability.day_of_week).all()

def set_availabilities(db: Session, schedule_id: int, availabilities: list[schemas.AvailabilityCreate]):
    db.query(models.Availability).filter(models.Availability.schedule_id == schedule_id).delete()
    db_objs = []
    for av in availabilities:
        # Override schedule_id to match the path param
        av_dict = av.dict()
        av_dict["schedule_id"] = schedule_id
        db_objs.append(models.Availability(**av_dict))
        
    db.add_all(db_objs)
    db.commit()
    return get_availabilities(db, schedule_id)

# --- Date Overrides ---
def get_schedule_overrides(db: Session, schedule_id: int):
    return db.query(models.DateOverride).filter(models.DateOverride.schedule_id == schedule_id).order_by(models.DateOverride.date.asc()).all()

def set_schedule_overrides(db: Session, schedule_id: int, overrides: list[schemas.DateOverrideCreate]):
    # Note: Overrides can be bulk-updated by date. For simplicity, we clear ALL overrides for this schedule,
    # or just the dates provided. Best is to clear all and replace with full payload if mapping the whole editor natively.
    # We will assume a complete sync from the frontend of all overrides for this schedule.
    db.query(models.DateOverride).filter(models.DateOverride.schedule_id == schedule_id).delete()
    db_objs = []
    for ov in overrides:
        ov_dict = ov.dict()
        ov_dict["schedule_id"] = schedule_id
        db_objs.append(models.DateOverride(**ov_dict))
        
    db.add_all(db_objs)
    db.commit()
    return get_schedule_overrides(db, schedule_id)

# --- Bookings ---
def get_bookings(db: Session):
    return db.query(models.Booking).order_by(models.Booking.start_time.asc()).all()

def get_booking(db: Session, booking_id: int):
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

def create_booking(db: Session, booking: schemas.BookingCreate):
    event_type = get_event_type(db, booking.event_type_id)
    if not event_type:
        raise ValueError("Event type not found")
        
    end_time = booking.start_time + timedelta(minutes=event_type.duration_minutes)
    
    # Check for double booking considering buffers
    p_start = booking.start_time - timedelta(minutes=event_type.buffer_time_before or 0)
    p_end = end_time + timedelta(minutes=event_type.buffer_time_after or 0)

    start_of_day = p_start.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = p_start.replace(hour=23, minute=59, second=59)

    existing_bookings = db.query(models.Booking).filter(
        models.Booking.status == "confirmed",
        models.Booking.start_time >= start_of_day,
        models.Booking.start_time <= end_of_day
    ).all()

    for b in existing_bookings:
        b_start = b.start_time - timedelta(minutes=(b.event_type.buffer_time_before if b.event_type else 0))
        b_end = b.end_time + timedelta(minutes=(b.event_type.buffer_time_after if b.event_type else 0))
        
        if (p_start < b_end) and (p_end > b_start):
            raise ValueError("Time slot is already booked or violates buffer constraints")
        
    db_booking = models.Booking(
        **booking.dict(),
        end_time=end_time
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def cancel_booking(db: Session, booking_id: int):
    db_booking = get_booking(db, booking_id)
    if db_booking:
        db_booking.status = "cancelled"
        db.commit()
        db.refresh(db_booking)
    return db_booking
