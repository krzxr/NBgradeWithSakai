import os
import pandas as pd
import paramiko
from stat import S_ISREG
import time
# system set up
def retrive_config(config_filename):
	print("Gathering setting from config")
	df = pd.DataFrame(pd.read_csv(config_filename))
	username = df.at[0,"username"]
	password = df.at[0,"password"]
	server = df.at[0,"server"]
	classname = df.at[0,"classname"]
	return str(username), str(password), str(server), str(classname)

# run command on server
def	establish_ssh(server, username, password):
	print("Establishing ssh connection")
	ssh = paramiko.SSHClient()
	ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
	ssh.connect(server, username=username, password=password)
	sftp = ssh.open_sftp()
	print("Completed establishing ssh connection\n")
	return ssh, sftp

def run_command(ssh,command):
	try:
		_, stdout, _ = ssh.exec_command(command, get_pty=True)
		last_output = ''
		for line in iter(stdout.readline, ""):
			last_output = line
			print(line, end="")
		print("Completed command",command)
		return last_output
	except:
		print("there is an error in running command",command)
	print()

def close_ssh(ssh, sftp):
	sftp.close()
	ssh.close()
	print("Closed ssh\n")

# get path
def get_path(config_filename):
	_,_,_, classname = retrive_config(config_filename)
	local_root_path = os.getcwd()
	remote_root_path = classname+"/"
	if local_root_path[-1]!="/":
		local_root_path+="/"
	return local_root_path, remote_root_path

def sftp_always_mkrdir(sftp, path):
	try:
		sftp.stat(path)
	except FileNotFoundError:
		sftp.mkdir(path)

# move if not existed
def sftp_move_if_not_existed(sftp, local_file, remote_file):

	try:
		sftp.stat(remote_file)
	except FileNotFoundError:
		sftp.put(local_file, remote_file)

def sftp_verify_existed(sftp, remote_file):
	try:
		sftp.stat(remote_file)
		return True
	except FileNotFoundError:
		return False

def sftp_move_local_folder_to_server(sftp, local_path, remote_path, file):
	isFile = os.path.isfile(local_path + file)
	file = file if isFile else file + '/'
	local_file = local_path + file
	remote_file = remote_path + file
	if isFile:
		sftp_move_if_not_existed(sftp,local_file, remote_file)
	else:
		sftp_always_mkrdir(sftp, remote_path + file)
		for subfile in os.listdir(local_path + file):
			local_subfile = local_path + file + subfile
			remote_subfile = remote_path + file + subfile
			sftp_move_if_not_existed(sftp,local_subfile, remote_subfile)

def sftp_move_server_folder_to_local(sftp, local_folder, server_folder, file_info):
	file_mode = file_info.st_mode
	file = file_info.filename if S_ISREG(file_mode) else file_info.filename + '/'
	local_file = local_folder + file
	server_file = server_folder + file
	if S_ISREG(file_mode):
		sftp.get(server_file, local_file)
	else:
		if not os.path.exists(local_file):
			os.mkdir(local_file)
		for subfile in sftp.listdir(server_folder + file):
			local_subfile = local_folder + file + subfile
			server_subfile = server_folder + file + subfile
			sftp.get(server_subfile, local_subfile)