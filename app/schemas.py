from marshmallow import Schema, fields, validates, ValidationError

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    year = fields.Int(required=True)

    @validates('year')
    def validate_year(self, value):
        if value < 0 or value > 2100:
            raise ValidationError("Year must be between 0 and 2100.")
