# Vehicle Parking App V2

A multi-user web application for managing 4-wheeler parking lots, spots, and vehicle reservations. Built with Flask (API), VueJS (frontend), Bootstrap (styling), SQLite (database), Redis (caching), and Celery (background jobs).

## Features

- Admin and User roles (role-based access)
- Admin: Manage parking lots, spots, users, and view analytics
- User: Register, login, reserve/occupy/release parking spots, view history
- Reservation and cost calculation
- Analytics and charts (Chart.js)
- Redis caching for performance
- Celery for background jobs (reminders, reports, CSV export)

## Technology Stack

- **Backend:** Flask
- **Frontend:** VueJS
- **Styling:** Bootstrap
- **Database:** SQLite
- **Caching:** Redis
- **Batch Jobs:** Celery + Redis
- **Charts:** Chart.js

## Setup Instructions

1. Clone the repository
2. Set up Python virtual environment and install backend dependencies (`requirements.txt`)
3. Set up Node.js environment and install frontend dependencies (`package.json`)
4. Configure environment variables as needed (see `.env.example`)
5. Run database migrations/initialization script (admin user is seeded automatically)
6. Start Flask backend, VueJS frontend, Redis server, and Celery worker

## Project Structure

- `/backend` - Flask API and models
- `/frontend` - VueJS app
- `/migrations` - Database migration scripts
- `/tasks` - Celery tasks

## Milestones

See the project plan for milestone breakdown and commit messages.

## License

This project is for educational purposes only.
