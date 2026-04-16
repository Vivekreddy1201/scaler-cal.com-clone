from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from datetime import datetime, date, timedelta, time
from fastapi.middleware.cors import CORSMiddleware

import models, schemas, crud
from database import engine, get_db

# Create all tables (In production use Alembic)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Scheduling Platform API")

@app.on_event("startup")
def startup_event():
    db = next(get_db())
    
    # Primitive migration: Try to add columns if they don't exist
    try:
        db.execute(text("ALTER TABLE event_types ADD COLUMN schedule_id INTEGER REFERENCES schedules(id)"))
        db.commit()
    except Exception:
        db.rollback()

    try:
        db.execute(text("ALTER TABLE availabilities ADD COLUMN schedule_id INTEGER REFERENCES schedules(id)"))
        db.commit()
    except Exception:
        db.rollback()

    try:
        db.execute(text("ALTER TABLE event_types ADD COLUMN buffer_time_before INTEGER DEFAULT 0"))
        db.commit()
    except Exception:
        db.rollback()

    try:
        db.execute(text("ALTER TABLE event_types ADD COLUMN buffer_time_after INTEGER DEFAULT 0"))
        db.commit()
    except Exception:
        db.rollback()

    try:
        db.execute(text("ALTER TABLE schedules ADD COLUMN is_default BOOLEAN DEFAULT FALSE"))
        db.commit()
    except Exception:
        db.rollback()

    # Create default schedule if none exists
    first_schedule = db.query(models.Schedule).first()
    if not first_schedule:
        first_schedule = models.Schedule(name="Working Hours", timezone="UTC", is_default=True)
        db.add(first_schedule)
        db.commit()
        db.refresh(first_schedule)
    else:
        # Guarantee at least one is default
        has_default = db.query(models.Schedule).filter(models.Schedule.is_default == True).first()
        if not has_default:
            first_schedule.is_default = True
            db.commit()
        
    # Update existing nulls
    db.execute(text(f"UPDATE event_types SET schedule_id = {first_schedule.id} WHERE schedule_id IS NULL"))
    db.execute(text(f"UPDATE availabilities SET schedule_id = {first_schedule.id} WHERE schedule_id IS NULL"))
    db.commit()

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Event Types Endpoints ---
@app.get("/api/event-types", response_model=List[schemas.EventTypeResponse])
def read_event_types(db: Session = Depends(get_db)):
    return crud.get_event_types(db)

