from marshmallow import Schema, fields


class SnakemakeUpdateForm(Schema):

    """ /api/note - POST

    Parameters:
     - title (str)
     - note (str)
     - user_id (int)
     - time_created (time)
    """
    # the 'required' argument ensures the field exists
    title = fields.Str(required=True)
    note = fields.Str(required=True)
    user_id = fields.Int(required=True)
    time_created = fields.DateTime(required=True)
