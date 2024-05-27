import os, re
import google.generativeai as AnalyticAi

class analyze:
    def __init__(self,input):
        self.prompt = """Analyze this convo for the risk of sextortion or cyberbulleying 
        format your ouput as follows to contain  
        cyberbulleying score: (high,low,medium), 
        sextortion score: ((high,low,medium)). 
        convo = """
        self.input = input

    def ext_Data(self,output):
        self.output = output
        self.pattern = r'"text":\s(".*")'
        self.match = re.search(self.pattern,self.output)
        if self.match:
            self.output = output[self.match.start()+7:self.match.end()]
            self.output.replace('\\n',' ')
            return self.output
        else:
            return ("no data found")

    def analtics_Engine(self):
        self.authkey= os.environ['api_key']
        AnalyticAi.configure(api_key=self.authkey)
        self.model = AnalyticAi.GenerativeModel('gemini-1.5-pro')
        self.response = str(self.model.generate_content(self.prompt + self.input))
        self.final = self.ext_Data(self.response)
        print(self.final)



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
That outcome is in your hands

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

Yankey, [18-Jan-24 9:01 AM]
I recieved downlaoded and listened

Yankey, [18-Jan-24 9:01 AM]
That is the song i was referring to

Mag, [18-Jan-24 9:05 AM]
Okay okay I get it

Mag, [06-Apr-24 10:29 AM]


Yankey, [06-Apr-24 10:40 AM]
She’s the best thing you would ever have .

Yankey, [06-Apr-24 10:41 AM]
Well i’m taking it and not going to break it eh 🙂🙃" """

#Instance = analyze(string)

#Instance.analtics_Engine()
