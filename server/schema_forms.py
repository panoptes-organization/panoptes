from marshmallow import Schema, fields


class SnakemakeUpdateMessage(Schema):

    info = fields.Str(required=False)
    done = fields.Int(required=False)
    total = fields.Int(required=False)


class SnakemakeUpdateForm(Schema):

    """ /api/note - POST

    Parameters:
     - title (str)
     - note (str)
     - user_id (int)
     - ts (time)
    """
    # the 'required' argument ensures the field exists
    msg = fields.Nested(SnakemakeUpdateMessage, required=True)
    timestamp = fields.DateTime(required=True)
    id = fields.Integer(required=False)


