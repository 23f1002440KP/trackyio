from marshmallow import Schema, fields, validate

class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    desc = fields.Str()
    # created_on = fields.Date()
    due_date = fields.Str()
    # is_active = fields.Bool()
    github_link = fields.Str()