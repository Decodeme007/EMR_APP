# 🏥 IPD Electronic Medical Record (EMR) System

A **Django-based Electronic Medical Record (EMR) system** designed to digitize and streamline **In-Patient Department (IPD)** workflows in clinics and healthcare facilities.

The system provides a centralized platform for managing patients, clinical information, billing, user accounts, and hospital workflows through a modular Django architecture.

live link: https://emr-app-yl3r.onrender.com/
> **Project Status:** 🚧 Under Active Development

---

## 📌 Overview

The IPD EMR system is a web-based healthcare management application built with **Python and Django**.

The primary goal of the system is to replace fragmented/manual patient record management with a structured digital workflow where patient information, clinical records, and billing data can be managed from a centralized application.

The project follows a modular architecture with separate Django applications for different healthcare domains.

### Core Modules

* 👤 **User & Account Management**
* 🧑‍⚕️ **Patient Management**
* 🩺 **Clinical Management**
* 💳 **Billing Management**
* 📁 **Medical Record Management**
* 🏥 **IPD Workflow Management**

---

## ✨ Key Features

### 👤 Account Management

* User authentication and authorization
* Custom user management
* User profiles
* Institution-based user association
* Role-oriented access to application functionality

### 🧑‍⚕️ Patient Management

* Patient registration and profile management
* Patient demographic information
* Patient identification and record tracking
* Centralized patient information

### 🏥 IPD Management

The system is designed around the workflow of patients admitted to an **In-Patient Department (IPD)**.

The workflow can be extended to support:

* Patient admission
* Bed/ward allocation
* Admission records
* Attending doctor information
* Patient clinical history
* Treatment information
* Discharge workflow

### 🩺 Clinical Management

The clinical module provides the foundation for maintaining patient-related medical information.

It is designed to support:

* Clinical observations
* Diagnosis information
* Treatment records
* Medical notes
* Patient history
* Clinical documentation

### 💳 Billing

The billing module is designed to manage financial information associated with patient care.

Possible workflows include:

* Patient billing
* Service charges
* Billing records
* Payment tracking
* IPD-related expenses

---

## 🏗️ Project Architecture

The project follows Django's modular application architecture.

```text
EMR_APP/
│
├── accounts/          # User and account management
│
├── patients/          # Patient management
│
├── clinical/          # Clinical/medical records
│
├── billing/           # Billing and financial workflows
│
├── config/            # Django project configuration
│
├── templates/         # HTML templates
│
├── static/            # Static assets
│
├── media/             # Uploaded media/profile files
│
├── manage.py          # Django management utility
│
├── requirements.txt   # Python dependencies
│
├── build.sh           # Deployment/build configuration
│
└── README.md
```

---

## 🛠️ Technology Stack

| Technology              | Purpose                     |
| ----------------------- | --------------------------- |
| **Python**              | Backend programming         |
| **Django 5.2**          | Web application framework   |
| **PostgreSQL**          | Production database support |
| **SQLite**              | Local development database  |
| **Django Templates**    | Frontend rendering          |
| **HTML/CSS**            | User interface              |
| **Bootstrap 5**         | Responsive UI               |
| **Django Crispy Forms** | Form rendering and styling  |
| **Pillow**              | Image/media processing      |
| **Gunicorn**            | Production WSGI server      |
| **WhiteNoise**          | Static file serving         |
| **dj-database-url**     | Database configuration      |

---

## 🔐 Multi-Institution Architecture

The application is designed with an **institution-aware architecture**, allowing users and healthcare data to be associated with a particular institution.

This provides a foundation for a multi-tenant healthcare system where application data can be scoped according to the healthcare institution associated with the authenticated user.

The architecture uses Django middleware to make the current institution available during request processing.

```text
Authenticated User
       │
       ▼
User's Institution
       │
       ▼
Institution-aware Request
       │
       ▼
Django Application Modules
       │
       ├── Patients
       ├── Clinical
       └── Billing
```

---

## 🔄 Application Workflow

A typical IPD workflow can be represented as:

```text
Patient Registration
        │
        ▼
Patient Admission
        │
        ▼
IPD / Ward Allocation
        │
        ▼
Clinical Assessment
        │
        ▼
Diagnosis & Treatment
        │
        ▼
Clinical Monitoring
        │
        ▼
Billing & Charges
        │
        ▼
Discharge
        │
        ▼
Medical Record
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Decodeme007/EMR_APP.git

cd EMR_APP
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The project dependencies include Django, Crispy Forms, Bootstrap 5, PostgreSQL support, Pillow, Gunicorn, WhiteNoise, and related packages.

### 4. Configure the Database

For local development, the project can use SQLite.

For production deployment, PostgreSQL can be configured through the Django database configuration/environment variables.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/emr_database
```

### 5. Apply Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create the administrator account.

### 7. Run the Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 📂 Django Applications

### `accounts`

Responsible for:

* User authentication
* User profiles
* Institution association
* Account-related functionality

### `patients`

Responsible for:

* Patient registration
* Patient profiles
* Patient information
* Patient record management

### `clinical`

Responsible for:

* Clinical information
* Medical records
* Diagnosis/treatment-related workflows
* Patient clinical documentation

### `billing`

Responsible for:

* Billing records
* Patient charges
* Financial workflows

---

## 🗄️ Database

The application uses Django's ORM for database interaction.

Development:

```text
SQLite
```

Production:

```text
PostgreSQL
```

The database layer is designed to maintain relationships between:

```text
Institution
    │
    ├── Users
    │
    └── Patients
          │
          ├── Clinical Records
          │
          └── Billing Records
```

---

## 📦 Deployment

The repository includes a `build.sh` script and production-oriented dependencies such as **Gunicorn** and **WhiteNoise**, providing a foundation for deployment to a cloud/server environment.

Before production deployment, configure:

* Production database
* Environment variables
* `SECRET_KEY`
* `DEBUG=False`
* `ALLOWED_HOSTS`
* Static files
* Media storage
* HTTPS/SSL
* Database credentials

---

## 🔒 Security Considerations

Because this application deals with healthcare information, production deployment should implement appropriate security controls.

Important considerations include:

* Secure authentication
* Role-based authorization
* HTTPS
* Environment-based secret management
* Database access controls
* Secure media/file handling
* Audit logging
* Protection of sensitive patient information
* Regular database backups

> **Note:** This project is currently under development and should not be used with real patient data in production without appropriate security, privacy, compliance, and clinical validation measures.

---

## 🎯 Future Enhancements

Planned/possible improvements include:

* [ ] Advanced role-based access control
* [ ] Doctor dashboard
* [ ] Nurse dashboard
* [ ] IPD admission/discharge workflow
* [ ] Bed and ward management
* [ ] Prescription management
* [ ] Laboratory investigations
* [ ] Radiology records
* [ ] Discharge summary generation
* [ ] PDF medical reports
* [ ] Advanced billing
* [ ] Payment integration
* [ ] REST API using Django REST Framework
* [ ] Mobile application integration
* [ ] Audit logs
* [ ] Notifications
* [ ] Dashboard and analytics
* [ ] Automated database backups

---



## 📄 License

This project is currently intended for educational and development purposes.
Add an appropriate open-source license if the project is intended for public distribution.
