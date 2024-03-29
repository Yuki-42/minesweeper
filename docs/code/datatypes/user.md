# User

Represents a user in the database.

## Attributes

The user object will have the following attributes:
- `id`: A serial integer representing the unique identifier for the user.
- `uuid`: A UUID string representing the unique identifier for the user. This is generated using uuid4 and is used for authentication.
- `username`: The username of the user.
- `email`: The email of the user.
- `accessLevel`: An integer representing the access level of the user. This can be used to determine what the user can access.
- `_password`: A string representing the hashed password of the user. This attribute should not be accessed directly, but rather through the `checkPassword()` method.

## Methods

The user object will have the following methods:
- `checkPassword(password: str) -> bool`: A method that takes a password string and returns a boolean indicating whether the password matches the user's hashed password.
