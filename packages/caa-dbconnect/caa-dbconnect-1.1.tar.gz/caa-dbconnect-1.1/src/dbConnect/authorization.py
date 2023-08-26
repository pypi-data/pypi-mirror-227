# -*- coding: utf-8 -*-
class Authorization: # wpd-specific helper
    def __init__(self,
                 user:str,
                 password:str,
                 host:str,
                 port:int,
                 database:str,
                 connector_type:str='pymysql',
                 db_type:str='mysql'
                 ):
        self.user            = user
        self.password        = password
        self.db_type         = db_type
        self.connector_type  = connector_type
        self.host            = host
        self.port            = int(port)
        self.database        = database
    
    @classmethod
    def fromEnv(cls, Creds):
        obj = cls(user     = Creds.get('db_un'),
                  password = Creds.get('db_pw'),
                  host     = Creds.get('db_host'),
                  port     = Creds.get('db_port'),
                  database = 'oetrader')
        return obj   

    @property
    def header(self):
        return {'user'          : self.user,
                'password'      : self.password,
                'db_type'       : self.db_type,
                'connector_type': self.connector_type,
                'host'          : self.host,
                'port'          : self.port,
                'database'      : self.database}

    def uri(self,database):
        hdr  = self.header
        msg  = f"{hdr['db_type']}+{hdr['connector_type']}://"
        msg += f"{hdr['user']}:{hdr['password']}@"
        msg += f"{hdr['host']}:{hdr['port']}/{database}"
        return msg