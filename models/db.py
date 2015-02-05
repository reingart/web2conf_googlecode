from gluon.tools import *
import uuid, datetime, re, os, time, stat
now=datetime.datetime.now()

migrate = True # DEV_TEST
fake_migrate = False

if SUSPEND_SERVICE:
    raise HTTP(503, "<html><body><h3>Service is momentarily unavailable</h3></body></html>")

if is_gae:
    db=GQLDB()
    session.connect(request,response,db=db)
else:
    db=DAL(DBURI, pool_size=20)

PAST=datetime.datetime.today()-datetime.timedelta(minutes=1)

#### cleanup sessions
##ps=os.path.join(request.folder,'sessions')
##try: [os.unlink(os.path.join(ps,f)) for f in os.listdir(ps) if os.stat(os.path.join(ps,f))[stat.ST_MTIME]<time.time()-3600]
##except: pass
#### end cleanup sessions

def wysiwyg(field,value):
    return DIV(field.name,TEXTAREA(_name=field.name, _cols="60", value=value,
                                   _id="wysiwyg",
                                   _style="width: 810px; height: 200px;"))


######################################
### PERSON
######################################

db.define_table('auth_user',
    ##Field('username', length=512, default='', label=T('Username')),
    Field('first_name',length=128,label=T('First Name')),
    Field('last_name',length=128,label=T('Last Name')),
    Field('email',length=128),
    Field('password','password',default='',label=T('Password'),readable=False),
    Field('level','text',label=T('Python knowledge level'),requires=IS_IN_SET(('principiante','intermedio','avanzado'))),
    Field('tutorials','list:string',label=T('Tutorials'),readable=False,writable=False),
    Field('dni','integer'),
    Field('certificate','boolean',default=False,label=T('I want a certificate of attendance'),readable=False,writable=False),
    Field('address',length=255,label=T('Mailing Address'),default=''),
    Field('city',label=T('City'),default=''),
    Field('state',label=T('State'),default='Buenos Aires'),
    Field('country',label=T('Country'),default='Argentina'),
    Field('zip_code',label=T('Zip/Postal Code'),default=''),    
    Field('phone_number',label=T('Phone Number'),comment=T('(cellphone)')),
    Field('include_in_delegate_listing','boolean',default=True,label=T('Include in Delegates List'),readable=False,writable=False),
    Field('sponsors','boolean',default=True,label=T('Contacto con Auspiciantes'),readable=False,writable=False),
    Field('twitter_username',length=64,label=T('Twitter username'),default=''),
    Field('personal_home_page',length=128,label=T('Personal Home Page'),default=''),
    Field('company_name',label=T('Entity Name'),default=''),
    Field('company_home_page',length=128,label=T('Entity Home Page'),default=''),
    Field('badge_line1',label=T('Badge Line 1'),default='',readable=False,writable=False),
    Field('badge_line2',label=T('Badge Line 2'),default='',readable=False,writable=False),
    Field('t_shirt_size',label=T('T-shirt Size'),readable=False,writable=False),
    Field('attendee_type',label=T('Registration Type'),default=ATTENDEE_TYPES[0][0],readable=False,writable=False),
    Field('discount_coupon',length=64,label=T('Discount Coupon'), readable=False,writable=False),
    Field('donation','double',default=0.0,label=T('Donation to PyAr'),readable=False,writable=False),
    Field('amount_billed','double',default=0.0,readable=False,writable=False),
    Field('amount_added','double',default=0.0,readable=False,writable=False),
    Field('amount_subtracted','double',default=0.0,readable=False,writable=False),
    Field('amount_paid','double',default=0.0,readable=False,writable=False),
    Field('amount_due','double',default=0.0,readable=False,writable=False),
    Field('resume','text',label=T('Resume (Bio)'),readable=True,writable=True),
    Field('photo','upload',label=T('Photo'), readable=True,writable=True),
    Field('cv','upload',label=T('CV'),readable=True,writable=True),
    Field('speaker','boolean',default=False,readable=False,writable=False),
    Field('session_chair','boolean',default=False,readable=False,writable=False),
    Field('manager','boolean',default=False,readable=False,writable=False),
    Field('reviewer','boolean',default=True,readable=False,writable=False),
    Field('latitude','double',default=0.0,readable=False,writable=False),
    Field('longitude','double',default=0.0,readable=False,writable=False),
    Field('confirmed','boolean',default=False,writable=False,readable=False),
    Field('registration_key',length=64,default='',readable=False,writable=False),
    Field('reset_password_key',length=64,default='',readable=False,writable=False),
    Field('reset_password_key', length=512, writable=False, readable=False, default=''),
    Field('registration_id', length=512, writable=False, readable=False, default=''),
    Field('created_by_ip',readable=False,writable=False,default=request.client),
    Field('created_on','datetime',readable=False,writable=False,default=request.now),
    ##Field('cena_viernes','boolean', comment="-con cargo-"),
    ##Field('cena_sabado','boolean', comment="sin cargo para los disertantes + organizadores"),
    ##Field('cena_obs','string', comment="indique si quiere invitar a la cena a familiares o amigos (cant. de reservas) -con cargo-"),
    format="%(last_name)s, %(first_name)s (%(id)s)",
    migrate=migrate, fake_migrate=fake_migrate)

