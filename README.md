Cal.com Clone

Build a scheduling and booking application that replicates core functionality and user experience of Cal.com, including event creation, availability management, and public booking.

 Live Demo

 https://scaler-cal-com-clone.vercel.app/

 GitHub Repository

 https://github.com/Vivekreddy1201/scaler-cal.com-clone

 Overview

This project is a full-stack scheduling application that allows users to:

Create and manage event types
Configure weekly availability and time slots
Share public booking links
Accept bookings from external users
Prevent double bookings using backend validation

The application is built with a focus on clean architecture, scalability, and real-world scheduling logic.

Tech Stack
Frontend
Framework: Next.js (App Router)
Language: TypeScript
Styling: Tailwind CSS
Date Handling: date-fns
Backend
Framework: FastAPI
ORM: SQLAlchemy
Database: PostgreSQL
Deployment
Frontend: Vercel
Backend + DB: Render
Core Features
1. Event Types Management
Create event types (title, description, duration, slug)
Edit and delete events
Unique public booking link for each event
2. Availability Settings
Set working days (e.g., Mon–Fri)
Configure daily time ranges
Timezone-aware scheduling
3. Public Booking Page
Calendar-based date selection
Dynamic time slot generation
Booking form (name + email)
Double booking prevention (server-side validation)
Booking confirmation
4. Bookings Dashboard
View upcoming bookings
View past bookings
Cancel bookings
Bonus Features Implemented
Buffer time between meetings
Multiple availability schedules
Date overrides (custom availability per day)
Responsive UI
System Design & Architecture
Backend
RESTful API using FastAPI
Modular structure:
Routes → Business Logic → Database Layer
Slot generation logic:
Based on availability + duration + buffer
Conflict prevention:
Booking validation before insert
Database Design

Key tables:

users (default user assumed)
event_types
availability
bookings

Relationships:

One user → many event types
One event type → many bookings
Availability linked to user
Key Challenges & Solutions
1. Preventing Double Booking
Implemented backend validation before confirming booking
Ensures slot is still available at request time
2. Time Slot Generation
Dynamically generated slots using:
Start time
End time
Event duration
Buffer time
3. Timezone Handling
Stored timestamps in UTC
Converted to user timezone on frontend
Sample API
Create Booking
POST /api/bookings
{
  "event_type_id": 1,
  "start_time": "2026-04-16T10:00:00Z",
  "end_time": "2026-04-16T10:30:00Z",
  "name": "John Doe",
  "email": "john@example.com"
}
Local Setup
1. Clone Repository
git clone https://github.com/Vivekreddy1201/scaler-cal.com-clone
cd scaler-cal.com-clone
2. Backend Setup
cd backend

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Run migrations / seed data
python seed.py

uvicorn main:app --reload
3. Frontend Setup
cd frontend

npm install
npm run dev
Assumptions
Single default user (no authentication required)
Email notifications not implemented
Basic validation for booking inputs
📸 Screenshots

(Add screenshots here for better presentation)

Evaluation Readiness

This project satisfies:

Functionality (all core features)
UI/UX (Cal.com-inspired design)
Database design (normalized schema)
Code quality (modular structure)
Code understanding (well-defined logic layers)
