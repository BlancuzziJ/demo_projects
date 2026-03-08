# Task Manager – Django Demo

A minimal task management web application that demonstrates core Django concepts.

## What it demonstrates

- **Models** – `Task` model with fields for title, description, due date, priority, and completion status
- **Views** – Class-based views (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`)
- **Templates** – Base template with block inheritance; Bootstrap 5 for styling
- **Forms** – `ModelForm` with validation
- **Django Admin** – Registered model with list display, filters, and search
- **URL routing** – `urls.py` patterns for CRUD operations

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Apply migrations
python manage.py migrate

# 3. Create a superuser (for Django Admin)
python manage.py createsuperuser

# 4. Run the development server
python manage.py runserver
```

Then open http://127.0.0.1:8000/ in your browser.

## Project Structure

```
task_manager/
├── manage.py
├── requirements.txt
├── task_manager/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── tasks/                 # Tasks app
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── urls.py
    ├── views.py
    └── templates/
        └── tasks/
            ├── base.html
            ├── task_list.html
            ├── task_detail.html
            ├── task_form.html
            └── task_confirm_delete.html
```
