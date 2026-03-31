<<<<<<< HEAD
# Portfolio Website - Madhini Ganesh Reddy

A modern, production-ready portfolio website with a custom admin dashboard built with Django, Tailwind CSS, and more.

## Features

### Frontend (User Interface)
- Modern, responsive design with Tailwind CSS
- Dark mode toggle
- Hero section with typing animation
- About, Skills, Projects, Experience, Education sections
- Contact form with database storage
- Smooth animations with AOS
- Fully responsive (mobile + desktop)

### Admin Dashboard
- Custom modern SaaS-style dashboard
- Login authentication system
- Analytics overview (total projects, messages, skills)
- Quick actions for CRUD operations
- Recent messages display
- Chart.js integration

## Tech Stack

- **Backend**: Django 6.0
- **Database**: SQLite (easily scalable to PostgreSQL)
- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript
- **Authentication**: Django Auth with custom user model
- **Admin Panel**: Custom-built dashboard (not default Django admin)
- **Deployment**: Render, Gunicorn, WhiteNoise

## Project Structure

```
portfolio/
├── accounts/           # Authentication app
├── core/               # Main portfolio app
├── templates/          # Base templates
├── static/             # Static files
├── media/              # User-uploaded files
├── portfolio/          # Django project settings
├── Procfile            # For Render deployment
├── requirements.txt    # Python dependencies
└── runtime.txt         # Python version
```

## Local Development Setup

```bash
# Clone the project
cd portfolio

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py create_superuser

# Load sample data
python manage.py load_sample_data

# Run development server
python manage.py runserver
```

### Access Local Server
- **Frontend**: http://127.0.0.1:8000/
- **Admin Dashboard**: http://127.0.0.1:8000/accounts/login/
- **Django Admin**: http://127.0.0.1:8000/admin/

### Default Credentials
- **Username**: admin
- **Password**: admin123

## Deployment to Render

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
# Create a new repository on GitHub and push
```

### Step 2: Create .env file
Create a `.env` file in the project root:
```
SECRET_KEY=your-secure-random-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
```

Generate a secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Step 3: Deploy on Render
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Create a new **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn portfolio.wsgi:application`
   - **Python Version**: 3.11
5. Add Environment Variables:
   - `SECRET_KEY`: Your generated secret key
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: Your Render domain
6. Click **Deploy**

### Step 4: Create Superuser on Production
After deployment, SSH into your Render service and create superuser:
```bash
render@your-app:~$ python manage.py createsuperuser
```

## Key URLs

| URL | Description |
|-----|-------------|
| `/` | Homepage |
| `/contact/` | Contact form |
| `/accounts/login/` | Admin login |
| `/accounts/dashboard/` | Admin dashboard |
| `/admin/` | Django admin panel |

## Customization

### Adding Your Information

1. Log in to the admin dashboard
2. Go to Profile section to edit your info
3. Add projects, skills, experience, education
4. Your changes will reflect on the homepage

## License

MIT License

## Author

Madhini Ganesh Reddy
Data Analyst & Machine Learning Engineer
=======
# portfolio
Creating responsive frontend interfaces using Django Templates and powerful backend systems with clean, scalable architecture.
>>>>>>> 0d8544d70e692bb536dc870b1feac5ac2fb3c91d
