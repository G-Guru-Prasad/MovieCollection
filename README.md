# Movie Collection Web Application

This is a Django-based web application that allows users to manage their movie collections. Users can register, authenticate, and perform CRUD operations on their collections. The application also fetches movie data from a third-party API.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features
- User registration and authentication
- Create, update, view, and delete movie collections
- Fetch and display movies from a third-party API
- Display favorite genres based on user's collections

## Installation
1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/MovieCollectionProject.git
    cd MovieCollectionProject
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    Create a `.env` file in the root directory and add the following:
    ```
    SECRET_KEY=your_secret_key
    DEBUG=True
    API_USERNAME=your_api_username
    API_PASSWORD=your_api_password
    ```

5. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser (optional, for accessing the admin interface):**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## Usage
- Navigate to `http://localhost:8000/` to access the application.
- Use the provided endpoints to register, authenticate, and manage collections.

## API Endpoints

### User Registration and Authentication
- **Register User**
    - URL: `POST /register/`
    - Request Payload:
        ```json
        {
            "username": "desired_username",
            "password": "desired_password"
        }
        ```
    - Response:
        ```json
        {
            "access_token": "JWT_token"
        }
        ```

### Movie Retrieval
- **Get Movies**
    - URL: `GET /movies/`
    - Response:
        ```json
        {
            "count": <total_number_of_movies>,
            "next": <link_for_next_page>,
            "previous": <link_for_previous_page>,
            "data": [
                {
                    "title": "movie_title",
                    "description": "movie_description",
                    "genres": "comma_separated_genres",
                    "uuid": "movie_uuid"
                }
            ]
        }
        ```

### Collection Management
- **Get All Collections**
    - URL: `GET /collection/`
    - Response:
        ```json
        {
            "is_success": true,
            "data": {
                "collections": [
                    {
                        "title": "collection_title",
                        "uuid": "collection_uuid",
                        "description": "collection_description"
                    }
                ],
                "favourite_genres": "top_3_favourite_genres"
            }
        }
        ```

- **Create Collection**
    - URL: `POST /collection/`
    - Request Payload:
        ```json
        {
            "title": "collection_title",
            "description": "collection_description",
            "movies": [
                {
                    "title": "movie_title",
                    "description": "movie_description",
                    "genres": "comma_separated_genres",
                    "uuid": "movie_uuid"
                }
            ]
        }
        ```
    - Response:
        ```json
        {
            "collection_uuid": "collection_uuid"
        }
        ```

- **Update Collection**
    - URL: `PUT /collection/<collection_uuid>/`
    - Request Payload:
        ```json
        {
            "title": "optional_updated_title",
            "description": "optional_updated_description",
            "movies": "optional_movie_list_to_be_updated"
        }
        ```
    - Response:
        ```json
        {
            "message": "Collection updated successfully"
        }
        ```

- **Get Collection Details**
    - URL: `GET /collection/<collection_uuid>/`
    - Response:
        ```json
        {
            "title": "collection_title",
            "description": "collection_description",
            "movies": [
                {
                    "title": "movie_title",
                    "description": "movie_description",
                    "genres": "comma_separated_genres",
                    "uuid": "movie_uuid"
                }
            ]
        }
        ```

- **Delete Collection**
    - URL: `DELETE /collection/<collection_uuid>/`
    - Response:
        ```json
        {
            "message": "Collection deleted successfully"
        }
        ```

## Testing
1. **Run the tests:**
    ```bash
    python manage.py test
    ```

2. **Sample Test Cases:**
    - Test user registration and authentication.
    - Test creating, updating, viewing, and deleting collections.
    - Test fetching movies from the third-party API.
    - Test the response structure for all endpoints.

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.
