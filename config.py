def mail_config():
    return {
        'MAIL_SERVER': 'smtp.gmail.com',
        'MAIL_PORT': 465,
        'MAIL_USERNAME': 'ajnetworks54779@gmail.com',
        'MAIL_PASSWORD': 'pvwn wvdw lvmk txbn',
        'MAIL_USE_TLS': False,
        'MAIL_USE_SSL': True
    }


def database_config():
    return{
        'MYSQL_HOST': "localhost",
        'MYSQL_USER': "root",
        'MYSQL_PASSWORD': "",
        'MYSQL_DB': "smartvote",
        'SECRET_KEY': "secretKey007"
    }