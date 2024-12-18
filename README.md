# Design By Committee

## Setup

```bash
cp .env.example .env
cp .flaskenv.example .flaskenv
pip install -r requirements.txt
```

If you received a DB copy, you're done now. Otherwise, initialize the database:

```bash
flask db upgrade
flask seed-personas
```

## Start the application locally

```bash
flask run
```

## Credits

We heavily drew upon [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) (2024) by Miguel Grinberg for inspiration in setting up the application structure and frontend.