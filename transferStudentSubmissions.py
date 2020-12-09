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
print("matching downloaded file - please remove irrelevant files with the name "+str(ASSIGNMENT_NAME))
for file in files_in_folder:
    print(file[:len(str(ASSIGNMENT_NAME))])
    if file[:len(str(ASSIGNMENT_NAME))].lower() == ASSIGNMENT_NAME:
        TIME_STAMPED_FOLDER = file
        break
print(TIME_STAMPED_FOLDER,ASSIGNMENT_NAME)
LOCAL_PATH = LOCAL_ROOT_PATH+TIME_STAMPED_FOLDER + '/'+ASSIGNMENT_NAME+"/"
if not os.path.isdir(LOCAL_PATH):
    LOCAL_PATH = LOCAL_ROOT_PATH+ASSIGNMENT_NAME+"/"
SERVER_SUBMISSION_PATH = SERVER_ROOT_PATH + 'submitted/'

# establish ssh connections
ssh, sftp = establish_ssh(SERVER,USERNAME,PASSWORD)

numBadFormatFile = 0
studentNameList = []

print("Begin transfering student files from "+LOCAL_PATH+" to "+SERVER_SUBMISSION_PATH)
for student_folder in os.listdir(LOCAL_PATH):
    if student_folder[0]=='.' or student_folder[-4:]=='.csv':
        print("skip "+file)
        continue
    try:
        local_submission_folder = LOCAL_PATH+student_folder+"/Submission attachment(s)/"
        local_submission_file = local_submission_folder+FULL_ASSIGNMENT_NAME+".ipynb"
        student_name = student_folder[:student_folder.rindex("(")]
        ##### server_student_folder_path: [server_directory]/[nb_grader_folder]/submitted/[name]/HW[id]/
        server_student_folder_path = SERVER_SUBMISSION_PATH + student_name + "/"
        server_student_hw_folder_path = server_student_folder_path + ASSIGNMENT_NAME +"/"
        server_student_file = server_student_hw_folder_path + FULL_ASSIGNMENT_NAME+".ipynb"
        if not os.path.exists(server_student_file):
            files_in_folder = os.listdir(server_student_hw_folder_path)
            complete_student_filename = None
            for file in files_in_folder:
                print(file[:len(str(ASSIGNMENT_NAME))])
                if file[-len(str(FULL_ASSIGNMENT_NAME)):].lower() == FULL_ASSIGNMENT_NAME:
                    complete_student_filename = file
                    print("found", complete_student_filename)
                    break
            server_student_file = complete_student_filename

        #print(local_submission_file,server_student_file)
        # create path in server folders
        sftp_always_mkrdir(sftp, server_student_folder_path)
        sftp_always_mkrdir(sftp, server_student_hw_folder_path)

        # move student submission
        sftp_move_if_not_existed(sftp,local_submission_file, server_student_file)

        # move data files
        for common_file in os.listdir(local_submission_folder):
            if common_file == ASSIGNMENT_NAME :
                continue
            sftp_move_local_folder_to_server(sftp, local_submission_folder, server_student_hw_folder_path, common_file)
        print(r"""       Completed transfer for """, student_name)
    except:
        numBadFormatFile+=1
        studentNameList.append(student_name)
print("Completed processing student submissions\n")
_ = ssh.exec_command("nbgrader autograde "+ASSIGNMENT_NAME)

# launching jupyter notebook
print("Start launching jupyter notebook on server")
_, exec_output,_ = ssh.exec_command("jupyter notebook --no-browser --port=8887")

# closing ssh
close_ssh(ssh, sftp)

# next step - info
print("Sumamry - number of bad formattings: ", numBadFormatFile)
if numBadFormatFile>0:
    print("Failed to transfer files for:")
    print(studentNameList)
    print()
print("Next steps:")
print("Run: \"expect open_server_nb.exp\" to redirect jupyter to local host.")
print("Note: It will not close after running. "+\
      "To close the expect process, use control-C to properly close the port")
print("\nThen open a server terminal with the command: expect login_server.exp")
print("\nRun in server terminal: nbgrader autograde "+ASSIGNMENT_NAME)
print("\nOpen your local browser and go to local host ***8888*** to manual grade")
print("\nRun in server terminal: nbgrader generate_feedback "+ASSIGNMENT_NAME)
print("\nThen retrive graded submission using python script")
