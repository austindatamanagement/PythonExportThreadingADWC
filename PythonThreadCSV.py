My script on python



#------------------------------------------------------------------------------

# Threads.py

#   This script demonstrates the use of threads with cx_Oracle. A session pool

# is used so that multiple connections are available to perform work on the

# database. Only one operation (such as an execute or fetch) can take place at

# a time on a connection. In the below example, one of the threads performs

# dbms_lock.sleep while the other performs a query.

#

# This script requires cx_Oracle 2.5 and higher.

#------------------------------------------------------------------------------



from __future__ import print_function



import cx_Oracle

import csv

import time

import datetime

pool = cx_Oracle.SessionPool("admin", "Fico12345678",

       "ficodb_high", 2, 5, 1, threaded = True)

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



  p_file := utl_file.fopen( 'DATA_PUMP_DIR', 'test_file.txt', 'w' );

  

  for c in ( SELECT

              PRFRD_SHOPPING_DY||1 || '|' ||

    1 || '|' ||

              GLBL_OFR_ID || '|' ||

              RAM_MBR_PFL.CLIENT_MBR_ID || '|' ||

              RAM_CREATED_DATE || '|' ||

              null || '|' ||

              OFR_TMPL_ID || '|' ||

              OFR_STRT_DT || '|' ||

              OFR_END_DT || '|' ||

              OFR_PRI || '|' ||

              PROPNSITY_SCR || '|' ||

              CAST(AWRD_VAL AS number) || '|' ||

              CTRL_GRP_IND as LINE

              FROM RAM_RCMDN RAM_RCMDN JOIN RAM_MBR_PFL RAM_MBR_PFL

              ON RAM_MBR_PFL.RAM_UNQ_MBR_ID = RAM_RCMDN.RAM_UNQ_MBR_ID

    where wkly_ofr_excutn_id=28 )

  loop

    utl_file.put_line( p_file, c.line );

  end loop;

  

  utl_file.fclose(p_file);

  

  dbms_cloud.put_object( 

    'test_cred', 

    'https://swiftobjectstorage.us-ashburn-1.oraclecloud.com/v1/ficolcl/test/test_file_prakash.txt',

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


