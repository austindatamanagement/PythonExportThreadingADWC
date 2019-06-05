from __future__ import print_function



import cx_Oracle

import csv

import time

import datetime

pool = cx_Oracle.SessionPool("username", "Password",

       "service_name", 2, 5, 1, threaded = True)

#csvf = open('ficob_data.csv', 'w')

#csv_writer = csv.writer(csvf,delimiter='|')

conn = pool.acquire()

cursor = conn.cursor()

#cursor.arraysize = 80000

print("TheLongQuery(): beginning execute...")

print("Starting to dump data to object storage!\n")

start_time = time.time()

now = datetime.datetime.now()

print("Start time :")

print (now)



cursor.execute("""

declare

  p_file utl_file.file_type;

begin

  p_file := utl_file.fopen( 'DATA_PUMP_DIR', 'test_export_python1.dmp', 'w' );

  for c in (select * from sales WHERE ROWNUM <= 10)

  loop
    utl_file.put_line(p_file, c.cust_id );
  end loop;

  utl_file.fclose(p_file);

  dbms_cloud.put_object( 

    'OBJ_STORE_CRED', 

    'swift URL to Object Storage/test_file.txt',

    'DATA_PUMP_DIR',

    'test_file.txt' );

    

end;

                """)

print("TheLongQuery(): done execute...")



elapsed_time = time.time() - start_time

print("All done!\n")

now = datetime.datetime.now()

print("End time : ")

print (now)

print("Total time in seconds to finish : ")

print(elapsed_time)

print("\n")


