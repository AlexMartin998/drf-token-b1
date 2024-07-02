# Authentication API

This API provides endpoints for user authentication, including login, registration, and profile retrieval. It uses Django REST Framework for handling requests and responses.

## Endpoints

### Login

- **URL:** `/login/`
- **Method:** `POST`
- **Description:** Authenticates a user by their username and password. If successful, returns a token for subsequent authenticated requests.
- **Data Params:**
  - `username`: The user's username.
  - `password`: The user's password.
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** `{ token: "user_token", user: { serialized user data } }`
- **Error Response:**
  - **Code:** 400 BAD REQUEST
  - **Content:** `{ error: "Invalid password" }`

### Register

- **URL:** `/register/`
- **Method:** `POST`
- **Description:** Registers a new user with the provided username, password, and email. Returns a token for the newly created user.
- **Data Params:**
  - `username`: Desired username.
  - `password`: Desired password.
  - `email`: User's email address.
- **Success Response:**
  - **Code:** 201 CREATED
  - **Content:** `{ token: "new_user_token", user: { id, username, email } }`
- **Error Response:**
  - **Code:** 400 BAD REQUEST
  - **Content:** `{ error details }`

### Profile

- **URL:** `/profile/`
- **Method:** `GET`
- **Description:** Retrieves the profile of the currently authenticated user. Requires a valid token.
- **Headers:**
  - `Authorization`: Token `<user_token>`
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** `{ message: "User profile", user: { id, username, email } }`

## Authentication and Permissions

- **Authentication:** This API uses token-based authentication. Clients should include an `Authorization` header with the value `Token <user_token>` to authenticate requests.
- **Permissions:** The profile endpoint requires the user to be authenticated. Other endpoints have their specific requirements as described.

## Models

- **User:** Utilizes Django's built-in `User` model.
- **Token:** Uses Django REST Framework's `Token` model for managing authentication tokens.

## Serialization

- **UserSerializer:** Serializes user data for responses. Includes fields such as `id`, `username`, and `email`.

## Security

Passwords are hashed using Django's `make_password` function before being stored in the database.

## Dependencies

- Django
- Django REST Framework