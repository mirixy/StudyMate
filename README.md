# StudyMate

StudyMate is a web application designed to help students manage their tasks and track their grades efficiently. With a user-friendly interface, StudyMate allows users to toggle between light and dark modes, manage to-do lists, and keep track of their academic performance.

## Features

- **User Authentication**: Secure login and registration system.
- **Task Management**: Add, edit, and delete tasks with deadlines.
- **Grade Tracking**: Add subjects and record grades for each quarter.
- **Light/Dark Mode**: Toggle between light and dark themes for better user experience.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/studymate.git
   cd studymate
   ```

2. **Install Dependencies**:
   Ensure you have Python and pip installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the Database**:
   Initialize the database with:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. **Run the Application**:
   Start the Flask development server:
   ```bash
   flask run
   ```

5. **Access the Application**:
   Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

### Authentication

- **Register**: Create a new account by providing a username and password.
- **Login**: Access your account using your credentials.

### Task Management

- **Add Tasks**: Navigate to the "Aufgaben" section to add new tasks with titles, descriptions, and deadlines.
- **Edit Tasks**: Modify existing tasks by clicking the "Bearbeiten" button.
- **Delete Tasks**: Remove tasks by clicking the "Löschen" button.

### Grade Tracking

- **Add Subjects**: In the "Noten Tracker" section, add new subjects.
- **Record Grades**: Enter grades for each quarter and specify if the subject is a "Leistungskurs" (LK).
- **View Grades**: See a summary of your grades and total points.

### Theme Toggle

- **Light/Dark Mode**: Use the theme toggle button to switch between light and dark modes for a comfortable viewing experience.

## Code Overview

- **Routes**: Defined in `app/routes.py`, handling user authentication, task management, and grade tracking.
  ```python:app/routes.py
  startLine: 1
  endLine: 242
  ```

- **Forms**: Defined in `app/forms.py`, using Flask-WTF for form handling and CSRF protection.
  ```python:app/forms.py
  startLine: 1
  endLine: 33
  ```

- **Templates**: HTML templates for different pages, such as `grades.html`, `add_todo.html`, and `base.html`.
  ```html:app/templates/grades.html
  startLine: 1
  endLine: 190
  ```

  ```html:app/templates/add_todo.html
  startLine: 1
  endLine: 25
  ```

  ```html:app/templates/base.html
  startLine: 1
  endLine: 26
  ```

- **Static Files**: CSS styles are defined in `app/static/style.css` for consistent styling across the app.
  ```css:app/static/style.css
  startLine: 309
  endLine: 680
  ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
