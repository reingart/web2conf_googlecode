# coding: utf8

######################################
### Sponsorship
######################################

db.define_table( 'sponsor',
   Field('name',label=T("Name"),requires=IS_NOT_IN_DB(db,'sponsor.name')),
   Field('number','integer',default=0,requires=IS_NOT_EMPTY(),label=T("Number")),
   Field('level','string',requires=IS_IN_SET(SPONSOR_LEVELS), label=T("Level")),
   Field('logo','upload'),
   Field('url','string',requires=IS_URL()),
   Field('contact','string',requires=IS_EMAIL(),label=T("Contact"), comment="email"),   
   Field('alt','string',requires=IS_NOT_EMPTY()),
   Field('image','upload', comment="Big logo for sponsors page"),
   Field('text','text', comment="Long text for program and sponsors page"),
   Field('ad','upload', comment="Ad image for the program guide (optional)"),
   Field('notes','text', comment="Phone number and other comments"),
   Field('active','boolean', default=False, writable=auth.has_membership(role="manager"), readable=False),
   Field('created_by',db.auth_user,label=T("Created By"),readable=False,writable=False,default=auth.user.id if auth.user else 0),
   Field('created_on','datetime',label=T("Created On"),readable=False,writable=False,default=request.now),
   Field('created_signature',label=T("Created Signature"),readable=False,writable=False,
            default=('%s %s' % (auth.user.first_name,auth.user.last_name)) if auth.user else ''),
   Field('modified_by','integer',label=T("Modified By"),readable=False,writable=False,default=auth.user.id if auth.user else 0),
   Field('modified_on','datetime',label=T("Modified On"),readable=False,writable=False,default=request.now,update=request.now),
   migrate=migrate, fake_migrate=fake_migrate)

# sponsor logo in badge:
auth.settings.extra_fields['auth_user'] = [
    Field('sponsor_id',"reference sponsor", label=T('Sponsor'), 
          readable=ENABLE_BADGE, writable=ENABLE_BADGE,
          requires=IS_EMPTY_OR(IS_IN_DB(db, db.sponsor, '%(name)s')),
          comment=T("(logo for badge)"),
          )
    ]

