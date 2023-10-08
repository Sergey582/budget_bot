from tortoise import Model, fields


class User(Model):
    user_id = fields.IntField(unique=True)
    username = fields.CharField(max_length=255, default='')
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"


class Expense(Model):
    user = fields.ForeignKeyField('models.User')
    amount = fields.FloatField()
    currency = fields.CharField(max_length=16)
    category = fields.IntField()
    transaction_date = fields.DatetimeField(default=None)
    updated_at = fields.DatetimeField()
    created_at = fields.DatetimeField()

    class Meta:
        table = "expenses"
        indexes = (
            ("user_id", "category"),
        )
