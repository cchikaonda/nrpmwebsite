"# nrpmwebsite" 
# New Restoration Plan Malawi Website

## Overview

The New Restoration Plan (NRP) Malawi Website is a modern content management platform developed using **Django** and **Wagtail CMS**. The website serves as the official online presence of New Restoration Plan Malawi, providing information about the organization's mission, programs, projects, news, publications, and community impact initiatives.

The platform enables administrators and content managers to easily create, edit, and publish content through an intuitive content management interface while maintaining high performance, security, and scalability.

---

## Features

### Content Management

* Wagtail-powered content management system
* User-friendly administrative dashboard
* Page creation and editing
* Rich text content editing
* Image and document management
* Draft and publish workflow

### Website Components

* Home Page
* About Us Section
* Projects and Programs
* News and Updates
* Team Profiles
* Contact Page
* Gallery Management
* Downloadable Resources
* Dynamic Navigation Menus

### Administration

* Role-based user permissions
* Secure authentication system
* Content moderation
* Media library management
* Search functionality

### Technical Features

* Responsive design
* SEO-friendly architecture
* Optimized media handling
* REST API support
* PostgreSQL database support
* Secure deployment configuration

---

## Technology Stack

### Backend

* Python 3.x
* Django
* Wagtail CMS
* Django REST Framework

### Database

* PostgreSQL (Recommended)
* SQLite (Development)

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap

### Server

* Nginx
* Gunicorn
* Linux VPS

---

## Project Structure

```text
project_root/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── home/
├── projects/
├── news/
├── contact/
├── core/
│
├── templates/
├── static/
├── media/
│
├── frontend/
├── backend/
│
└── config/
```

---

## Installation

### Clone the Repository

```bash
git clone <repository_url>
cd nrp-website
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file and configure:

```env
SECRET_KEY=your_secret_key
DEBUG=True

DATABASE_NAME=database_name
DATABASE_USER=database_user
DATABASE_PASSWORD=database_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create a Superuser

```bash
python manage.py createsuperuser
```

### Collect Static Files

```bash
python manage.py collectstatic
```

### Start Development Server

```bash
python manage.py runserver
```

Access the application at:

```text
http://127.0.0.1:8000
```

Access the Wagtail administration panel at:

```text
http://127.0.0.1:8000/admin
```

---

## Deployment

Recommended production environment:

* Ubuntu Server
* PostgreSQL
* Nginx
* Gunicorn
* SSL Certificate (Let's Encrypt)
* VPS Hosting (Hostinger, DigitalOcean, AWS, or similar)

Deployment steps:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

---

## Security Considerations

* Disable DEBUG in production.
* Use HTTPS/SSL certificates.
* Store secrets in environment variables.
* Regularly update dependencies.
* Configure database backups.
* Restrict administrative access.

---

## Contributors

**New Restoration Plan (NRP) Malawi**

### Lead Developer

**Chicco Chikaonda**

* Software Developer & Systems Engineer
* Email: [chicco@amityonline.com](mailto:chicco@amityonline.com)
* Phone: +265 999 048 474

---

## License

Copyright © New Restoration Plan (NRP) Malawi.

All rights reserved.

This software and its source code are the property of New Restoration Plan Malawi and may not be reproduced, modified, or distributed without prior written authorization.

---

## About New Restoration Plan Malawi

New Restoration Plan (NRP) Malawi is committed to promoting sustainable development, community empowerment, environmental stewardship, and innovative solutions that improve livelihoods across Malawi.

Through strategic partnerships and community-driven initiatives, NRP works to create lasting positive change for individuals, families, and communities.

