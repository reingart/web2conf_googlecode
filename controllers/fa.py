#############################################
# Submit Financial Aid Application
#############################################

@auth.requires_login()
def application():
    # following idiom from Massimo's profile():
    try:
        you=db.fa.person==auth.user.id
        db.fa['exposes']=db.fa.fields[4:]
        person=db(you).select()[0]
    except:
        if datetime.datetime.today() > FACUTOFF_DATE:
            t2.redirect('index',flash=XML(T('<b><font color="red">Applications are no longer being accepted.</b><br>(Financial Aid Application deadline: 23 February 2009)</font>')))
        form=t2.create(db.fa,vars=dict(person=auth.user.id),onaccept=lambda form: email_fa('created'),next='fa_app')
    else:
        form=t2.update(db.fa,query=you,deletable=False,onaccept=lambda form: email_fa('updated'),next='fa_app')
    # email from here...
    return dict(form=form)