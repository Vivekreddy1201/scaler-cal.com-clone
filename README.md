Cal.com Clone - Full Stack Scheduling Platform

Description  
This project is a full-stack scheduling and booking application inspired by Cal.com. It allows users to create event types, define availability, and share public booking links where others can schedule meetings.

Live Demo  
https://scaler-cal-com-clone.vercel.app/

Overview  
The application enables users to manage their schedules and allows external users to book time slots based on defined availability. It focuses on clean architecture, efficient scheduling logic, and a smooth booking experience.

Tech Stack  

Frontend  
- Next.js (App Router)  
- TypeScript  
- Tailwind CSS  
- date-fns  

Backend  
- FastAPI  
- SQLAlchemy  
- PostgreSQL  

Deployment  
- Frontend hosted on Vercel  
- Backend and database hosted on Render  

Core Features  

Event Types Management  
- Create event types with title, description, duration, and unique slug  
- Edit and delete event types  
- Each event type has a public booking link  

Availability Settings  
- Configure working days  
- Set daily time ranges  
- Timezone-aware scheduling  

Public Booking  
- Calendar-based date selection  
- Dynamic time slot generation  
- Booking form with name and email  
- Prevention of double booking using backend validation  
- Booking confirmation  

Bookings Dashboard  
- View upcoming bookings  
- View past bookings  
- Cancel bookings  

Bonus Features  
- Buffer time between meetings  
- Multiple availability schedules  
- Date overrides  
- Responsive UI  

System Design  

The application follows a client-server architecture with clear separation between frontend and backend.

Backend  
- REST API built using FastAPI  
- Modular structure with routes, services, and database layers  
- Slot generation based on availability, duration, and buffer time  
- Server-side validation to prevent booking conflicts  

Database Design  
- users table (default user assumed)  
- event_types table  
- availability table  
- schedules table  
- date_overrides table  
- bookings table  

Relationships  
- One user can have multiple event types  
- One event type can have multiple bookings  
- Availability linked to schedules  

Core Logic  

Slot Generation  
- Check date overrides or weekly availability  
- Generate slots based on duration and working hours  
- Apply buffer time before and after events  
- Remove slots that overlap with existing bookings  

Double Booking Prevention  
- Booking validation performed at backend before saving  

Timezone Handling  
- All timestamps stored in UTC  
- Converted to local timezone on frontend  

API Endpoints  

Event Types  
- GET /api/event-types  
- GET /api/event-types/{id}  
- POST /api/event-types  
- PUT /api/event-types/{id}  
- DELETE /api/event-types/{id}  

Schedules and Availability  
- GET /api/schedules  
- POST /api/schedules  
- PUT /api/schedules/{id}/default  
- GET /api/schedules/{id}/availability  
- PUT /api/schedules/{id}/availability  
- GET /api/schedules/{id}/overrides  
- PUT /api/schedules/{id}/overrides  

Public Booking  
- GET /api/public/event-types/{slug}  
- GET /api/public/slots/{slug}?target_date=YYYY-MM-DD  
- POST /api/bookings  

Bookings  
- GET /api/bookings  
- PATCH /api/bookings/{id}/cancel  

Sample API  

POST /api/bookings  

{
  "event_type_id": 1,
  "start_time": "2026-04-16T10:00:00Z",
  "end_time": "2026-04-16T10:30:00Z",
  "name": "ram",
  "email": "ram@gmail.com"
}

Local Setup  

1. Clone repository  
git clone https://github.com/Vivekreddy1201/scaler-cal.com-clone  
cd scaler-cal.com-clone  

2. Backend setup  
cd backend  

python -m venv venv  
source venv/bin/activate   (Windows: venv\Scripts\activate)  

pip install -r requirements.txt  
python seed.py  

uvicorn main:app --reload  

3. Frontend setup  
cd frontend  

npm install  
npm run dev  

Assumptions  
- Single default user (no authentication implemented)  
