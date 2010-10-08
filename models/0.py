# set user selected language (default spanish)
if request.vars.lang: session.lang=request.vars.lang
T.force(session.lang or "es")


######################################
### PARAMETERS
######################################
import datetime
try:
    from gluon.contrib.gql import *
except ImportError:
    is_gae=False
else:
    is_gae=True

VERSION=0.5
##T.current_languages=['es','es-ar','es-es']

# If Developer Test, turn off email verificaiton and recaptcha checks,
#  db-pooling, use GCO sandbox, etc.:
# DEV_TEST=True   # settings suitable for development work
DEV_TEST=True # Deployed settings

if DEV_TEST:
    DBURI='sqlite://development.db'
    DBPOOLS=0
    # to test translations; example:  http://..../function?force_language=es
    if request.vars.force_language: session.language=request.vars.force_language
    if session.language: T.force(session.language)
else:
    # DBURI set in 0_private.py
    DBURI='sqlite://production.db'
    DBPOOLS=0

response.title='UbuCon Argentina 2010'
response.subtitle='Buenos Aires - 19 y 20 de Noviembre de 2010'
response.footer="""Primeras conferencias en Español de Ubuntu en Argentina (organizado por <a href="http://www.ubuntu-ar.org/">UbuntuAr</a>). <br/>
Más Información: <a href="https://wiki.ubuntu.com/ArgentinaTeam/UbuCon2010">ArgentinaTeam</a>&nbsp;
<a href="https://lists.ubuntu.com/ubuntu-ar">Ubuntu User Group Argentina <ubuntu-ar@lists.ubuntu.com></a>"""
response.keywords='ubuntu, software libre, buenos aires, argentina'
response.description='Hecho con web2py'



# GOOGLEMAP_KEY set in 0_private.py - here just to ensure definition
GOOGLEMAP_KEY='ABQIAAAANoGcCJcC-46KzN8dgwAVFxQM2onOJ6gcAGXVGT4swjtfsK1_mxRQAFcA_jfbaz70v91ye2tVdv8ftA'

# The following GOOGLE items set in 0_private.py - here to ensure defaults:
GOOGLE_MERCHANT_ID=''
GOOGLE_MERCHANT_KEY=''
GOOGLE_SANDBOX=DEV_TEST

FOOD_PREFERENCES=('normal','vegetarian','vegan','kosher','halal')
FOOD_PREFERENCES_LABELS=(T('normal'),T('vegetarian'),T('vegan'),T('kosher'),T('halal'))

T_SHIRT_SIZES=('man/small','man/medium','man/large','man/xlarge','man/2xlarge','man/3xlarge',
               'woman/small','woman/medium','woman/large')
T_SHIRT_SIZES_LABELS=(T("men's/small"),T("men's/medium"),T("men's/large"),T("men's/xlarge"),T("men's/2xlarge"),
                T("men's/3xlarge"),T("women's/small"),T("women's/medium"),T("women's/large"))

# TODAY_DATE is here so that comparizons w/ cutoff dates
#  will work properly anywhere in web2conf
# NOTE: we add 6 hours since our server is EST, and this will cover Hawaii
#  will want to have these times be session time local in next rev.
TODAY_DATE=datetime.datetime.today()
EARLYBIRD_DATE=datetime.datetime(2009,2,22,6,0,0)
PRECONF_DATE=datetime.datetime(2009,3,19,6,0,0)
FACUTOFF_DATE=datetime.datetime(2009,2,24,6,0,0)

### fix this ...
if TODAY_DATE<EARLYBIRD_DATE:  ### early registration!
   ATTENDEE_TYPES=(
     ('gratis',T('Gratuito, $0')),
   )
elif TODAY_DATE<PRECONF_DATE:  ### pre-conference registration!:
   ATTENDEE_TYPES=(
     ('gratis',T('Gratuito, $0')),
   )
else:
   ATTENDEE_TYPES=(
     ('gratis',T('Gratuito, $0')),
   )
if session.manager:
   ATTENDEE_TYPES=(
     ('gratis',T('Gratuito, $0')),
   )
ATTENDEE_TYPE_COST=dict(
     gratis=0.0,
   )
ATTENDEE_TYPE_COST[None]=0.0

TUTORIALS_LIST=(
)
TUTORIALS=dict(TUTORIALS_LIST) ### do not remove

TUTORIALS_CAPS={
}

COST_FIRST_TUTORIAL=120.0
COST_SECOND_TUTORIAL=80.0

ACTIVITY_TYPES=('talk','keynote','panel','plenary','tutorial','summit','open-space','social','break') 
ACTIVITY_CATEGORIES=('desktop','server','netbook','gui','web','herramientas','comunidad','paquetes','instalación','administración')
ACTIVITY_LEVELS=("Beginner","Intermediate","Advanced")
ACTIVITY_DURATION={'talk': 45, 'tutorial': 120}


SPONSOR_LEVELS=("Organizer", "Main Sponsor", "Sponsor")

# verify by email, unless running a developer test:
EMAIL_VERIFICATION= True #not DEV_TEST
EMAIL_SERVER='localhost:25'
EMAIL_AUTH=None # or 'username:password'
EMAIL_SENDER='register@jornadasregionales.org'

# for FA applications / communication
FA_EMAIL_UPDATES=True
FA_EMAIL_TO=EMAIL_SENDER

# for testing:
#  disable recaptcha by setting DEV_TEST at the top of this file:
DO_RECAPTCHA= False #not DEV_TEST
# RECAPTCHA public and private keys are set in 0_private.py
#  - here to ensure defaults:
RECAPTCHA_PUBLIC_KEY=''
RECAPTCHA_PRIVATE_KEY=''

ENABLE_TALKS=True

if True and DEV_TEST:    # for local development
    HOST='localhost:8000'
    HOST_NEXT='localhost:8000'
else:
    HOST=''
    HOST_NEXT=''

HOTELS=('unknown','Hyatt Regency','Crowne Plaza','other','none')

# for badge generation:
TRUETYPE_PATH='/usr/share/fonts/truetype/freefont'
GSFONTS_PATH='/usr/share/fonts/type1/gsfonts/'

EMAIL_VERIFY_SUBJECT=T("%s Registration Confirmation") % response.title
EMAIL_VERIFY_BODY=T("""                                              
Dear Attendee,

To proceed with your registration and verify your email, click on the following link:

%s

--
%s
""") % ("http://%s%s/%%(key)s" % (request.env.http_host, URL(r=request,f='verify')), response.title)

PASSWORD_RETRIEVE_SUBJECT=T("%s Registration Password") % response.title
PASSWORD_RETRIEVE_BODY=T("Your new password is %(password)s")
INVOICE_HEADER = "This is a Conference Invoice!!!"

CONFERENCE_URL=None
CONFERENCE_COORDS=-34.59448,-58.41274



COUNTRIES=['United States', 'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Costa Rica', "C&ocirc;te d'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'North Korea','South Korea', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia and Montenegro', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']
