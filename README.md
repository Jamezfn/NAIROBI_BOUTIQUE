# Nairobi Boutique Hub

Welcome to **Nairobi Boutique Hub**, a comprehensive web application built with Flask that allows users to discover, manage, and curate their favorite boutiques and items. Whether you're a boutique owner looking to showcase your products or a shopper aiming to create a personalized bucket list, Nairobi Boutique Hub provides the tools you need to enhance your shopping experience.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Migrations](#database-migrations)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Folder Structure](#folder-structure)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

### **User Authentication**
- **Registration & Login:** Secure user registration and login functionalities.
- **Profile Management:** Users can view and update their profile information, including changing passwords.
- **Authentication Protection:** Certain routes are protected and require users to be logged in to access them.

### **Boutique Management**
- **Create Boutiques:** Boutique owners can create new boutiques with detailed descriptions and locations.
- **Edit & Delete Boutiques:** Owners can update or remove their boutiques as needed.
- **View Boutiques:** Users can browse and view details of various boutiques.

### **Item Management**
- **Add Items to Boutiques:** Owners can add new items to their boutiques, including details like name, price, description, and images.
- **Edit & Delete Items:** Owners can update or remove items from their boutiques.
- **View Items:** Users can view items within boutiques and get detailed information about each item.

### **Bucket List**
- **Add Items:** Users can add items from any boutique to their personalized bucket list.
- **View Bucket List:** Users can view all items in their bucket list, complete with details and pricing.
- **Remove Items:** Users can remove items from their bucket list as desired.

### **Responsive Design**
- **Bootstrap Integration:** The application utilizes Bootstrap 5 for a responsive and modern user interface.
- **Custom Styling:** Additional custom CSS ensures an Apple-like aesthetic and enhanced user experience.

### **Flash Messages**
- **User Feedback:** Informative flash messages provide users with real-time feedback on their actions, such as successful item additions or error notifications.

## Technologies Used

