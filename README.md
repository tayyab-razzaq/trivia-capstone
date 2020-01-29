# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Update questions.
5) Search for questions based on a text query string.
6) Play the quiz game, randomizing either all questions or within a specific category. 


API Endpoints Documentation
--------------------------------------------------------
GET `'/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.

```json5
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```

GET `'/questions'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Fetches a list of questions in which each entry is question dictionary with the keys are answer, category, difficulty, id and question.
- Request Arguments: Page Number
- Returns: Dictionary of Categories, Current Category, List of questions and total number of questions.

```json5
{
	"categories": {
		"1": "Science",
		"2": "Art",
		"3": "Geography",
		"4": "History",
		"5": "Entertainment",
		"6": "Sports"
	},
	"current_category": null,
	"questions": [
		{
			"answer": "Apollo 13",
			"category": 5,
			"difficulty": 4,
			"id": 2,
			"question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
		},
		{
			"answer": "Tom Cruise",
			"category": 5,
			"difficulty": 4,
			"id": 4,
			"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
		},
		{
			"answer": "Maya Angelou",
			"category": 4,
			"difficulty": 2,
			"id": 5,
			"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
		},
		{
			"answer": "Edward Scissorhands",
			"category": 5,
			"difficulty": 3,
			"id": 6,
			"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
		},
		{
			"answer": "Muhammad Ali",
			"category": 4,
			"difficulty": 1,
			"id": 9,
			"question": "What boxer's original name is Cassius Clay?"
		},
		{
			"answer": "Brazil",
			"category": 6,
			"difficulty": 3,
			"id": 10,
			"question": "Which is the only team to play in every soccer World Cup tournament?"
		},
		{
			"answer": "Uruguay",
			"category": 6,
			"difficulty": 4,
			"id": 11,
			"question": "Which country won the first ever soccer World Cup in 1930?"
		},
		{
			"answer": "George Washington Carver",
			"category": 4,
			"difficulty": 2,
			"id": 12,
			"question": "Who invented Peanut Butter?"
		},
		{
			"answer": "Lake Victoria",
			"category": 3,
			"difficulty": 2,
			"id": 13,
			"question": "What is the largest lake in Africa?"
		},
		{
			"answer": "The Palace of Versailles",
			"category": 3,
			"difficulty": 3,
			"id": 14,
			"question": "In which royal palace would you find the Hall of Mirrors?"
		}
	],
	"total_questions": 26,
	"success": true
}
```

DELETE `'/questions/<int:question_id>'`

- Delete question from the questions in database.
- Request Arguments: questions_id(Question Id)
- Returns: true with status 204 if successfully deleted.

```json5
{
    "success": true
}
```

POST `'/questions'`

- Create a new question
- Request Body: question, answer, difficulty and category.
- Returns: true and question id with status 201 if successfully created.

Request

```json5
{
    "question": "Test 1",
    "answer": "Answer 1",
    "category": 1,
    "difficulty": 1
}
```

Response

```json5
{
    "success": true,
    "id": 15
}
```

PATCH `'/questions<int:question_id>'`

- Update the based on given question id.
- Request Arguments: questions_id(Question Id)
- Request Body: question, answer, difficulty and category.
- Returns: true and question id with status 200 if successfully updated.

Request

id=1
```json5

{
    "question": "Test 2",
    "answer": "Answer 2",
    "category": 1,
    "difficulty": 1
}
```

Response

```json5
{
    "question": "Test 2",
    "answer": "Answer 2",
    "category": 1,
    "difficulty": 1,
    "id": 1
}
```

POST `'/questions/filter'`

- Searches for the questions
- Request Body: search term to search question on that.
- Returns: List of questions and total number of questions.

Request

```json5
{
    "searchTerm": "The"
}
```

Response

```json5
{
	"questions": [
		{
			"answer": "Maya Angelou",
			"category": 4,
			"difficulty": 2,
			"id": 5,
			"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
		},
		{
			"answer": "Tom Cruise",
			"category": 5,
			"difficulty": 4,
			"id": 4,
			"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
		},
		{
			"answer": "Edward Scissorhands",
			"category": 5,
			"difficulty": 3,
			"id": 6,
			"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
		},
		{
			"answer": "Brazil",
			"category": 6,
			"difficulty": 3,
			"id": 10,
			"question": "Which is the only team to play in every soccer World Cup tournament?"
		},
		{
			"answer": "Uruguay",
			"category": 6,
			"difficulty": 4,
			"id": 11,
			"question": "Which country won the first ever soccer World Cup in 1930?"
		},
		{
			"answer": "Lake Victoria",
			"category": 3,
			"difficulty": 2,
			"id": 13,
			"question": "What is the largest lake in Africa?"
		},
		{
			"answer": "The Palace of Versailles",
			"category": 3,
			"difficulty": 3,
			"id": 14,
			"question": "In which royal palace would you find the Hall of Mirrors?"
		},
		{
			"answer": "The Liver",
			"category": 1,
			"difficulty": 4,
			"id": 20,
			"question": "What is the heaviest organ in the human body?"
		},
		{
			"answer": "Blood",
			"category": 1,
			"difficulty": 4,
			"id": 22,
			"question": "Hematology is a branch of medicine involving the study of what?"
		},
		{
			"answer": "Scarab",
			"category": 4,
			"difficulty": 4,
			"id": 23,
			"question": "Which dung beetle was worshipped by the ancient Egyptians?"
		}
	],
	"total_questions": 10,
	"success": true
}
```

