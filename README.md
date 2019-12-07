# codefeatly

## About project
This project is created for holding programming contests just as on www.codeforces.com.  

## Installation
All you need is to install LAMP server if you are on GNU/LinuxOS and configure it.  
If you are on WindowsOS then just install OpenServer and configure that too the way you want.

### Notice
If you installed OpenServer on Windows then go to "{OpenServer folder}/OSPanel/userdata/config". There open "php.ini" file of php version you are using. Find line "output_buffering" and change the value to 4096.

## Configuration
1. In MySQL create a database to keep information there. Ex db name: "codefeatly". It is better if encode type will be "utf8_general_ci". Make sure you have the same encoding in settings of OpenServer if you are on Windows.  
2. Go to file "config.php" and correct the connection to your MySQL database you just created.  

## Adminpanel
### Notice
Default token for registrating an admin is "Y29kZWZlYXRseQ==" (the word "codefeatly" encoded in Base64).  
If you want to change it then go to "adminpanel/registration.php" and change the checking token on line 16 to that you want.  
