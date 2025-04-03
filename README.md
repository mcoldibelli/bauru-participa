
# Bauru Participa API

This project aims to create an API for the Bauru
Participa platform, which was conceived as a place where residents
can propose ideas, discuss relevant topics, and vote in polls on local issues, from infrastructure projects to cultural events.

This API will allow residents to view active polls, vote on their preferred options, and see the results in real time.
## Environment Variables

To run this project, you must configure the following environment variables in database/envs/.env file:

`MYSQL_ROOT_PASSWORD`

`MYSQL_DATABASE`

`MYSQL_USER`

`MYSQL_PASSWORD`

`DATABASE_URI`

A sample.env file containing these variables is already provided. Populate it with your database-specific values and then rename sample.env to .env.

## Running locally

Clone the project

```bash
  git clone https://github.com/mcoldibelli/bauru-participa.git
```

Enter in project database directory

```bash
  cd bauru-participa/database
```

Start the database docker container

```bash
  docker compose up -d
```
Start the application file

```
python3 run.py
```

## Stack utilizada

**Back-end:** Python, Flask, SQL Alchemy, MySQL, Docker


## API Docs

# API Documentation

## Endpoints

### Create a New Poll
```http
POST /api/enquetes
```
#### Request Body
```json
{
  "title": "string",
  "description": "string"
}
```
#### Response
```json
{
  "message": "Poll created with success",
  "data": {
    "id": "integer",
    "title": "string",
    "description": "string"
  }
}
```

### List All Polls
```http
GET /api/enquetes
```
#### Response
```json
[
  {
    "id": "integer",
    "title": "string",
    "description": "string"
  }
]
```

### Get Poll Details
```http
GET /api/enquetes/{poll_id}
```
#### Response
```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "options": [
    {
      "id": "integer",
      "description": "string"
    } , ... ,
  ]
}
```

### Delete a Poll
```http
DELETE /api/enquetes/{poll_id}
```
#### Response
```json
{
  "message": "Poll deleted with success"
}
```

### Create a New Poll Option
```http
POST /api/enquetes/{poll_id}/opcoes
```
#### Request Body
```json
{
  "description": "string"
}
```
#### Response
```json
{
  "message": "Poll option added with success",
  "data": {
    "id": "integer",
    "poll_id": "integer",
    "description": "string"
  }
}
```

### List Poll Options
```http
GET /api/enquetes/{poll_id}/opcoes
```
#### Response
```json
{
  "poll_id": "integer",
  "options": [
    {
      "id": "integer",
      "description": "string"
    }
  ]
}
```

### Delete a Poll Option
```http
DELETE /api/enquetes/{poll_id}/opcoes/{option_id}
```
#### Response
```json
{
  "message": "Poll option deleted successfully",
  "data": {
    "poll_id": "integer",
    "option_id": "integer"
  }
}
```

### Vote on a Poll
```http
POST /api/enquetes/{poll_id}/votar
```
#### Request Body
```json
{
  "user_id": "integer",
  "option_id": "integer"
}
```
#### Response
```json
{
  "message": "Vote registered successfully",
  "data": {
    "vote_id": "integer",
    "user_id": "integer",
    "poll_id": "integer",
    "option_id": "integer",
    "voted_at": "timestamp"
  }
}
```

### Get Poll Results
```http
GET /api/enquetes/{poll_id}/resultados
```
#### Response
```json
{
  "data": {
    "options": [
      "description": "string",
      "option_id": "integer",
      "percentage": "string",
      "votes": "integer"
    ], ... ,
    "total_votes": "integer"
  }
}
```

## User Endpoints

### Create a New User
```http
POST /api/usuarios
```
#### Request Body
```json
{
  "name": "string"
}
```
#### Response
```json
{
  "message": "User created successfully",
  "data": {
    "id": "integer",
    "name": "string"
  },
}
```

### List All Users
```http
GET /api/usuarios
```
#### Response
```json
[
  {
    "id": "integer",
    "name": "string"
  }, ... ,
]
```