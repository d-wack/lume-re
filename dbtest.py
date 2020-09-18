import pymysql.cursors


# Connect to the database
connection = pymysql.connect(host='localhost', user='dotwack', password='redtango1', db='re', cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `pet` (`name`, `owner`,`species`,`sex`) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, ('test', 'test','test','f'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `pet` WHERE `name`=%s"
        cursor.execute(sql, ('Puffball',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()