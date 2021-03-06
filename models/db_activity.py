# -*- coding: utf-8 -*-

######################################
### MANAGE ACTIVITIES ("TALK" PROPOSALS)
######################################

autotranslate = lambda x: T(x) if not x in ("", None) else x

db.define_table('activity',
    Field('authors',label=T("Authors"),default=('%s %s' %(auth.user.first_name, auth.user.last_name)) if auth.user else None),
    Field('title',label=T("Title")),
    Field('type','text',label=T("Type")),
    Field('code', readable=False, writable=False,),
    Field('duration','integer',label=T("Duration in minutes")), # era 45 min
    Field('request_time_extension', 'boolean', readable=False, writable=False, default=False, label=T("Time extension"), comment=T("(explain why)")),
    Field('cc',label=T("cc"), length=512, default="", readable=False, writable=False),
    Field('abstract','text',label=T("Abstract")),
    Field('description','text',label=T("Description"),widget=wysiwyg),
    Field('categories','list:string',label=T("Categories")),
    Field('level','string',label=T("Level"),represent=autotranslate),
    Field('track','string',label=T("Track"),represent=autotranslate),
    Field('logo','upload', comment=T("only used for sprints)")),
    Field('scheduled_datetime','datetime',label=T("Scheduled Datetime"),writable=False,readable=False),
    Field('scheduled_room',label=T("Scheduled Room"),requires=IS_EMPTY_OR(IS_IN_SET(sorted(ACTIVITY_ROOMS.items()))), writable=False,readable=False),
    Field('status',default='pending',label=T("Status"),writable=False,readable=False),
    Field('confirmed','boolean',default=False,writable=False,readable=False),
    Field('video',length=128,label=T('Video'),default='',writable=False,readable=False),
    Field('score','double',label=T("Score"),default=None,readable=False,writable=False),
    Field('created_by',db.auth_user,label=T("Created By"),readable=False,writable=False,default=auth.user.id if auth.user else 0),
    Field('created_on','datetime',label=T("Created On"),readable=False,writable=False,default=request.now),
    Field('created_signature',label=T("Created Signature"),readable=False,writable=False,
             default=('%s %s' % (auth.user.first_name,auth.user.last_name)) if auth.user else ''),
    Field('modified_by','integer',label=T("Modified By"),readable=False,writable=False,default=auth.user.id if auth.user else 0),
    Field('modified_on','datetime',label=T("Modified On"),readable=False,writable=False,default=request.now,update=request.now),
    Field('notes', 'text', comment=T("Additional remarks"), label=T("Notes")),
    Field('license', 'string', default="CC BY-SA, Atribución - Compartir derivadas de la misma forma.", label=T("License")),
    format='%(title)s',
    migrate=migrate, fake_migrate=fake_migrate)

db.define_table("partaker", Field("activity", db.activity),
                Field("user_id", db.auth_user),
                Field("add_me", "boolean", default=True, comment=T("Confirm my assistance")),
                Field("comment", "text", comment=T("Write a comment for the project's owner")),
                migrate=migrate, fake_migrate=fake_migrate)

if request.controller != 'appadmin':
    db.activity.description.represent=lambda value: XML(value)
db.activity.title.requires=[IS_NOT_EMPTY(), IS_NOT_IN_DB(db,'activity.title')]
db.activity.authors.requires=IS_NOT_EMPTY()
db.activity.status.requires=IS_IN_SET(['pending','accepted','rejected', 'declined'])
db.activity.type.requires=IS_IN_SET([(k, T(k)) for k in ACTIVITY_TYPES])
db.activity.type.default=None
db.activity.level.requires=IS_IN_SET([(k, T(k)) for k in ACTIVITY_LEVELS])
db.activity.level.default=ACTIVITY_LEVELS[0]
db.activity.track.requires=IS_IN_SET([(k, T(k)) for k in ACTIVITY_TRACKS])
db.activity.track.default=ACTIVITY_TRACKS[0]
db.activity.abstract.requires=IS_NOT_EMPTY()
db.activity.abstract.represent=lambda x: MARKMIN(x, sep="br")
db.activity.abstract.comment= SPAN(T("WIKI format: "), A('MARKMIN', _target='_blank',
     _href="http://web2py.com/examples/static/markmin.html",))
db.activity.description.requires=IS_NOT_EMPTY()
db.activity.categories.requires=IS_IN_SET(ACTIVITY_CATEGORIES,multiple=True)
##db.activity.displays=db.proposal.fields
db.activity.status.writable=db.activity.status.readable=auth.has_membership('manager')
db.activity.scheduled_datetime.writable=db.activity.scheduled_datetime.readable=auth.has_membership('manager')
db.activity.video.writable=db.activity.video.readable=auth.has_membership('reviewer')
db.activity.scheduled_datetime.writable=db.activity.scheduled_datetime.readable=auth.has_membership('manager')
db.activity.scheduled_room.writable=db.activity.scheduled_room.readable=auth.has_membership('manager')
db.activity.created_by.writable=db.activity.created_by.readable=auth.has_membership('manager')
db.activity.scheduled_room.represent = lambda x: x and ACTIVITY_ROOMS[int(x)] or ''

db.activity.represent=lambda activity: \
   A('[%s] %s' % (activity.status,activity.title),
     _href=URL(r=request,c='activity',f='display',args=[activity.id]))

