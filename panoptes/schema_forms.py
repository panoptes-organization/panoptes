from marshmallow import Schema, fields


class SnakemakeUpdateMessage(Schema):

    info = fields.Str(required=False)
    done = fields.Int(required=False)
    total = fields.Int(required=False)
    msg = fields.Str(required=False)
    level = fields.Str(required=False)


class SnakemakeUpdateForm(Schema):

    """ /api/note - POST

    Parameters:
     - title (str)
     - note (str)
     - user_id (int)
     - ts (time)
    """
    # the 'required' argument ensures the field exists
    # msg = fields.Nested(SnakemakeUpdateMessage, required=True)
    msg = fields.Str(required=True)
    timestamp = fields.Str(required=True)
    id = fields.Integer(required=False)
