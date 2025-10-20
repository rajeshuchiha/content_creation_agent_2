First, generate migration locally 'alembic revision --autogenerate -m "Create Tables" '
push version to git
then docker compose up (it has alembic upgrade head)