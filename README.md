# NbgradeWithSakai

## System Set Up
1. Input your login info to config.csv 
2. Run systemSetup.py
   * It downloads jupyter, notebook, and nbgrader. 
   * It sets up a series of folders and partially configures the nbgrader
   * It creates expect scripts for easy login to server and easy connection to the jupyter notebook to your local computer
     * Open_server_nb provides an ssh connection to the server’s jupyter notebook (localhost 8887)
     * Open_local_nb connects to the server’s jupyter notebook locally, and you can find the notebook on localhost 8888.  
3. When you open the jupyter notebook on your local computer for the first time, you might need to use the specific link provided by the terminal running open_server_nb set up a password. 
4. Confirm  jupyter, notebook, and nbgrader are downloaded. Make sure you see “form grader” in the jupyter notebook home page. 
5. If not, then run the commands starting with jupyter from systemSetup.py. (or refer to nbgrader installation setup here) 
6. Then open nbgrader_config.py and change c.Exchange.root entry to: c.Exchange.root = './exchange'
7. Nbgrader should be functional now. If there is any error, check details below, or google :-)   .

##  Homework set up
1. An overview of organization 
   * Source: this is where you put the instructor solutions. Inside this folder, there is a folder per homework assignment. 
   * Release: this is where you get the student version of the solution. 
   * Submitted: this is where you put the homework students submitted. Inside this submitted foder, there is a folder per student. Inside a student folder, there is a folder per homework assignment 
   * Feedback: this is where you get the graded homework. Graded homeworks are in html. Similar structure as submitted. 
   * Autograded: this is where the autograded homework is located. Similar structure as submitted 
2. But you don’t really need to worry about these file structures. File transfers are automated 
   * Python3 transferInstructorFile <homework_assignment_number> -> transfers instructor file
   * Python3 transferStudentSubmissions <homework_assignment_number> -> transfers student submissions 
   * Python3 retriedGradedSubmissions <homework_assignment_number> -> get graded assignments back. 
3. So you can start by transferring instructor solutions with transferInstructorFile.py. Then use the expect scripts (login_server.exp, open_local_nb.exp, open_server_nb.exp) by running each script on a separate terminal (expect <script_name>) to establish a connection between your server and your local computer. Go to jupyter notebook’s formgrader (this will be in your localhost 8888, accessible from any browser). This is nbgrader’s interface. Create/go to an assignment. 
    * You can assign points through View->Cell Toolbar->Create Assignment (in the toolbar)
    * When writing the assignment, you should inform the nbgrader that a cell needs to be graded by clicking “Create Assignment”. On the top right corner of the cell, there are several options as to how the assignment can be graded
      * Auto graded answer (where student put their answer, necessary)
      * Auto graded test (where you put the autograding tests, very necessary!)
      * Manually graded answer (necessary! This helps us to assign points later)
   * Note that if an assertion fails, there is no partial credit. You can manually assign partial credit. 
4. To release an assignment, go to form grader interface, click generate and then release. 
5. Go to the release folder to find the student version. A student version is the version of the homework without solution. 
6. After students finish their assignments, you can download them from sakai to where the NbgraderWithSakai is located. Then you can run transferStudentSubmission.py. 
7. Then use the expect scripts to establish a connection between your server and your local computer. You can run autograding from the command line (nbgrader autograder <assignment_name, which should be <class_name-hw<assignment-number> > and then start manual grading. See more here. 
8. In the nbgrader interface, click collect and then autograde. If this autograde button does not work, use command line. 
9. After grading, run release feedback (nbgrader generate feedback <assignment_name>) and use retrieveGradedSubmissions to get the graded homeworks back in a format acceptable to Sakai. You can upload the folder you downloaded from Sakai back to Sakai. 
10. Right now automatically transferring grades and comments are not supported. So you will need to manually enter the grades. 


