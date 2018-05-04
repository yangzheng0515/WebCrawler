# -*- coding:utf-8 -*-
import MySQLdb
import datetime

#封装MySQLdb类基本操作mysqldb
# 参考：http://blog.csdn.net/justdoithai/article/details/52757015


class mysqldb:
        conn = ''
        cursor = ''
        def __init__(self,host1='localhost',user1='root',passwd1='www',database1='test',charset1='utf8'):
            try:
            print 'init_ ok'
                self.conn=MySQLdb.connect(host=host1,user=user1,passwd=passwd1,db=database1,port=3306,charset=charset1);
                self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            except MySQLdb.Error,e:
                error = 'Connect failed! ERROR (%s): %s' %(e.args[0],e.args[1])
                    print error
                    sys.exit()
        #针对读操作返回结果集
        def _exeCute(self,sql=''):
            try:
                self.cursor.execute(sql)
                records = self.cursor.fetchall()
                return records
            except MySQLdb.Error,e:
                error = 'MySQL execute failed! ERROR (%s): %s' %(e.args[0],e.args[1])
                    print error
                    #sys.exit()
        #针对更新,删除,事务等操作失败时回滚
        def _exeCuteCommit(self,sql=''):
            try:
                self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
                self.conn.commit()
            except MySQLdb.Error,e:
                self.conn.rollback()
                error = 'MySQL execute failed! ERROR (%s): %s' %(e.args[0],e.args[1])
                    print error
                    #sys.exit()
        #创建表
        #tablename:表名称,attr_dict:属性键值对,constraint:主外键约束
        #attr_dict:{'book_name':'varchar(200) NOT NULL'...}
        #constraint:PRIMARY KEY(`id`)
        def _createTable(self,table,attr_dict,constraint):
            sql = ''
            sql_mid = '`id` bigint(11) NOT NULL AUTO_INCREMENT,'
            for attr,value in attr_dict.items():
                sql_mid = sql_mid + '`'+attr + '`'+' '+ value+','
            sql = sql + 'CREATE TABLE IF NOT EXISTS %s ('%table
            sql = sql + sql_mid
            sql = sql + constraint
            sql = sql + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'
            print '_createTable:'+sql
            self._exeCuteCommit(sql)

        #查询表内容
        #cond_dict:{'name':'xiaoming'...}
        #order:'order by id desc'
        def _select(self,table,cond_dict='',order=''):
            consql = ' '
        if cond_dict!='':
                    for k,v in cond_dict.items():
                        consql = consql+k+'='+v+' and'
                consql = consql + ' 1=1 '
            sql = 'select * from %s where '%table
            sql = sql + consql + order
            print '_select:'+sql
            return self._exeCute(sql)

        #插入单条数据
        def _insert(self,table,attrs,value):
            #values_sql = ['%s' for v in attrs]
            attrs_sql = '('+','.join(attrs)+')'
            values_sql = ' values('+','.join(value)+')'
            sql = 'insert into %s'%table
            sql = sql + attrs_sql + values_sql
        print '_insert:'+sql
            self._exeCuteCommit(sql)
        #插入多条数据
        #attrs:[id,name,...]
        #values:[[1,'jack'],[2,'rose']]
        def _insertMany(self,table,attrs,values):
            values_sql = ['%s' for v in attrs]
            attrs_sql = '('+','.join(attrs)+')'
            values_sql = ' values('+','.join(values_sql)+')'
            sql = 'insert into %s'%table
            sql = sql + attrs_sql + values_sql
            print '_insertMany:'+sql
            try:
            print sql
            #print values
            for i in range(0,len(values),20000):
                    self.cursor.executemany(sql,values[i:i+20000])
                    self.conn.commit()
            except MySQLdb.Error,e:
                self.conn.rollback()
                error = '_insertMany executemany failed! ERROR (%s): %s' %(e.args[0],e.args[1])
                    print error
                    sys.exit()
        def _now(self):
            now0 = datetime.datetime.now()
            now = now0.strftime('%Y-%m-%d %H:%M:%S')
            print now
        def _close(self):
            self.cursor.close()
            self.conn.close()
    def __del__(self):
        self._close()


if __name__ == '__main__':
    a = mysqldb('192.168.1.2','root','666','test','utf8')
    a._now()
    table='test_mysqldb'
    attrs={'name':'varchar(200) DEFAULT NULL','age':'int(11) DEFAULT NULL'}
    constraint='PRIMARY KEY(`id`)'
    a._createTable(table,attrs,constraint)
    col = ['name','age']
    val = ['\'xiegonghai\'','25']
    a._insert('test_mysqldb',col,val)
    print(a._select(table))