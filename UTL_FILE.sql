declare
  fhandle utl_file.file_type;
begin
  fhandle := utl_file.fopen( 'DATA_PUMP_DIR', 'test_file.txt', 'w' );
  for c in ( SELECT CHANNEL_ID || '|' || 
                    CHANNEL_DESC || '|' ||
                    CHANNEL_CLASS || '|' || 
                    CHANNEL_CLASS_ID || '|' ||
                    CHANNEL_TOTAL || '|' ||
                    CHANNEL_TOTAL_ID as LINE FROM channels)
  loop
    utl_file.put_line(fhandle, c.line );
  end loop;
  utl_file.fclose(fhandle);
  dbms_cloud.put_object( 
    'def_cred_name', 
    'https://swiftobjectstorage.us-ashburn-1.oraclecloud.com/v1/gse00015635/backup_demoatp/test_file.txt',
    'DATA_PUMP_DIR',
    'test_file.txt' );  
end;
/
 