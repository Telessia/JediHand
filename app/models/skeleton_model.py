import mongoengine as me

class Skeleton_model(me.Document):
    groupname = me.StringField(required=True)
    picpath = me.StringField()
    skeleton = me.StringField()
    default = me.BooleanField()
    command = me.StringField()