# web2py planet model

db.define_table("feed",
    Field("name", label=T("name")),
    Field("author", label=T("author")),
    Field("email", requires=IS_EMAIL(), label=T("email")),
    Field("url", requires=IS_URL(), comment=T("RSS/Atom feed")),
    Field("link", requires=IS_URL(), comment=T("Blog href"), label=T("link")),
    Field("general", "boolean", comment=T("Many categories (needs filters)"), label=T("general")),
    migrate=migrate, fake_migrate=fake_migrate)

PLANET_FEEDS_MAX = 12

# end of web2py planet model


##db.auth_user.username.comment=T('(required)')
db.auth_user.first_name.comment=T('(required)')
db.auth_user.last_name.comment=T('(required)')
db.auth_user.email.comment=T('(required)')
db.auth_user.password.comment=not JANRAIN and T('(required)') or T('(optional)')
db.auth_user.resume.widget=lambda field,value: SQLFORM.widgets.text.widget(field,value,_cols="10",_rows="8")
db.auth_user.photo.comment=T('Your picture (100px)')
db.auth_user.dni.comment=T('(required if you need a certificate)')
#db.auth_user.certificate.comment=XML(A(str(T('El Costo de Certificado es $x.-')) + '[2]',_href='#footnote2'))
db.auth_user.t_shirt_size.requires=IS_IN_SET(T_SHIRT_SIZES,T_SHIRT_SIZES_LABELS)
db.auth_user.t_shirt_size.comment=XML(A(str(T('cost TBD')) + ' [2]',_href='#footnote2'))

db.auth_user.level.comment=T("")

db.auth_user.zip_code.comment=T('(for map)')

db.auth_user.company_name.comment=T('company, university')

db.auth_user.sponsors.comment=XML(A(str(T('Privacy policy')) + ' [1]',_href='#footnote1'))
#db.auth_user.include_in_delegate_listing.comment=T('If checked, your Name, Company and Location will be displayed publicly')
db.auth_user.include_in_delegate_listing.comment=XML(A(str(T('Privacy policy')) + ' [1]',_href='#footnote1'))
db.auth_user.resume.comment=T('Short Biografy and reference (required for speakers)')

db.auth_user.cv.comment=XML(A(str(T('Job Fair')) + ' [3]',_href='#footnote3'))

##db.auth_user.username.requires=[IS_LENGTH(512),IS_NOT_EMPTY(), IS_NOT_IN_DB(db,'auth_user.username')]
db.auth_user.first_name.requires=[IS_LENGTH(128),IS_NOT_EMPTY()]
db.auth_user.last_name.requires=[IS_LENGTH(128),IS_NOT_EMPTY()]

## Virtual fields:
import md5
# security hash can be used to validate user_id in public url (ie. schedule bookmark)
db.auth_user.security_hash = Field.Virtual(lambda row:  "created_by_ip" in row.auth_user and md5.new("%s%s" % (row.auth_user.created_by_ip, row.auth_user.created_on)).hexdigest())

auth=Auth(globals(),db)                      # authentication/authorization

db.auth_user.password.requires=[CRYPT()]
if not JANRAIN:
    db.auth_user.password.requires.append(IS_NOT_EMPTY())

