from GeminImplementation import Manalyze

string = """"Yankey,[1-Jan-24 12:30 PM]
My eyes were on my screen when the message came in

Mag, [01-Jan-24 12:32 PM]
Oooooh

Mag, [01-Jan-24 12:32 PM]
Okay okay

Mag, [17-Jan-24 9:40 AM]


Mag, [17-Jan-24 9:41 AM]
Not bad at all for a wedding song😂😅🤭

Yankey, [17-Jan-24 10:39 AM]
Sounds good to perform on a guitar for my wife then

Mag, [17-Jan-24 11:49 AM]
😂it's my song 
If its not me...don't play or even listen  to it

Yankey, [17-Jan-24 2:41 PM]
i will disgrace you and kill you

Mag, [17-Jan-24 3:58 PM]
Ooooh

Yankey, [17-Jan-24 4:57 PM]
Yes ma’m

Yankey, [17-Jan-24 7:53 PM]
I like this song

Yankey, [17-Jan-24 7:56 PM]
The first part

Mag, [17-Jan-24 9:09 PM]
Which one??

Yankey, [18-Jan-24 8:59 AM]
You deleted the song you sent

Mag, [18-Jan-24 9:00 AM]
Vpn
It was taking too long to send

Mag, [18-Jan-24 9:00 AM]
You want it??
"""

query = Manalyze(string)
output = query.main()
#extract  score and reasoning 
print(output[2])

