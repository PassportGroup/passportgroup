from marshmallow import Schema, fields


class PassportMailSchema(Schema):
    id = fields.Integer()
    message_id = fields.Str()
    thread_id = fields.Str()
    excerpt = fields \
        .Function(lambda obj: (obj.snippet[:250] + '...') if len(obj.snippet) > 250 else obj.snippet)


class PassportGroupTaskSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    slug = fields.Str()
    excerpt = fields\
        .Function(lambda obj: (obj.description[:250] + '...') if len(obj.description) > 250 else obj.description)
    status = fields.Str()
    cron_expression = fields.Str()
    description = fields.Str()
    extra_parameters = fields.Function(lambda obj: obj.parameters)
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    class Meta:
        ordered = True