db.activity.type.represent=lambda activity_type: T(activity_type and activity_type.replace("_", " ") or '')
db.activity.duration.represent=lambda activity_duration: activity_duration and ("%s min" % activity_duration) or 'n/a'

db.activity.notes.default = "Tipo de público: \nConocimientos previos: \nRequisitos Especiales: (hardware, materiales, ayuda financiera)"

db.define_table('activity_archived',db.activity,Field('activity_proposal',db.activity),
                migrate=migrate, fake_migrate=fake_migrate)

db.define_table('attachment',
   Field('activity_id',db.activity,label=T('ACTIVITY'),writable=False),
   Field('name','string',label=T('Name')),
   Field('description','text',label=T('Description')),
   Field('file','upload',label=T('File')),
   Field('file_data','blob',default=''),
   Field('filename'),
   Field('created_by','integer',label=T("Created By"),readable=False,writable=False,default=auth.user.id if auth.user else 0),
   Field('created_on','datetime',label=T("Created On"),readable=False,writable=False,default=request.now),
   migrate=migrate, fake_migrate=fake_migrate)
db.attachment.name.requires=IS_NOT_EMPTY()
db.attachment.file.requires=IS_NOT_EMPTY()
db.attachment.filename.requires=IS_NOT_EMPTY()
db.attachment.filename.comment=T("(new filename for downloads)")

db.define_table('comment',
   Field('activity_id',db.activity,label=T('ACTIVITY'),writable=False),
   Field('body','text',label=T('Body')),
   Field('created_signature',label=T("Created Signature"),readable=False,writable=False,
             default=('%s %s' % (auth.user.first_name,auth.user.last_name)) if auth.user else ''),
   Field('created_by','integer',label=T("Created By"),readable=False,writable=False,default=auth.user.id if auth.user else 0),
   Field('created_on','datetime',label=T("Created On"),readable=False,writable=False,default=request.now),
   migrate=migrate, fake_migrate=fake_migrate)
db.comment.body.requires=IS_NOT_EMPTY()

db.define_table('review',
   Field('activity_id',db.activity,label=T('ACTIVITY'),writable=False),
   Field('rating','integer',label=T('Rating'),default=0),
   Field('body','text',label=T('Body'),comment="Mensaje opcional para el autor / organizadores"),
   Field('created_by','integer',label=T("Created By"),readable=False,writable=False,default=auth.user.id if auth.user else 0),
   Field('created_signature',label=T("Created Signature"),readable=False,writable=False,
             default=('%s %s' % (auth.user.first_name,auth.user.last_name)) if auth.user else ''),
   Field('created_on','datetime',label=T("Created On"),readable=False,writable=False,default=request.now),
   migrate=migrate, fake_migrate=fake_migrate)
#db.review.body.requires=IS_NOT_EMPTY()
db.review.rating.requires=IS_IN_SET([x for x in range(0,6)])

db.define_table('author',
    Field('user_id', db.auth_user),
    Field('activity_id', db.activity),
    Field('created_by','integer',label=T("Created By"),readable=False,writable=False,default=auth.user.id if auth.user else 0),
    Field('created_on','datetime',label=T("Created On"),readable=False,writable=False,default=request.now),
    migrate=migrate, fake_migrate=fake_migrate)

def user_is_author(activity_id=None):
    if not auth.is_logged_in() or (not request.args and activity_id is None) or not request.args[0].isdigit():
        return False
    if activity_id is None:
        activity_id = request.args[0]
    if db((db.author.user_id==auth.user_id)&(db.author.activity_id==activity_id)).count():
        return True

def user_is_author_or_manager(activity_id=None):
    allowed = False
    if activity_id is not None:
        project = db.activity[activity_id]
        if project is not None:
            if project.created_by == auth.user_id:
                allowed = True
            elif auth.has_membership(role="manager"):
                allowed = True
    return allowed

def activity_is_accepted():
    if not request.args or not request.args[0].isdigit():
        return False
    if db((db.activity.id==request.args[0])&(db.activity.status=='accepted')).count():
        return True

# TODO: enhance with proper tables...
TUTORIALS_LIST= cache.ram(request.env.path_info + ".tutorials", 
                                   lambda: [row.title for row in db(db.activity.status=='accepted').select(db.activity.title, orderby=db.activity.title)], 
                                   time_expire=60*5)

class IS_IN_SET_NOT_EMPTY(IS_IN_SET):
    def __call__(self, value):
        (values, error) = IS_IN_SET.__call__(self,value)
        if not values:
            return (values, self.error_message)
        else:
            return (values, error)
db.auth_user.tutorials.requires=IS_IN_SET(TUTORIALS_LIST,multiple=True)
db.auth_user.tutorials.comment=SPAN(T('(seleccione su preferencia de charlas para la organización del evento; '),
A('más información',_target='_blank',_href='/2011/activity/accepted'),T(", la disponibilidad y horarios pueden variar sin previo aviso)"))

ACTIVITY_LEVEL_HINT = {}
for i, level in enumerate(ACTIVITY_LEVELS):
    ACTIVITY_LEVEL_HINT[level] = XML("&loz;"* (i+1),)

db.activity.code.requires = IS_EMPTY_OR(IS_NOT_IN_DB(db, db.activity.code))
