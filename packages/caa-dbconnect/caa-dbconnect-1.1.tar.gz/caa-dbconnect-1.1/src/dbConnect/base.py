"""
John 3:16
For God so loved the world, that he gave his only begotten Son, that whosoever believeth
in Him should not perish, but have everlasting life. 
"""
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
import datetime as dt
from sqlalchemy.sql import text as sql_text
import json, time, re
jsonblock=r"\:\S{1}"

try:
    from sqlTypes import type_map
    from authorization import Authorization
    from response import DBR
except ModuleNotFoundError:
    from .sqlTypes import type_map
    from .authorization import Authorization
    from .response import DBR

__DOC__ = """
INSTRUCTION:
    
    
Authorization: auth object used to valid your credentials and connect you to the server
    setup user credentials using environment variables for easier setup
    setx DB_UN -your username-
    REQUIRED VARIABLES ARE == DB_UN, DB_PW, DB_HOST, DB_PORT
    
DB: database query object used to run queries
    requests are made in similar syntax to sql, like so:
    response = DB.select('DATABASE','TABLE',{??PARAMS??},COLUMNS,ORDERBY,REVERSE,LIMIT)
    requests:
        - DB.select( database, table, params, columns, orderBy, reverse, limit )
        - DB.insert( database, table, records, newOnly, keyCol )
        - DB.upsert( database, table, records, keyCol )
        - DB.update( database, table, update, params )
        - DB.delete( database, table, params )
    
    params:
        - DB.or_( [ -list of dictionaries- ] ) => this will group together the list under a nested OR like so (SELECT ... WHERE BLAH=BLABLA AND (COL1=VAL2 OR COL2=VAL2))
        - DB.and_( { -dictionary-} ) => this is the and functionality (this is used internally, but if you're building a complicated query, this may help you accomplish it)
                                                                        
        - DB.greaterThan( value, orEqual = False ) -> key > value (if orEqual, then >=)
        - DB.lessThan( value, orEqual = False ) -> key < value
        - DB.after( date, inclusive = False) -> keyDate > date (inclusive will include the provided day)
        - DB.before( date, inclusive = False) -> keyDate < date
        - DB.onDay( date ) -> keyDate = date
        - DB.between (value1, value2) -> key between value1 and value2
        - DB.null() -> key is null
        - DB.not_(method, arguments)
            for example -> DB.not_(DB.null)  for KEY IS NOT NULL |||| DB.not_(DB.between, value1, value2) for KEY NOT BETWEEN value1 AND value2
"""
DEBUG = False
NULLPOOL_LIMIT  = 10_000
DEFAULT_CHUNK   = 25_000
TIMEOUT_SECONDS = 240
POOL_RECYCLE    = 900

