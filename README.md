# unamira

# IT Exam

## About project
This project is created for holding programming contests just as on codeforces.com.  

## Installation
All you need is to install LAMP server if you are on GNU/LinuxOS and configure it.  
If you are on WindowsOS then just install OpenServer and configure that too the way you want.

### Notice
If you installed OpenServer on Windows then go to "{OpenServer folder}/OSPanel/userdata/config". There open "php.ini" file of php version you are using. Find line "output_buffering" and change the value to 4096.

## Configuration
1. In MySQL create a database to keep information there. Ex db name: "unamira".  
It is better if encode type will be in "utf8mb4_unicode_520_ci". If you put "utf8mb4_unicode_520_ci" encoding to database in MySQL then do not forget to put "utf8mb4_unicode_ci" encoding in settings of OpenServer.
2. Go to file "config.php" and correct the connection to your MySQL database you just created.  

## Adminpanel
### Notice
Default token for registrating an admin is 'dW5hbWlyYQ==' (the word "unamira" encoded in Base64).  
If you want to change it then go to "adminpanel/registration.php" and change the checking token on line 16 to that you want.  