@app.get("/api/event-types/{event_id}", response_model=schemas.EventTypeResponse)
def read_event_type(event_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_event_type(db, event_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Event type not found")
    return db_obj

@app.post("/api/event-types", response_model=schemas.EventTypeResponse)
def create_event_type(event_type: schemas.EventTypeCreate, db: Session = Depends(get_db)):
    if crud.get_event_type_by_slug(db, slug=event_type.slug):
        raise HTTPException(status_code=400, detail="an event type with this url already exists")
    return crud.create_event_type(db=db, event_type=event_type)

@app.put("/api/event-types/{event_id}", response_model=schemas.EventTypeResponse)
def update_event_type(event_id: int, event_type: schemas.EventTypeCreate, db: Session = Depends(get_db)):
    db_obj = crud.update_event_type(db, event_id, event_type)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Event type not found")
    return db_obj

@app.delete("/api/event-types/{event_id}")
def delete_event_type(event_id: int, db: Session = Depends(get_db)):
    success = crud.delete_event_type(db, event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event type not found")
    return {"message": "Success"}

# --- Schedules Endpoints ---
@app.get("/api/schedules", response_model=List[schemas.ScheduleResponse])
def read_schedules(db: Session = Depends(get_db)):
    return crud.get_schedules(db)

@app.post("/api/schedules", response_model=schemas.ScheduleResponse)
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    return crud.create_schedule(db, schedule)

@app.put("/api/schedules/{schedule_id}", response_model=schemas.ScheduleResponse)
def update_schedule(schedule_id: int, schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    db_obj = crud.update_schedule(db, schedule_id, schedule)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return db_obj

@app.delete("/api/schedules/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    success = crud.delete_schedule(db, schedule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"message": "Success"}

@app.put("/api/schedules/{schedule_id}/default")
def set_schedule_default(schedule_id: int, db: Session = Depends(get_db)):
    success = crud.set_schedule_default(db, schedule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"message": "Success"}

# --- Availability Endpoints ---
@app.get("/api/schedules/{schedule_id}/availability", response_model=List[schemas.AvailabilityResponse])
def read_schedule_availability(schedule_id: int, db: Session = Depends(get_db)):
    return crud.get_availabilities(db, schedule_id)

@app.put("/api/schedules/{schedule_id}/availability", response_model=List[schemas.AvailabilityResponse])
def update_schedule_availability(schedule_id: int, availabilities: List[schemas.AvailabilityCreate], db: Session = Depends(get_db)):
    return crud.set_availabilities(db, schedule_id, availabilities)

# --- Date Overrides Endpoints ---
@app.get("/api/schedules/{schedule_id}/overrides", response_model=List[schemas.DateOverrideResponse])
def read_schedule_overrides(schedule_id: int, db: Session = Depends(get_db)):
    return crud.get_schedule_overrides(db, schedule_id)

@app.put("/api/schedules/{schedule_id}/overrides", response_model=List[schemas.DateOverrideResponse])
def update_schedule_overrides(schedule_id: int, overrides: List[schemas.DateOverrideCreate], db: Session = Depends(get_db)):
    return crud.set_schedule_overrides(db, schedule_id, overrides)

# --- Public Booking Endpoints ---
@app.get("/api/public/event-types/{slug}", response_model=schemas.EventTypeResponse)
def get_public_event_type(slug: str, db: Session = Depends(get_db)):
    event_type = crud.get_event_type_by_slug(db, slug)
    if not event_type:
        raise HTTPException(status_code=404, detail="Event type not found")
    return event_type

@app.get("/api/public/slots/{slug}")
def get_available_slots(slug: str, target_date: date, db: Session = Depends(get_db)):
    event_type = crud.get_event_type_by_slug(db, slug)
    if not event_type:
        raise HTTPException(status_code=404, detail="Event type not found")
        
    day_of_week = target_date.weekday() # 0 = Mon, 6 = Sun
    schedule_id = event_type.schedule_id
    
    if not schedule_id:
        schedule = db.query(models.Schedule).first()
        schedule_id = schedule.id if schedule else None

    if schedule_id:
        # Check Date Overrides FIRST
        overrides = db.query(models.DateOverride).filter(
            models.DateOverride.schedule_id == schedule_id,
            models.DateOverride.date == target_date
        ).all()
        
        if overrides:
            if any(ov.is_unavailable for ov in overrides):
                availabilities = [] # Full day blocked
            else:
                availabilities = overrides # Duck-typing allows start_time / end_time mapping
        else:
            availabilities = db.query(models.Availability).filter(
                models.Availability.schedule_id == schedule_id,
                models.Availability.day_of_week == day_of_week
            ).all()
    else:
        availabilities = []
    
    if not availabilities:
        return {"date": target_date, "slots": []}
        
    # Get all confirmed bookings for this day
    next_day = target_date + timedelta(days=1)
    bookings_on_day = db.query(models.Booking).filter(
        models.Booking.status == "confirmed",
        models.Booking.start_time >= datetime.combine(target_date, time.min),
        models.Booking.start_time < datetime.combine(next_day, time.min)
    ).all()
    
    slots = []
    duration = timedelta(minutes=event_type.duration_minutes)
    
    for avail in availabilities:
        current_time = datetime.combine(target_date, avail.start_time)
        end_avail_time = datetime.combine(target_date, avail.end_time)
        
        # If looking at today, we want to show times starting from right NOW, 
        # jumping to the next crisp interval, without extending the true schedule limits.
        if target_date == date.today():
            now = datetime.now()
                
            if current_time < now:
                # Snap to the very next clean interval
                minutes_diff = (now - current_time).total_seconds() / 60
                intervals_to_jump = int(minutes_diff // event_type.duration_minutes) + 1
                current_time += timedelta(minutes=intervals_to_jump * event_type.duration_minutes)
        
        while current_time + duration <= end_avail_time:
            slot_end = current_time + duration
            
            # Check overlap considering buffers
            overlap = False
            
            p_start = current_time - timedelta(minutes=event_type.buffer_time_before or 0)
            p_end = slot_end + timedelta(minutes=event_type.buffer_time_after or 0)
            
            for b in bookings_on_day:
                b_start = b.start_time - timedelta(minutes=(b.event_type.buffer_time_before if b.event_type else 0))
                b_end = b.end_time + timedelta(minutes=(b.event_type.buffer_time_after if b.event_type else 0))
                
                if (p_start < b_end) and (p_end > b_start):
                    overlap = True
                    break
                    
            if not overlap:
                slots.append({
                    "start_time": current_time.isoformat(),
                    "end_time": slot_end.isoformat()
                })
                
            # Slots should be incremented based on the event time size dynamically
            current_time += timedelta(minutes=event_type.duration_minutes)
            
    return {"date": target_date, "slots": slots}

# --- Bookings Management ---
@app.get("/api/bookings", response_model=List[schemas.BookingResponse])
def read_bookings(db: Session = Depends(get_db)):
    return crud.get_bookings(db)

@app.post("/api/bookings", response_model=schemas.BookingResponse)
def create_new_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_booking(db, booking)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.patch("/api/bookings/{booking_id}/cancel", response_model=schemas.BookingResponse)
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    db_obj = crud.cancel_booking(db, booking_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_obj