- **Backend:**
  - [Flask](https://flask.palletsprojects.com/) - Web framework for Python.
  - [Flask-Login](https://flask-login.readthedocs.io/) - User session management.
  - [Flask-Migrate](https://flask-migrate.readthedocs.io/) - Handling SQLAlchemy database migrations.
  - [SQLAlchemy](https://www.sqlalchemy.org/) - ORM for database interactions.
  - [Flask-WTF](https://flask-wtf.readthedocs.io/) - Form handling and CSRF protection.
  - [dotenv](https://github.com/theskumar/python-dotenv) - Loading environment variables.

- **Frontend:**
  - [Bootstrap 5](https://getbootstrap.com/) - Responsive CSS framework.
  - [Custom CSS](#) - Additional styling for enhanced UI/UX.

- **Testing:**
  - [unittest](https://docs.python.org/3/library/unittest.html) - Python's built-in testing framework.
  - [Flask-Testing](https://pythonhosted.org/Flask-Testing/) - Extension for testing Flask applications.

## Installation

### **Prerequisites**
- **Python 3.8+**
- **pip** - Python package installer.
- **Git** - Version control system.

### **Steps**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/nairobi-boutique-hub.git
   cd nairobi-boutique-hub
   ```

2. **Create a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```env
     FLASK_ENV=development
     SECRET_KEY=your_secret_key
     DEV_DATABASE_URI=sqlite:///dev.db
     TEST_DATABASE_URI=sqlite:///:memory:
     DATABASE_URI=sqlite:///prod.db
     ```
     - **Note:** Replace `your_secret_key` with a secure key of your choice.

## Configuration

The application uses different configurations for development, testing, and production environments. These configurations are defined in the `config.py` file.

```python
# config.py

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI', 'sqlite:///dev.db')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///:memory:')
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///prod.db')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

- **Switching Configurations:**
  - The application automatically selects the configuration based on the `FLASK_ENV` environment variable.
  - For example, to run in testing mode, set `FLASK_ENV=testing`.

## Database Migrations

The application uses **Flask-Migrate** to handle database migrations.

### **Initialize Migrations**
```bash
flask db init
```

### **Create a Migration Script**
```bash
flask db migrate -m "Initial migration."
```

### **Apply Migrations**
```bash
flask db upgrade
```

- **Note:** Always create and apply migrations when you make changes to your database models.

## Running the Application

1. **Activate the Virtual Environment**
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Set Environment Variables**
   - Ensure that the `.env` file is properly set up with necessary variables.

3. **Run the Application**
   ```bash
   flask run
   ```
   - The application will be accessible at `http://127.0.0.1:5000/`.

## Testing

The application includes a suite of automated tests to ensure functionality and reliability.

### **Running Tests**

1. **Ensure the Virtual Environment is Active**
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Navigate to the Tests Directory**
   ```bash
   cd tests
   ```

3. **Run the Tests**
   ```bash
   python3 test_bucketlist.py
   ```
   - **Expected Output:**
     ```
     ......
     ----------------------------------------------------------------------
     Ran 6 tests in 19.499s

     OK
     ```

### **Test Coverage**

The tests cover various scenarios, including:
- Adding valid and duplicate items to the bucket list.
- Handling invalid or missing `item_id` inputs.
- Ensuring unauthorized users cannot modify bucket lists.
- Verifying that flash messages appear correctly.

## Folder Structure

```
nairobi-boutique-hub/
├── app.py
├── config.py
├── extensions.py
├── models/
│   ├── user.py
│   ├── item.py
│   ├── boutique.py
│   └── bucketlist.py
├── routes/
│   ├── auth.py
│   ├── boutiques.py
│   ├── bucketlist.py
│   └── items.py
├── templates/
│   ├── index.html
│   ├── profile.html
│   ├── bucket-list.html
│   └── ... (other templates)
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   ├── images/
│   │   └── default-avatar.png
│   └── ... (other static files)
├── tests/
│   ├── test_bucketlist.py
│   └── ... (other test files)
├── migrations/
│   └── ... (Flask-Migrate files)
├── requirements.txt
├── .env
└── README.md
```

- **`app.py`:** Application factory and blueprint registrations.
- **`config.py`:** Configuration classes for different environments.
- **`extensions.py`:** Initialization of extensions like SQLAlchemy and Flask-Login.
- **`models/`:** Database models representing users, boutiques, items, and bucket lists.
- **`routes/`:** Blueprint route files handling different functionalities.
- **`templates/`:** Jinja2 templates for rendering HTML pages.
- **`static/`:** Static assets like CSS, JavaScript, and images.
- **`tests/`:** Automated test cases.
- **`migrations/`:** Database migration scripts managed by Flask-Migrate.
- **`requirements.txt`:** Python dependencies.
- **`.env`:** Environment variables.
- **`README.md`:** Project documentation.

## API Endpoints

### **Authentication (`routes/auth.py`)**

- **Register**
  - **URL:** `/auth/register`
  - **Methods:** `GET`, `POST`
  - **Description:** Register a new user.

- **Login**
  - **URL:** `/auth/login`
  - **Methods:** `GET`, `POST`
  - **Description:** User login.

- **Logout**
  - **URL:** `/auth/logout`
  - **Methods:** `POST`
  - **Description:** User logout.

- **Profile**
  - **URL:** `/auth/profile`
  - **Methods:** `GET`
  - **Description:** View user profile.

### **Boutiques (`routes/boutiques.py`)**

- **List Boutiques**
  - **URL:** `/boutiques/list`
  - **Methods:** `GET`
  - **Description:** Display all boutiques.

- **Create Boutique**
  - **URL:** `/boutiques/create`
  - **Methods:** `GET`, `POST`
  - **Description:** Create a new boutique.

- **Update Boutique**
  - **URL:** `/boutiques/update/<int:boutique_id>`
  - **Methods:** `GET`, `POST`
  - **Description:** Update an existing boutique.

- **Delete Boutique**
  - **URL:** `/boutiques/delete/<int:boutique_id>`
  - **Methods:** `POST`
  - **Description:** Delete a boutique.

### **Items (`routes/items.py`)**

- **Create Item**
  - **URL:** `/boutiques/<int:boutique_id>/items`
  - **Methods:** `POST`
  - **Description:** Add a new item to a boutique.

- **Get Items in Boutique**
  - **URL:** `/boutiques/<int:boutique_id>/items`
  - **Methods:** `GET`
  - **Description:** Retrieve all items in a specific boutique.

- **Get Item Details**
  - **URL:** `/items/<int:item_id>`
  - **Methods:** `GET`
  - **Description:** Retrieve details of a specific item.

- **Update Item**
  - **URL:** `/items/<int:item_id>`
  - **Methods:** `POST`
  - **Description:** Update an existing item.

- **Delete Item**
  - **URL:** `/items/<int:item_id>/delete`
  - **Methods:** `POST`
  - **Description:** Delete an item.

### **Bucket List (`routes/bucketlist.py`)**

- **Add to Bucket List**
  - **URL:** `/bucketlist/add`
  - **Methods:** `POST`
  - **Description:** Add an item to the user's bucket list.

- **View Bucket List**
  - **URL:** `/bucketlist/view`
  - **Methods:** `GET`
  - **Description:** View all items in the user's bucket list.

- **Remove from Bucket List**
  - **URL:** `/bucketlist/remove/<int:item_id>`
  - **Methods:** `POST`
  - **Description:** Remove an item from the user's bucket list.

## Contributing

Contributions are welcome! Please follow these steps to contribute to the project:

1. **Fork the Repository**
   - Click the "Fork" button at the top right of the repository page.

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/yourusername/nairobi-boutique-hub.git
   cd nairobi-boutique-hub
   ```

3. **Create a New Branch**
   ```bash
   git checkout -b feature/YourFeatureName
   ```

4. **Make Your Changes**
   - Implement your feature or fix the bug.

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add your commit message here"
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/YourFeatureName
   ```

7. **Create a Pull Request**
   - Navigate to the original repository and click "Compare & pull request".

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/)

---

Thank you for using **Nairobi Boutique Hub**! If you have any questions or need further assistance, feel free to reach out.
