# [sql 基础](../../webENGI/Subjict/sql_base.md)
# pymysql 模块
1. 建立数据库连接

    `pymysql.connect(host,port,user,password,database,charset)`

2. 创建游标

    `counnect对象.coursor()`

    需要游标来查询数据库中的数据，也需要游标来返回查询数据

3. 执行 sql 语句

    `游标对象.execute("sql 语句")`

4. 获取返回数据

    1. 获取结果集的下一行.返回元组

        `游标对象.fetchone()`

    2. 获取指定返回的个数. 返回元组，默认取一个

        `游标对象.fetchmany([参数])`

    3. 返回剩下的所有行,如果走到末尾,就返回空元组,否则返回一个元组,其元素是每一行的记录封装的一个元组

        `游标对象.fetchall()`

    4. 返回当前行号
        
        `游标对象.rownumber()` 
    
    5. 返回总的行数

        `游标对象.rowcount()`

8. 关闭游标与连接

    `游标对象.close()`

    `counnect对象.close()`


# Connection类方法

`connect()` 方法传参就是在给 `Connection` 类的 `_init_` 初始化魔术方法参数

`Connection` 类提供了三个方法： `begin` 开始事务， `commit` 提交事务， `rollback` 回滚事务，如果通过 `sql` 语句对数据库中的数据进行了修改， 则需要提交事务。

- `rollback()` 是个很重要的方法，正确的使用 `rollback` 可以避免 `commit` 提交事务的时候发生错误导致程序中断。主要使用方式：结合try except捕获异常，将事务进行rollback回滚

eg. 数据库插入操作
```sql
# !/usr/bin/python3
 
import pymysql
 
# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='testuser',
                     password='test123',
                     database='TESTDB')
 
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
 
# SQL 插入语句
sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
try:
   # 执行sql语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
except:
   # 如果发生错误则回滚
   db.rollback()
 
# 关闭数据库连接
db.close()
```