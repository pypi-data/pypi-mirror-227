# ddopy - PyPI Utility Module

## Overview

`ddopy` is a Python module that provides a collection of utility functions and classes to simplify common tasks. Whether you're working with databases or making HTTP requests, this module has you covered.

## Classes

### DatabaseManager

The `DatabaseManager` class is designed to streamline database interaction using SQLAlchemy. It handles the connection to your database and provides methods to execute queries and retrieve results, making database operations efficient and straightforward.

#### Example Usage

```python
from ddopy import DatabaseManager

# Create a DatabaseManager instance with your database URL
db_manager = DatabaseManager(database_url)

# Open a session
session = db_manager.open_session()

# Perform database operations using the session
# Example: session.query(your_model).filter_by(your_condition).all()

# Commit the changes to the database
db_manager.commit_session()

# Close the session when done
db_manager.close_session()
```

### HttpRequester

The `HttpRequester` class simplifies the process of making HTTP POST requests to a specified URL. It is a straightforward utility for sending JSON payloads to a target server.

#### Example Usage

```python
from ddopy import HttpRequester

# Create an HttpRequester instance
http_requester = HttpRequester()

# Set the URL (optional if provided during initialization)
http_requester.set_url("http://your-api-endpoint.com")

# Define the JSON payload
payload = {
    "key1": "value1",
    "key2": "value2"
}

# Send an HTTP POST request with the payload
response_json = http_requester.post_request(payload)

# Process the response
print(response_json)
```

## Functions

Currently, there are no additional utility functions implemented. Stay tuned for updates as we continue to enhance this module with more handy features.

## Installation


You can install `ddopy` from PyPI using pip:

```shell
pip install ddopy
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

If you would like to contribute to this project, please follow our [contributing guidelines](CONTRIBUTING.md).

## Issues and Feedback

If you encounter any issues or have feedback for us, please [open an issue](https://github.com/your-repo-name/issues) on GitHub.

We hope you find `ddopy` useful in your Python projects!
