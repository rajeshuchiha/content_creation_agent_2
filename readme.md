First, generate migration locally 'alembic revision --autogenerate -m "Create Tables" '
push version to git
then docker compose up (it has alembic upgrade head)

** Don't forget setting postgres env in powershell

alembic migrations locally:
1.Start postgres(pgvector) (for local) (check later)
docker run -d `
  -p 5432:5432 `
  -e POSTGRES_DB=mydb `
  -e POSTGRES_USER=user `
  -e POSTGRES_PASSWORD=pass `
  --name pg18 `
  pgvector/pgvector:pg18 
2.alembic revision --autogenerate -m "Create Tables" 
3.alembic upgrade head

Always generate migration files locally (dev environment) then **push these files (version) to git**.
alembic upgrade is automatic in CI/CD.