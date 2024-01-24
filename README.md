# Kolom - Your Blogging Platform

Kolom is a Django-based blog website that enables users to register, write, and read blog posts. The platform features user authentication, multiple user roles (admin, author, reader), and email notifications for new blog posts.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- User Registration and Authentication
- Three User Roles: Admin, Author, Reader
- Author Role: Write and Publish Blog Posts
- Reader Role: Save Posts and Update Profile Photo
- Email Notifications for New Blog Posts

## Getting Started

### Prerequisites

- Python (3.7+ recommended)
- Django (3.0+ recommended)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/kolom-blog.git
2. Navigate to the project directory:

   ```bash
   cd kolom-blog
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Apply migrations:
    ```bash
    python manage.py migrate
5. Create Superuser:
    ```bash
    python manage.py createsuperuser
6.  Start the developmenet server:
    ```bash
    python manage.py runserver
Visit http://127.0.0.1:8000/ in your browser.

##### Configuration:
  - Update your email settings in settings.py for email notifications.

##### Usage :
  - Register an account on the website.
  - Activate your account by clicking the activation link sent to your email.
  - Log in using your credentials.
  - Explore the blog, save interesting posts, and update your profile photo.
  - If you have the author role, you can write and publish blog posts.

##### Contributing: 
  If you would like to contribute to the project, please follow the Contributing Guidelines.
  
##### License :
   - This project is licensed under the MIT License - see the LICENSE file for details.
     ````bash
     Make sure to replace placeholders like `your-username`, `kolom-blog`, and others with the actual information specific to your project. Additionally, consider creating the referenced files like `CONTRIBUTING.md` and `LICENSE` with relevant content.

