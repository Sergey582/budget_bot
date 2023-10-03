config = {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": {
                        "port": 5432,
                        "database": "telegram_bot",
                        "host": "postgers",
                        "user": "telegram_bot",
                        "password": "password",
                    }
                }
            },
            "apps": {
                "models": {
                    "models": [
                        "app.core.modules.spending.models",
                        "aerich.models"
                    ],
                    "default_connection": "default"
                },
            },
            "use_tz": True,
        }
