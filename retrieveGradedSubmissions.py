import sys
from util import *

ASSIGNMENT_ID = str(sys.argv[1])

config_filename = str(sys.argv[2]) if len(sys.argv)>3 else "config.csv"
USERNAME, PASSWORD, SERVER, CLASSNAME = retrive_config(config_filename)

ASSIGNMENT_NAME = "hw"+str(ASSIGNMENT_ID)
FULL_ASSIGNMENT_NAME = CLASSNAME+"-hw"+str(ASSIGNMENT_ID)
LOCAL_ROOT_PATH, SERVER_ROOT_PATH = get_path(config_filename)

files_in_folder = os.listdir(".")
TIME_STAMPED_FOLDER = None

print("matching downloaded file - please remove irrelevant files with the name "+ASSIGNMENT_NAME)
for file in files_in_folder:
    if file[:len(ASSIGNMENT_NAME)].lower() == ASSIGNMENT_NAME:
        TIME_STAMPED_FOLDER = file
        break

LOCAL_PATH = LOCAL_ROOT_PATH+TIME_STAMPED_FOLDER + '/'+ASSIGNMENT_NAME+"/"
if not os.path.isdir(LOCAL_PATH):
    LOCAL_PATH = LOCAL_ROOT_PATH+ASSIGNMENT_NAME+"/"
SERVER_FEEDBACK_PATH = SERVER_ROOT_PATH + 'feedback/'

# ssh connection
ssh, sftp = establish_ssh(SERVER,USERNAME,PASSWORD)

full_student_folder_name_map = dict()
for student_folder in os.listdir(LOCAL_PATH):
    if student_folder[0]=='.' or student_folder[-4:]=='.csv':
        continue
    student_name = student_folder[:student_folder.rindex("(")]
    full_student_folder_name_map[student_name]=student_folder

#moving feedback
print('Begin retriving graded submission')
for folder in sftp.listdir(SERVER_FEEDBACK_PATH):
    if folder[0]==".":
        continue
    # set local folders
    #### [local_directory]/[folder for submission]/feedback/HW#/student_name/
    local_folder = LOCAL_PATH + full_student_folder_name_map[folder] + '/Feedback Attachment(s)/'
    # /[server_directory]/[nb_grader_folder]/feedback/HW#/
    server_folder = SERVER_FEEDBACK_PATH + folder + '/' + ASSIGNMENT_NAME + '/'

    # make local path
    if not os.path.exists(local_folder):
        os.mkdir(local_folder)

    # move files from server
    for file_info in sftp.listdir_attr(server_folder):
        sftp_move_server_folder_to_local(sftp, local_folder, server_folder, file_info)

    print(r"""     Completed processing for student """,folder)
print("Comleted graded submission retrivial\n")
print()
print("Go to the terminal with open_server_nb.exp and enter control C!")
close_ssh(ssh,sftp)
