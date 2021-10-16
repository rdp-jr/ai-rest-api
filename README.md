# AI REST API

## Installation
1. Clone the repository
2. Navigate to project root directory
3. Create a virtual environment with `py -m venv venv` or a different virtual environment if you'd like
4. Install Packages with `pip install -r requirements.txt` 
5. In `app/config.py`, set `testing` to `False` (default set to `True`) and set `mongodb_url` to a MongoDB connection (default set to `mongodb://localhost:27017`)

## Mock Login 
To simulate how the API works, we need to "login" a user.
Do not skip this step or the API will not behave properly.

1. Run `py seed.py` in order to create a test user
2. Go to the URL `/dashboard`. You should see the following:
```
{
  "id": "61642328d0b56917037c40ad",
  "name": "jdoe",
  "projects": []
}
```

Note:
- You may also create a new user through sending a POST request to `/users` (use `localhost:8000/docs` to easily do this). 
- In `app/config.py`, set the `logged_in_user_id` to the desired user to login to (default set to `61642328d0b56917037c40ad`)

## Run the application
1. Run server with `uvicorn app.main:app --reload`
2. View the documentation and test the API at [localhost:8000/docs](http://localhost:8000/docs)

## Run Tests
1. Make sure the database is non-existent, as the tests create and mock the data automatically. The database is cleared after running all tests.
2. In `app/config.py`, set `testing` to `True` (default set to `True`)
3. To run the full test suite, run `pytest`
4. To run a single test (ex. `test_user.py`) run `pytest tests/test_user.py`

## Testing with the Frontend Client

1. Run `py generate_dashboard.py` to populate the dashboard automatically, then view the [Frontend Client](https://github.com/rdp-jr/ai-frontend) in [localhost:5000](http://localhost:5000)