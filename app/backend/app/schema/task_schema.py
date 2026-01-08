from marshmallow import Schema, fields, validate

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    desc = fields.Str()
    status = fields.Str(validate=validate.OneOf(["to-do", "in-progress", "done"]))
    priority = fields.Str(validate=validate.OneOf(['low','medium', 'high']))
    due_date = fields.Str()
    # project_id = fields.Int(required=True)