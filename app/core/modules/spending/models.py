from tortoise import Model, fields


class Expense(Model):
    telegram_user_id = fields.IntField()
    amount = fields.FloatField()
    currency = fields.CharField(max_length=16)
    category = fields.IntField()
    updated_at = fields.DatetimeField()
    created_at = fields.DatetimeField()

    class Meta:
        table = "expenses"
        indexes = (
            ("telegram_user_id", "category"),
        )
