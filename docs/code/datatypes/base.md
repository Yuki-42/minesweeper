# Base 

The project uses a base `DbBase` as a parent class for all database models. This class provides the basic functionality
expected from all database models, having the `id` and `createdAt` attributes.

## Attributes

The `DbBase` object will have the following attributes:
- `id`: A serial integer representing the unique identifier for the object.
- `createdAt`: A datetime object representing the date and time the object was created.

## Methods

The `DbBase` object will have the following methods:
- `dict() -> dict`: A method that returns a dictionary representation of the object. This method is used to convert 
the object to a format that can be easily serialized to JSON.
- `__int__() -> int`: A method that returns the `id` attribute of the object. This method is used to allow the object
to be used as an integer in contexts where the `id` attribute is needed.
- `_set(column: str, value: Any) -> None`: A method that sets the value of a column in the object. This method is used
to set the values of the object's attributes when creating or updating the object in the database.