POST `'/categories/<int:category_id>/questions'`

- To get questions based on category
- Request Arguments: category_id (Category Id).
- Returns: List of questions, total number of questions and current category.

for category 1 response is below

```json5
{
	"current_category": {
		"id": 1,
		"type": "Science"
	},
	"questions": [
		{
			"answer": "The Liver",
			"category": 1,
			"difficulty": 4,
			"id": 20,
			"question": "What is the heaviest organ in the human body?"
		},
		{
			"answer": "Alexander Fleming",
			"category": 1,
			"difficulty": 3,
			"id": 21,
			"question": "Who discovered penicillin?"
		},
		{
			"answer": "Blood",
			"category": 1,
			"difficulty": 4,
			"id": 22,
			"question": "Hematology is a branch of medicine involving the study of what?"
		},
		{
			"answer": "Answer 1",
			"category": 1,
			"difficulty": 1,
			"id": 24,
			"question": "Test 1"
		},
		{
			"answer": "Answer 1",
			"category": 1,
			"difficulty": 1,
			"id": 25,
			"question": "Test 1"
		},
		{
			"answer": "Answer 1",
			"category": 1,
			"difficulty": 1,
			"id": 26,
			"question": "Test 1"
		},
		{
			"answer": "Answer 1",
			"category": 1,
			"difficulty": 1,
			"id": 27,
			"question": "Test 1"
		},
		{
			"answer": "Answer 1",
			"category": 1,
			"difficulty": 1,
			"id": 28,
			"question": "Test 1"
		},
		{
			"answer": "Answer 1",
			"category": 1,
			"difficulty": 1,
			"id": 29,
			"question": "Test 1"
		},
		{
			"answer": "Answer 1",
			"category": 1,
			"difficulty": 1,
			"id": 31,
			"question": "Test 1"
		},
		{
			"answer": "Answer 1",
			"category": 1,
			"difficulty": 1,
			"id": 33,
			"question": "Test 1"
		},
		{
			"answer": "Answer 1",
			"category": 1,
			"difficulty": 1,
			"id": 35,
			"question": "Test 1"
		},
		{
			"answer": "Answer 1",
			"category": 1,
			"difficulty": 1,
			"id": 37,
			"question": "Test 1"
		}
	],
	"total_questions": 13,
	"success": true
}
```

POST `'/quizzes'`

- To get questions to play the quiz.
- Returns: Random question within the given category.

Request

```json5
{
    "quiz_category": {
        "id": 1
    },
    "previous_questions": []
}
```

Response

```json5
{
    "question": {
        "answer": "Blood", 
        "category": 1, 
        "difficulty": 4, 
        "id": 22, 
        "question": "Hematology is a branch of medicine involving the study of what?"
    },
    "success": true
}
```

Errors
--------------------------------------------------------

Bad Request `400`

```json5
{
  'success': false,
  'error': 400,
  'message': 'Bad Request'
}
```

Unauthorized `401`

```json5
{
  'success': false,
  'error': 401,
  'message': 'Unauthorized'
}
```

Forbidden `403`

```json5
{
  'success': false,
  'error': 403,
  'message': 'Forbidden'
}
```

Not Found `404`

```json5
{
  'success': false,
  'error': 404,
  'message': 'Not Found'
}
```

Method Not Allowed `405`

```json5
{
  'success': false,
  'error': 405,
  'message': 'Method Not Allowed'
}
```

Unprocessable Entity `422`

```json5
{
  'success': false,
  'error': 422,
  'message': 'Unprocessable Entity'
}
```

Internal Server Error `500`

```json5
{
  'success': false,
  'error': 500,
  'message': 'Internal Server Error'
}
```

Permissions Documentation
--------------------------------------------------------

- `add-question` permission to call api to add question in db through through POST `'/questions'` api
- `update-question` permission to call api to update question in db through PATCH `'/questions<int:question_id>'` api
- `delete-question` permission to call api to delete question in db through through DELETE `'/questions<int:question_id>'` api
- `play-quiz` permission to call api to play quiz through POST `'/quizzes'` api

Roles Documentation
--------------------------------------------------------
### Manager

Can add/update/delete question and play quiz

Permissions: 

- `add-question`
- `update-question`
- `delete-question`
- `play-quiz`

### Member

Can play quiz

Permissions: 

- `play-quiz`


Setting up the development environment
--------------------------------

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
export DATABASE_URL=postgres://postgres:postgres@localhost:5432/trivia
flask run
```

`DATABASE_URL` can be different on different environment so choose value of that variable according to your machine.

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## Testing
To run the tests from file, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
export TEST_DATABASE_URL=postgres://postgres:postgres@localhost:5432/trivia_test
python test_flaskr.py
```

`TEST_DATABASE_URL` can be different on different environment so choose value of that variable according to your machine.

To test the endpoint hosted at heroku use the tokens from the `tokens.json` file

or use the below link to fetch the updated tokens

`https://kagaroatgoku.auth0.com/authorize?audience=trivia-api&response_type=token&client_id=0cakHerqB1NapAVD0th3RJEjNsDsUBsU&redirect_uri=http://localhost:8000/login-results`

User with email `fsnd-capstone-manager@gmail.com` is assigned the `Manager` role
User with email `fsnd-capstone-member@gmail.com` is assigned the `Member` role

Heroku app is deployed at https://trivia-api-capstone.herokuapp.com/

