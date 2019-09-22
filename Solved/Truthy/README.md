# Truthy
Web

## Challenge 

Do you solemnly swear that you will tell the truth, the whole truth, and nothing but the truth, so help you God?

Something is fishy about truths in PHP

http://challs.hats.sg:1342/

http://challs.hats.sg:1342/?SRC

Challenge by: Gladiator

## Solution

http://challs.hats.sg:1342/?SRC

	<?php
	if(isset($_GET['SRC'])){
	    show_source("index.php");
	    die();
	}
	require_once 'flag.php';
	if(isset($_GET['flag'])){
	    $var = $_GET['flag'];
	    if($var == 1 && strlen($var) == 9){
	            echo $flag;
	        }
	}
	?>

	<!DOCTYPE html>
	<html>
	<head>
	    <title></title>
	</head>
	<body>
	    Truth shall unfold when I GET a SouRCe.<br>
	    <!-- Try making a GET request for SRC ?-->
	</body>
	</html>

Simply make a number of length 9 that equals to one by padding it with zeros.

http://challs.hats.sg:1342/?flag=000000001

flag{flash_back_from_whitehacks2019} Truth shall unfold when I GET a SouRCe.

## Flag

	flag{flash_back_from_whitehacks2019}
