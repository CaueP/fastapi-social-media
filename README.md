# FastAPI Social Media
This is a project created to study FastAPI by a REST API for a social media application.

## Setting up
1. Install `pipx`
2. Install poetry: `pipx install --suffix "@fastapi-social-media" poetry==1.8.1`
3. Install pyenv
    - Create virtualenv `pyenv install 3.12`
    - Link project with pyenv: `poetry@fastapi-social-media env use 3.12`
    - Activate virtualenv `poetry@fastapi-social-media shell`

## Running the app
`poetry@fastapi-social-media run uvicorn social_media_api.main:app --reload`