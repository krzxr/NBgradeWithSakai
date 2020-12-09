import sys
from util import *

ASSIGNMENT_ID = str(sys.argv[1])

config_filename = str(sys.argv[2]) if len(sys.argv)>3 else "config.csv"
USERNAME, PASSWORD, SERVER, CLASSNAME = retrive_config(config_filename)
LOCAL_ROOT_PATH, SERVER_ROOT_PATH = get_path(config_filename)

ASSIGNMENT_NAME = "hw"+str(ASSIGNMENT_ID)
FULL_ASSIGNMENT_NAME = CLASSNAME+"-hw"+str(ASSIGNMENT_ID)
LOCAL_PATH = LOCAL_ROOT_PATH+"source/"+ASSIGNMENT_NAME+"/"
SERVER_SOURCE_PATH = SERVER_ROOT_PATH + 'source/'+ASSIGNMENT_NAME + '/'

ssh, sftp = establish_ssh(SERVER,USERNAME,PASSWORD)

sftp_always_mkrdir(sftp, SERVER_SOURCE_PATH)

print()
print("Begin transfering instructor files from ",LOCAL_PATH," to ",SERVER_SOURCE_PATH)
for file in os.listdir(LOCAL_PATH):
	print(file)
	if file[0]=='.':
		print("skip "+file)
		continue
	sftp_move_local_folder_to_server(sftp, LOCAL_PATH, SERVER_SOURCE_PATH, file)
print("Completed instructor files transfer.\n")

print()
close_ssh(ssh,sftp)