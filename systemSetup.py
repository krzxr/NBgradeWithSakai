from util import *
import os
import sys

def mkdir_always(filename):
    if not os.path.exists(filename):
        os.mkdir(filename)
config_filename = str(sys.argv[1]) if len(sys.argv)>2 else "config.csv"
USERNAME, PASSWORD, SERVER, CLASSNAME = retrive_config(config_filename )

print("Generating three scripts on your computer")

ssh_file = open("login_server.exp","w+")
ssh_file.write(r'''#!/usr/bin/expect

set timeout 10

spawn ssh "'''+USERNAME+r'''\@'''+SERVER+r'''"

expect "'''+USERNAME+r'''\@'''+SERVER+r'''\'s password: "

send "'''+PASSWORD+r'''\r";

interact
''')
ssh_file.close()

local_file = open("open_server_local.exp", "w+")
local_file.write(r'''#!/usr/bin/expect

set timeout 10

spawn ssh -N -L localhost:8888:localhost:8887 "'''+USERNAME+r'''\@'''+SERVER+r'''"

expect "'''+USERNAME+r'''\@'''+SERVER+r'''\'s password: "

send "'''+PASSWORD+r'''\r";

interact


''')
local_file.close()

ssh_file = open("open_server_nb.exp","w+")
ssh_file.write(r'''#!/usr/bin/expect

set timeout 10

spawn ssh "'''+USERNAME+r'''\@'''+SERVER+r'''"

expect "'''+USERNAME+r'''\@'''+SERVER+r'''\'s password: "

send "'''+PASSWORD+r'''\r";

sleep 1

send "cd '''+CLASSNAME+r'''\r"

sleep 1

send "jupyter notebook --no-browser --port=8887\r"

interact
''')
ssh_file.close()


print("Completed exp set up. The script will port server's notebook to your local host 8887. ")
print("if there is any failure below, then go to drive for nbgrader set up notes")

print("Setting up jupyter notebook and nbgrader on the server")
ssh, sftp = establish_ssh(SERVER,USERNAME,PASSWORD)
run_command(ssh, "python3 -m pip install jupyter --user")
run_command(ssh, "python3 -m pip install notebook --user")
run_command(ssh, "python3 -m pip install nbgrader --user")
run_command(ssh, "python3 -m pip install tqdm --user")
run_command(ssh, "python3 -m pip install matplolib --user")
run_command(ssh, "python3 -m pip install numpy --user")
run_command(ssh, "python3 -m pip install IPython --user")
run_command(ssh, "python3 -m pip install scipy --user")
run_command(ssh, "python3 -m pip install pandas --user")
run_command(ssh, "python3 -m pip install sklearn --user")
local_bin_path = run_command(ssh,"systemd-path user-binaries")[:-2]+"/"
print(local_bin_path)
run_command(ssh, local_bin_path+"jupyter nbextension install --user --py nbgrader --overwrite")
run_command(ssh, local_bin_path+"jupyter nbextension enable --user --py nbgrader")
run_command(ssh, local_bin_path+"jupyter serverextension enable --user --py nbgrader")
run_command(ssh, local_bin_path+"nbgrader quickstart "+CLASSNAME)
run_command(ssh, "mkdir ./"+CLASSNAME+"/exchange")
run_command(ssh, "mkdir ./" + CLASSNAME + "/release")
run_command(ssh, "mkdir ./" + CLASSNAME + "/feedback")
run_command(ssh, "mkdir ./" + CLASSNAME + "/autograded")
run_command(ssh, "mkdir ./" + CLASSNAME + "/submitted")
print()
print(r"""If the comamnds above are successful, then run "expect login_server.exp" to verify """)
print("(1) jupyter notebook is installed by opening jupyter notebook")
print("(2) nbgrader is installed by checking that there is a nbgrader tab in your jupyter notebook main interface")

print("go to folder "+CLASSNAME+" and open nbgrader_config.py")
print("change c.Exchange.root entry to: c.Exchange.root = './exchange'")
close_ssh(ssh, sftp)
print("if there is an error above, check drive for notes")
print(r"""Next step: run "transferInstructorFile.py <assignment_id>" to move an insturctor file.""")
print(r"""Or: run "transferStudentSubmissions.py <assignment_id>" to move student files.""")