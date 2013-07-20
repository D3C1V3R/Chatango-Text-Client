Chatango Text Client
====================

GUI client for Chatango that's written with  python and uses TK.

	Credits to Hanzel/Pystub (Chatango users)
		Nullspeaker (https://github.com/Nullspeaker/ch.py)
		
	An 'Optional' file can be created by the user to filter out usernames in the client.
	To do this,
	
	1. Make a file within the same location as the client called 'Ignored.txt'
	2. Fill the text file with names, no formatting needed.
	

	Commands;
	
	!bg <Hex Colour/Name>
		Sets client Background colour, Common colour names are useable
			!bg 123, !bg 112233
	!nc <Hex Colour>
		Sets Name Colour (Not visible to client)
			!nc 123, !nc 112233
	!bc <Hex Colour>
		Sets Message Body Colour 
			!bc 123, !nc 112233
	!font <Name>
		Sets Message Font style
			0 = Arial
			1 = Comic
			2 = Georgia
			3 = Handwriting
			4 = Impact
			5 = Palatino
			6 = Papyrus
			7 = Times
			8 = Timewriter
			OR input font name.
	!ignore <Name>
		Ignores user from being seen by client.