auth.settings.table_user=db.auth_user
auth.settings.cas_domains = None        # disable CAS
auth.define_tables(username=False, migrate=migrate)
auth.settings.controller='user'
auth.settings.login_url=URL(r=request,c='user',f='login')
#auth.settings.on_failed_authorization=URL(r=request,c='user',f='login')
auth.settings.logout_next=URL(r=request,c='default',f='index')
auth.settings.register_next=URL(r=request,c='default',f='index')
auth.settings.verify_email_next=URL(r=request,c='default',f='index')
auth.settings.profile_next=URL(r=request,c='user',f='profile')
auth.settings.retrieve_password_next=URL(r=request,c='user',f='login')
auth.settings.change_password_next=URL(r=request,c='default',f='index')
auth.settings.logged_url=URL(r=request,c='user',f='profile')
auth.settings.create_user_groups = False
#sauth.settings.actions_disabled = ['register', 'change_password','request_reset_password']
auth.settings.reset_password_requires_verification = True
auth.settings.formstyle = "bootstrap"
auth.settings.label_separator = ""


if EMAIL_SERVER:
    mail=Mail()                                  # mailer
    mail.settings.server=EMAIL_SERVER
    mail.settings.sender=EMAIL_SENDER
    mail.settings.login=EMAIL_AUTH
    auth.settings.mailer=mail                    # for user email verification
    auth.settings.registration_requires_verification = EMAIL_VERIFICATION
    auth.messages.verify_email_subject = EMAIL_VERIFY_SUBJECT
    auth.messages.verify_email = EMAIL_VERIFY_BODY
    
##if RECAPTCHA_PUBLIC_KEY:
##    auth.settings.captcha=Recaptcha(request, RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY)
auth.define_tables(migrate=migrate, fake_migrate=fake_migrate)

db.auth_membership.user_id.represent=lambda v: "%(last_name)s, %(first_name)s (%(id)s)" % db.auth_user[v]

db.auth_user.email.requires=[IS_LENGTH(128),IS_EMAIL(),IS_NOT_IN_DB(db,'auth_user.email')]
db.auth_user.personal_home_page.requires=[IS_LENGTH(128),IS_NULL_OR(IS_URL())]
db.auth_user.company_home_page.requires=[IS_LENGTH(128),IS_NULL_OR(IS_URL())]
db.auth_user.country.requires=IS_IN_SET(COUNTRIES)
db.auth_user.created_by_ip.requires=\
    IS_NOT_IN_DB(db(db.auth_user.created_on>PAST),'auth_user.created_by_ip')
db.auth_user.registration_key.default=str(uuid.uuid4())

db.auth_user.reviewer.writable=db.auth_user.reviewer.readable=auth.has_membership('manager')
db.auth_user.speaker.writable=db.auth_user.speaker.readable=auth.has_membership('manager')

# Enable tutorial selection after proposal deadline
##db.auth_user.tutorials.writable = db.auth_user.tutorials.readable = TODAY_DATE>PROPOSALS_DEADLINE_DATE
##db.auth_user.tutorials.label = "Charlas Preferidas"

# Enable simplified registration (no password asked)
if SIMPLIFIED_REGISTRATION and TODAY_DATE>REVIEW_DEADLINE_DATE and request.controller=='user' and request.function=='register':
    db.auth_user.password.readable = False
    db.auth_user.password.writable = False
    ##db.auth_user.confirmed.default = False
else:
    db.auth_user.confirmed.default = False
    db.auth_user.password.comment = "(nueva para este sitio)"
    ##db.auth_user.confirmed.readable = True
    ##db.auth_user.confirmed.writable = True
    ##db.auth_user.address.requires = IS_NOT_EMPTY()

db.auth_user.confirmed.label = T("Confirm attendance")

# badge:
if ENABLE_BADGE:
    db.auth_user.badge_line1.readable = False
    db.auth_user.badge_line2.readable = False
    db.auth_user.badge_line1.writable = False
    db.auth_user.badge_line2.writable = False

    db.auth_user.badge_line1.comment = T("(i.e. position)")
    db.auth_user.badge_line2.comment = T("(ie. interests)")
