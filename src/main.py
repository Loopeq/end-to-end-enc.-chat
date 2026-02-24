# odds_service/
# │
# ├── app/
# │   ├── main.py
# │   ├── config/
# │   │   ├── settings.py
# │   │   └── logging.py
# │   │
# │   ├── api/
# │   │   ├── deps.py
# │   │   ├── routes/
# │   │
# │   ├── core/
# │   │   ├── redis.py
# │   │   ├── celery_app.py
# │   │   ├── database.py
# │   │   └── scheduler.py
# │   │
# │   ├── models/
# │   │   ├── match.py
# │   │   ├── market.py
# │   │   └── odds_snapshot.py
# │   │
# │   ├── schemas/
# │   │
# │   ├── services/
# │   │
# │   ├── workers/
# │   │
# │   └── repositories/
# │
# ├── alembic/
# ├── docker/
# │   ├── Dockerfile
# │   └── docker-compose.yml
# │
# ├── requirements.txt
# └── README.md