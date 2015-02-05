# coding: utf8

if ENABLE_EXPENSES:

    db.define_table( 'expense_form',
        Field( 'person', db.auth_user ),
        Field( 'event','string', length=20, default='PyCon 09'),
        Field( 'created_on','datetime'),
        migrate=migrate,
    )
    
    db.expense_form.person.requires=IS_IN_DB(db,'auth_user.id','%(name)s [%(id)s]')
    
    db.define_table( 'expense_item',
        Field( 'exp_form', db.expense_form ),
        Field( 'seq', 'integer', ),
        Field( 'receipt_no', 'integer', default=1 ),
        Field( 'receipt_item', 'integer', default=1 ),
        Field( 'acct_code','string', length=20, default='video'),
        Field( 'description', 'text', default='' ),
        Field( 'serial_no', 'string', length=30, default='' ),
        Field( 'location', 'text', default='' ),
        Field( 'amount', 'double', default='0.00'),
        migrate=migrate)
    
    db.expense_item.exp_form.requires=IS_IN_DB(db,'expense_form.person','%(id)s')