class DB():
    
    def __init__(self,
                 auth:Authorization,
                 poolclass = NullPool
                 ):
        self.auth = auth
        self.poolclass    = poolclass
        self.pool_recycle = POOL_RECYCLE
        self.default_db   = 'jupiterdb'
        self.debug        = DEBUG
        
    ### INITIALIZERS
    @classmethod
    def env(cls):
        auth = Authorization.fromEnv()
        obj = cls(auth)
        return obj
     
    ### EXECUTION
    def engine(self, database=None, nullpool=False):
        if not database:
            database = self.default_db
        if nullpool:
            return create_engine(self.auth.uri(database),
                                 poolclass=self.poolclass,
                                 echo_pool= 'debug' if self.debug else False,
                                 connect_args={'connect_timeout': TIMEOUT_SECONDS}
                                 )
        else:
            return create_engine(self.auth.uri(database),
                                 pool_recycle=self.pool_recycle,
                                 echo_pool='debug' if self.debug else False,
                                 connect_args={'connect_timeout': TIMEOUT_SECONDS}
                                 )
    
    
    def run(self, query, database=None, nullpool=False):
        if not database:
            database = self.default_db
        attempt = 0
        while True:
            try:
                data = []
                with self.engine(database, nullpool).connect() as ctx:
                    qry = sql_text(query)
                    result = ctx.execute(qry)
                    ctx.commit()
                    kwargs = dict()
                    kwargs.update({'query':query,
                                   'database':database, 
                                   'returnsRows':result.returns_rows, 
                                   'affectedRows': result.rowcount})
                    if result.returns_rows:
                        hdrs = result.keys()
                        data = result.fetchall()
                        data = [dict(zip(hdrs,x)) for x in data]
                    result.close()
                        
                if len(data) > 0:
                    return DBR(*data,**kwargs)
                else:
                    return DBR(**kwargs)
            except Exception as err:
                if attempt > 5:
                    print(err)
                    break
                time.sleep(5)
                attempt += 1
    
    
    def test_connection(self):
        try:
            _=self.run('show tables','jupiterdb')
            return True
        except:
            return False
    
    ### DATA TYPE HELPERS
    def valConvert(self, k, v, colData, **kwargs):
        col = colData[k]
        kwargs.update(col)
        # used for datatypes on 'write' queries
        val = col['DATA_TYPE'](v, **kwargs)
        return val.SQL
    
    @staticmethod
    def fix_json(value):
        m=re.findall(jsonblock, value)
        for x in m:
            old=x
            new=x.replace(":",": ")
            value = value.replace(old,new)
        return value
    
    @staticmethod
    def sqlValTypes(val, delimiter:str='|', quoteDateTime:bool=False):
        # used for datatypes on 'read' queries
        if str(val).startswith('`') and str(val).endswith('`'):
            return val # this is a 'column'
        if "'" in str(val):
            val = val.replace("'","''")
        if "\\" in r"{}".format(str(val)):
            val = val.replace('\\','\\\\')
            
        if '%' in str(val):
            val = val.replace('%','%%')
        
        if val == None:
            return 'NULL'
        
        if type(val) == str:
            val = DB.fix_json(val)
            return f"'{val}'"
        elif type(val) == bool:
            val = int(val)
            return f"{val}"
        elif type(val) == int:
            return f"{val}"
        elif type(val) == float:
            return f"{val}"
        elif isinstance(val,dict):
            val = json.dumps(val, default=str)
            val = DB.fix_json(val)
            return f"'{val}'"
        elif isinstance(val,list):
            val = f'{delimiter}'.join(val)
            return f"'{val}'"
        elif isinstance(val,set) or isinstance(val,tuple):
            val = list(val)
            val = f'{delimiter}'.join(val)
            return f"'{val}'"
        elif isinstance(val,dt.datetime):
            val = dt.datetime.strftime(val,'%Y-%m-%d %H:%M:%S')
            if quoteDateTime:
                return f"'{val}'"
            else:
                return f"{val}"
        elif isinstance(val,dt.date):
            val = dt.datetime.strftime(val,'%Y-%m-%d')
            if quoteDateTime:
                return f"'{val}'"
            else:
                return f"{val}"
        elif isinstance(val,dt.time):
            date = dt.datetime.now()
            val = date.replace(hour = val.hour,minute=val.minute,second=val.second)
            val = dt.datetime.strftime(val,'%H:%M:%S')
            if quoteDateTime:
                return f"'{val}'"
            else:
                return f"{val}"
        else:
            return f"'{val}'"
    
    
    @staticmethod
    def paramHndlr(k, v):
        if isinstance(v,dict):
            if '_qry' in v and '_val' in v:
                return f"`{k}` {v['_qry']}"
            
        if k == '_OR_' or k == '_AND_':
            return v # this is an n-dimensional grouping, already converted, just pass it back with out the unneeded key
        
        if isinstance(v, list):
            return f"`{k}` {DB.in_(v)['_qry']}"
        
        qry = f"`{k}` = {DB.sqlValTypes(v)}"
        
        return qry
    
    
    ### MINI QUERIES
    def getExistingKeys(self, database, table, keys, keyCol, inverse=False):
        keyList = self.select(database = database, 
                              table    = table, 
                              params   = {keyCol:self.in_(keys)}, 
                              columns  = [ keyCol ])
        keyList = list(set([x[keyCol] for x in keyList.records]))
        if inverse:
            # return the non existing keys only (used mainly for inserting ONLY new records)
            return [x for x in keys if x not in keyList]
        return keyList
    
    
    def getTables(self, database=None):
        if not database:
            database = self.default_db
        return self.run('show tables', database)
    
    
    def convertHdrInfo(self, mapp, value):
        if mapp == 'IS_NULLABLE':
            return value == 'YES'
        elif mapp == 'DATA_TYPE':
            return type_map[str(value).upper()]
        elif mapp == 'COLUMN_TYPE':
            return value.upper()
        else:
            return value
    
    
    def getHeaderInfo(self, database, table):
        if not database:
            database = self.default_db
        hdrQry = f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{table}'"
        hdrRsp = self.run(hdrQry, database)
        res = {x['COLUMN_NAME']: {k : self.convertHdrInfo(k, v) for k,v in x.items()} for x in hdrRsp.records}
        return res
    
    
    ### SELECT
    def select(self, database, table, params = {}, columns = [], 
               orderBy:str = None, reverse = False, distinct = False, 
               limit:int = None, offset:int = None, textual=False):
        if len(columns) > 0:
            columns = [f"`{x}`" for x in columns]
            selCols = ', '.join(columns)
            if distinct:
                selCols = f"DISTINCT {selCols}"
        else:
            selCols = '*'
        qry = f"SELECT {selCols} FROM `{database}`.`{table}`"
        if params:
            qry += ' WHERE '
            paramList = []
            for k,v in params.items():
                paramList.append(DB.paramHndlr(k,v))
            paramText = ' AND '.join(paramList)
            qry += paramText
        if orderBy is not None:
            qry += f" ORDER BY `{orderBy}` {'DESC' if reverse else 'ASC'} "
        if limit is not None and limit!=0:
            qry += f'LIMIT {limit}'
            if offset is not None and offset!=0:
                if orderBy is None:
                    raise Exception("OFFSET BLOCKED BECAUSE 'orderBy':'<column name>' IS MISSING FROM THE ARGUMENTS")
                qry += f' OFFSET {offset}'
        qry += ';'
        if textual:
            return qry
        return self.run(qry,database)
    
    ### INSERT
    def insert(self, database, table, records, newOnly=False, keyCol=None, 
               chunksize:int=DEFAULT_CHUNK, colData:dict=None, textual=False):
        nullpool = len(records) < NULLPOOL_LIMIT
        if newOnly:
            if not keyCol:
                raise Exception("'newOnly' operation only works if you provide the 'keyCol' value.")
            # the following 'getExistingKeys' will only get the non-existing keys
            new = self.getExistingKeys(database, table, [x[keyCol] for x in records], 
                                       keyCol, 
                                       True)
            records = [x for x in records if x[keyCol] in new]
        
        if len(records) == 0:
            if textual:
                return ''
            return DBR(**{'query':'','database':database, 'returnsRows':False, 'affectedRows': 0, 'message':'no new records'})
        remaining=[]
        if chunksize is None:
            chunksize = len(records)
        limiter = min(len(records),chunksize)
        records,remaining = records[:limiter],records[limiter:]
        if colData is None:
            colData = self.getHeaderInfo(database, table)
        
        cols = [f"`{x}`" for x in list(records[0].keys())]
        missing = [x for x in list(records[0].keys()) if x not in list(colData.keys())]
        
        if len(missing) != 0:
            missing = ', '.join(missing)
            raise Exception(f"INVALID COLUMNS = ({missing})")
            
        colText = ', '.join(cols)
        qry = f'INSERT INTO `{database}`.`{table}` ({colText}) VALUES '
        
        rList = []
        for x in records:
            if len(x) != len(cols):
                raise Exception(f"Uneven record sizes detected. Expected {len(cols)}, got {len(x)}")
            cCols = [self.valConvert(k, v, colData) for k,v in x.items()]
            cColText = ', '.join(cCols)
            cLineQry = f"({cColText})"
            rList.append(cLineQry)
        rText = ', '.join(rList)
        qry += rText
        qry += ';'
        if textual:
            return qry
        if len(records)>0:
            rsp = self.run(qry, database, nullpool)
            if len(remaining)>0:
                return self.insert(database, table, remaining, newOnly, keyCol, chunksize, colData=colData, textual=False)
            else:
                return rsp
        return DBR(query=qry, message="FAIL")
    
    ### UPSERT
    def new_upsert(self, database, table, records, keycol, update_mask=[], 
                   chunksize:int=DEFAULT_CHUNK, colData:dict=None, textual=False):
        nullpool = len(records) < NULLPOOL_LIMIT
        if isinstance(keycol, str):
            keycol = [keycol]
        if len(update_mask) == 0:
            update_mask = [x for x in list(records[0].keys()) if x not in keycol]
        else:
            update_mask = [x for x in update_mask if x not in keycol]
            if len(update_mask) == 0:
                raise Exception('Update Mask must contain NON key columns')
        remaining=[]
        if chunksize is None:
            chunksize = len(records)
        limiter = min(len(records),chunksize)
        records,remaining = records[:limiter],records[limiter:]
        if colData is None:
            colData = self.getHeaderInfo(database, table)
        cols = [f"`{x}`" for x in list(records[0].keys())]
        missing = [x for x in list(records[0].keys()) if x not in list(colData.keys())]
        if len(missing) != 0:
            missing = ', '.join(missing)
            raise Exception(f"INVALID COLUMNS = ({missing})")
            
        colText = ', '.join(cols)
        qry = f'INSERT INTO `{database}`.`{table}` ({colText}) VALUES '
        
        rList = []
        for x in records:
            if len(x) != len(cols):
                raise Exception(f"Uneven record sizes detected. Expected {len(cols)}, got {len(x)}")
            cCols = [self.valConvert(k, v, colData) for k,v in x.items()]
            cColText = ', '.join(cCols)
            cLineQry = f"({cColText})"
            rList.append(cLineQry)
        rText = ', '.join(rList)
        qry += rText
        qry += " ON DUPLICATE KEY UPDATE "
        updatelist=[]
        for col in update_mask:
            updatelist.append(f"`{col}`=VALUES(`{col}`)")
        qry += ', '.join(updatelist)
        qry += ';'
        if textual:
            return qry
        if len(records)>0:
            rsp = self.run(qry, database, nullpool)
            if len(remaining)>0:
                return self.new_upsert(database, table, remaining, keycol, update_mask, chunksize, colData=colData, textual=False)
            else:
                return rsp
        return DBR(query=qry, message="FAIL")

    
    def upsert(self, database, table, records, keyCol):
        print("** ** WARNING: DB.upsert IS PLANNED FOR DEPRECATION. USE DB.replace OR DB.new_upsert INSTEAD ** ** ")
        print("** ** WARNING: DB.new_upsert WILL BE RENAMED DB.upsert IN THE NEAR FUTURE ** ** ")
        print("RUN help(db.replace) TO SEE WHAT CHANGES YOU NEED TO MAKE TO MIGRATE TO NEW VERSION")
        try:
            rsp = self.delete(database = database, 
                        table = table, 
                        params = { 
                            keyCol : self.in_( [ x[keyCol] for x in records ] )
                            }
                        )
        except:
            if len(records) == 0:
                raise Exception('No records passed to upsert method')
            raise Exception('upsert error:\n', database, table, records[0], keyCol)
        rsp2 = self.insert(database, table, records)
        rsp2.updated_rows = rsp.affectedRows
        rsp2.inserted_rows = rsp2.affectedRows - rsp2.updated_rows
        return rsp2
    
    def replace(self, database:str, table:str, records:list, keyCols:list|str, 
                params:dict=None, chunksize:int=DEFAULT_CHUNK, colData:dict=None):
        """
        To migrate from db.upsert to db.replace, rename keyCol to keyCols (if using keyword arguments)
        Everything else will stay the same. (replace now offers multi-key replacing, which upsert could not do)
        """
        if chunksize is None:
            chunksize = len(records)
        remaining=[]
        if chunksize is None:
            chunksize = len(records)
        limiter = min(len(records),chunksize)
        records,remaining = records[:limiter],records[limiter:]
        if colData is None:
            colData = self.getHeaderInfo(database, table)
        if isinstance(keyCols, str):
            keyCols = [keyCols]
        if len(records)>0:
            if params is None:
                params = {"_OR_": self.or_([
                    {key:r[key] for key in keyCols}
                    for r in records
                ])}
            rsp = self.delete(database=database, table=table, params=params)
            rsp2 = self.insert(database, table, records, colData=colData, chunksize=chunksize)
            if len(remaining)>0:
                return self.replace(database, table, remaining, keyCols, params, chunksize)
            return rsp2
        else:
            return True
    
    ### UPDATE
    def update(self, database, table, update:dict, params:dict, textual=False):
        cols = self.getHeaderInfo(database, table)
        
        updateVals = [f"{k} = {self.valConvert(k, v, cols)}" for k,v in update.items()]
        updateText = ', '.join(updateVals)
        qry = f"UPDATE `{database}`.`{table}` SET {updateText} WHERE "
        paramList = []
        for k,v in params.items():
            paramList.append(self.paramHndlr(k,v))
        paramText = ' AND '.join(paramList)
        qry += paramText
        qry += ';'
        if textual:
            return qry
        return self.run(qry, database, nullpool=True)
    
    
    
    ### DELETE
    def clearTable(self, database, table, textual=False):
        if not database:
            database = self.default_db
        
        query = f"DELETE FROM `{database}`.`{table}`;"
        if textual:
            return query
        return self.run(query,database=database)
        

    def delete(self, database, table, params, textual=False):
        qry = f"DELETE FROM `{database}`.`{table}`"
        if params:
            qry += ' WHERE '
            paramList = []
            for k,v in params.items():
                paramList.append(self.paramHndlr(k,v))
        
            paramText = ' AND '.join(paramList)
            qry += paramText
        else:
            raise Exception('DELETE requires params/conditions')
        qry += ';'
        if textual:
            return qry
        return self.run(qry,database)
    
    
    def create_table(self, database:str, table:str, columns:list=[]):
        print("THIS FUNCTION IS PLANNED FOR THE FUTURE")
        return NotImplemented
    
    
    ### PARAM BUILDING METHODS
    @staticmethod
    def column(value):
        return f"`{value}`"
    
    @staticmethod
    def equalTo(value, _not = False):
        """SELECT ... WHERE KEY = VALUE === self.select(.....,{'KEY':self.equalTo(value)})"""
        return {'_qry' : f"{'<>' if _not else '='} {DB.sqlValTypes(value)}", 
                '_val' : value, 
                '_not' : _not}
    
    @staticmethod
    def greaterThan(value, orEqual=False, _not = False):
        """SELECT ... WHERE KEY > VALUE === self.select(.....,{'KEY':self.greaterThan(value)})"""
        oper = '>'
        if _not:
            oper = '<'
            orEqual = not orEqual
        return {'_qry' : f"{oper}{'=' if orEqual else ''} {DB.sqlValTypes(value)}", 
                '_val' : value, 
                '_not' : _not}
    
    @staticmethod
    def lessThan(value, orEqual = False, _not = False):
        """SELECT ... WHERE KEY < VALUE === self.select(.....,{'KEY':self.lessThan(value)})"""
        oper = '<'
        if _not:
            oper = '>'
            orEqual = not orEqual
        return {'_qry' : f"{oper}{'=' if orEqual else ''} {DB.sqlValTypes(value)}", 
                '_val' : value, 
                '_not' : _not}
    
    @staticmethod
    def between(value1, value2, _not = False): # not inclusive
        v1 = min([value1, value2])
        v2 = max([value1, value2])
        """SELECT ... WHERE KEY BETWEEN VALUE1 AND VALUE2 === self.select(.....,{'KEY':self.between(VALUE1,VALUE2)})"""
        return {'_qry' : f"{'NOT ' if _not else ''}BETWEEN {DB.sqlValTypes(v1)} AND {DB.sqlValTypes(v2)}", 
                '_val' : (value1,value2), 
                '_not' : _not}
    
    @staticmethod
    def after(date, inclusive = False, _not = False):
        """SELECT ... WHERE DATE_COL > DATE === self.select(.....,{'DATE_COL':self.after(DATE)})"""
        oper = '>'
        if _not:
            oper = '<'
            inclusive = not inclusive
        return {'_qry' : f"{oper}{'=' if inclusive else ''} '{date}'", 
                '_val' : date, 
                '_not' : _not}
    
    @staticmethod
    def before(date, inclusive = False, _not=False):
        """SELECT ... WHERE DATE_COL < DATE === self.select(.....,{'DATE_COL':self.before(DATE)})"""
        oper = '<'
        if _not:
            oper = '>'
            inclusive = not inclusive
        return {'_qry' : f"{oper}{'=' if inclusive else ''} '{date}'", 
                '_val' : date, 
                '_not' : _not}
    
    @staticmethod
    def onDay(date, _not = False):
        """SELECT ... WHERE DATE_COL = DATE === self.select(.....,{'DATE_COL':self.onDay(DATE)})"""
        return {'_qry' : f"{'<>' if _not else '='} '{date}'", 
                '_val' : date, 
                '_not' : _not}
    
    @staticmethod
    def null(_not = False):
        """SELECT ... WHERE KEY IS NULL === self.select(.....,{'KEY':self.null()})"""
        return {'_qry' : f"IS{' NOT ' if _not else ' '}NULL", 
                '_val' : None, 
                '_not' : _not}
    
    @staticmethod
    def in_(items, _not = False):
        if isinstance(items, str):
            if str(items).lower().startswith('select '):
                itemStr = items
            else:
                raise Exception('"IN" multi-queries require a select statement for the internal query')
        else:
            """SELECT ... WHERE KEY IN (VAL1, VAL2, VAL3, ...) === self.select(.....,{'KEY':self.in_( [VAL1, VAL2, VAL3, ...] )})"""
            ITEMS = [DB.sqlValTypes(x) for x in items]
            itemStr = ', '.join(ITEMS)
        return {'_qry' : f"{'NOT ' if _not else ''}IN ({itemStr})", 
                '_val' : items, 
                '_not' : _not}
    
    @staticmethod
    def contains_(value, _not = False):
        """SELECT ... WHERE KEY LIKE %%VALUE%% === self.select(.....,{'KEY':self.contains_(VALUE)})"""
        return {'_qry' : f"{'NOT ' if _not else ''}LIKE '%%{value}%%'", 
                '_val' : value, 
                '_not' : _not}
    
    
    @staticmethod
    def startsWith_(value, _not = False):
        """SELECT ... WHERE KEY LIKE VALUE%% === self.select(.....,{'KEY':self.startsWith_(VALUE)})"""
        return {'_qry' : f"{'NOT ' if _not else ''}LIKE '{value}%%'", 
                '_val' : value, 
                '_not' : _not}
    
    @staticmethod
    def endsWith_(value, _not = False):
        """SELECT ... WHERE KEY LIKE %%VALUE === self.select(.....,{'KEY':self.endsWith_(VALUE)})"""
        return {'_qry' : f"{'NOT ' if _not else ''}LIKE '%%{value}'", 
                '_val' : value, 
                '_not' : _not}
    
    
    @staticmethod
    def regex_(value, _not=False):
        """SELECT ... WHERE KEY REGEXP value === self.select(.....,{'KEY':self.regex_(VALUE)})"""
        return {'_qry' : f"{'NOT ' if _not else ''}REGEXP '{value}'", 
                '_val' : value, 
                '_not' : _not}
    
    
    ### PARAM NEGATION
    @staticmethod
    def not_(func, *args, **kwargs):
        """Inverse any param. not_ is a wrapper function for all parameter-building methods
        examples:
            SELECT ... WHERE KEY IS NOT NULL  =>  self.select(.....,{'KEY':self.not_(null)})
            SELECT ... WHERE KEY IS NOT BETWEEN 2 AND 5 => self.select(.....,{'KEY',self.not_( self.between, 2, 5 )})
            SELECT ... WHERE DATE_COL < YESTERDAY => self.select(.....,{'DATE_COL':self.not_(self.after, YESTERDAY, inclusive = True)})
        """
        kwargs.update({'_not' : True})
        try:
            return func(*args, **kwargs)
        except:
            raise Exception(f"Please wrap the 'not_' method around the desired query type like so: db.not_(db.{func.__name__}, **kwargs)")
            
            
            
    ### NESTED PARAMETER BUILDING METHODS (N-DIMENSIONAL PARAMETER SETS)
    @staticmethod
    def or_(params:list, nested = True):
        """NEST A GROUP OF PARAMETERS USING 'OR'.
        args: 
            - params: list of param dictionaries
            - nested: boolean, adds parenthesis to the set of parameters (needed in complex queries, like key=1 and (this=that or that=this) and key2=2)
                default = True
        
        example:
            SELECT ... WHERE KEY1 = VAL1 AND (KEY2 = 4 OR KEY3 = 5) => 
                self.select(.....,{'KEY1':'VAL1', '_OR_' : self.or_([ {'KEY2':4}, {'KEY3':5} ])})
        """
        kSet = [DB.and_(record, nested = True) for record in params]
        kSetStr = ' OR '.join(kSet)
        if nested:
            return f"({kSetStr})"
        else:
            return kSetStr
    
    @staticmethod
    def and_(params, nested = True):
        """NEST A GROUP OF PARAMETERS USING 'AND'.
        args: 
            - params: dictionary or list (if repeating same key)
            - nested: boolean, adds parenthesis to the set of parameters (needed in complex queries, like key=1 and (this=that or that=this) and key2=2)
                default = True
        
        example:
            SELECT ... WHERE KEY1=VAL1 OR {KEY2=VAL2 AND KEY3=VAL3} => 
                self.select(....., {'_OR_' : self.or_([ {'KEY1':'VAL1'}, {'_AND_': self.and_({'KEY2'='VAL2','KEY3':'VAL3'})} ], nested = False}) 
        """
        if isinstance(params, list):
            kSet = [DB.and_(x, nested=False) for x in params]
        else:
            kSet = [DB.paramHndlr(k, v) for k,v in params.items()]
        qry = ' AND '.join(kSet)
        if nested:
            return f"({qry})"
        else:
            return qry
        
    ### SPECIAL METHODS
    def __doc__(self):
        return print(__DOC__)
    
    def __repr__(self):
        return f"<DataBase Object (user = {self.auth.user})>"