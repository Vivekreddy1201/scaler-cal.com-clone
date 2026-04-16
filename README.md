# Scheduling Platform (Cal.com Clone)

A functional scheduling and booking web application designed to visually resemble Cal.com. 

## Tech Stack
- **Frontend**: Next.js (App Router), React, Tailwind CSS V4, Lucide React, Date-fns.
- **Backend**: FastAPI (Python), SQLAlchemy.
- **Database**: PostgreSQL (`psycopg2`).

## Features
- **Event Types Management**: Create, view, delete event types. Each generates a shareable public link.
- **Availability Settings**: Configure weekly working days and hours.
- **Public Booking Page**: Shareable link `/[slug]` with a smooth calendar and time slot picker.
- **Bookings Dashboard**: View upcoming and past appointments. Cancel upcoming appointments.

## Database Schema Design
1. **`event_types`**: Stores `id`, `title`, `description`, `duration_minutes`, `slug`.
2. **`availabilities`**: Stores `day_of_week` (0-6), `start_time`, `end_time`, `timezone`.
3. **`bookings`**: Stores `event_type_id`, `booker_name`, `booker_email`, `start_time`, `end_time`, `status`. Links to `event_types`. 

## Setup Instructions

### 1. Database Setup
Ensure PostgreSQL is running locally and update the connection string in `backend/database.py` to match your credentials. Currently, it defaults to:
`postgresql://postgres:<password>@localhost:5432/scaler_ag`

### 2. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Seed the database with fake data:
   ```bash
   python seed.py
   ```
5. Run the FastAPI development server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### 3. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
4. Access the admin dashboard at `http://localhost:3000`.

## Assumptions
- For the MVP, timezones are normalized to UTC.
- A default internal user is logged in, and therefore there is no authentication layer required by the prompt.
- The slots rendered on the public booking page are logically clamped by the Event Type's duration (e.g. 30 min slices between start and end availability).
