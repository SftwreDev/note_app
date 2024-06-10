# FastAPI Application

This FastAPI application provides an API for managing notes and tags.

## Getting Started

Follow these steps to get the project up and running on your local machine for development and testing purposes.

### Prerequisites

- [Python](https://www.python.org/downloads/) (3.10+ recommended)
- [Git](https://git-scm.com/)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/)

### Installation

1. **Clone the Repository**

    Clone the repository to your local machine using the following command:

    ```bash
    git clone https://github.com/SftwreDev/note_app.git
    ```

2. **Navigate to the Application Directory**

    ```bash
    cd app
    ```

3. **Create a Virtual Environment**

    Create a virtual environment to manage your dependencies.

    ```bash
    python -m venv venv
    ```

4. **Activate the Virtual Environment**

    Activate the virtual environment.

    - **Windows**

      ```bash
      venv\Scripts\activate
      ```

    - **Linux / macOS**

      ```bash
      source venv/bin/activate
      ```

5. **Install Dependencies**

    Install the required Python packages from `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

6. **Create a `.env` File**

    Create a `.env` file in the root of the project and set your `DB_URL` environment variable.

    Example `.env` file:

    ```env
    DB_URL=sqlite:///./test.db
    ```

    Replace `sqlite:///./test.db` with the appropriate database URL for your environment.

7. **Run Alembic Migrations**

    Apply the database migrations using Alembic.

    ```bash
    alembic upgrade head
    ```

8. **Run the FastAPI Application**

    Start the FastAPI application in development mode.

    ```bash
    fastapi dev main.py
    ```

    By default, the application will run at `http://127.0.0.1:8000`.
