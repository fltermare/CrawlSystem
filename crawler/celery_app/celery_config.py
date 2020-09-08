from datetime import timedelta
from celery.schedules import crontab

# Timezone
timezone = "Asia/Taipei"

# import
imports = ("celery_app.tasks",)

# result
result_backend = "db+sqlite:///results.sqlite"

# schedules
beat_schedule = {
    "specified-time": {
        "task": "celery_app.tasks.cleanup",
        # "schedule": crontab(hour=15, minute=0),
        'schedule': timedelta(seconds=60),
    }
}
