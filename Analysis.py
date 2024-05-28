from google.generativeai.types import HarmCategory, HarmBlockThreshold
import google.generativeai as AnalyticAi
import os, re

class analyze:
    #Prompt for Gemini-1.5-Pro
    def __init__(self,input):
        self.prompt = """Analyze this conversation for the risk of sextortion or cyberbulleying. 
        Format your ouput as follows exactly like this
        cyberbulleying score: (high,low,medium)
        sextortion score: ((high,low,medium))
        thirdline: Your Explanation
        Take into consideration familiarity and relationship between parties but this factors should not directly affect the score
        convo = """
        self.input = input
    #Data cleaning and extraction
    def ext_Data(self,output):
        self.gmiOut = output
        self.pattern = r'"text":\s(".*")'
        self.match = re.search(self.pattern,self.gmiOut)
        if self.match:
            self.gmiOut = output[self.match.start()+7:self.match.end()]
            self.fgmiOut = re.sub(r'\\n','. ',self.gmiOut)
            #Extraction for cyber score
            self.Cbpattern = r'(cyberbulleying\s?score:\s?\w{3,7})'
            self.match2 = re.search(self.Cbpattern,self.fgmiOut,re.IGNORECASE)
            if self.match2:
                self.Cboutput = self.fgmiOut[self.match2.start():self.match2.end()]
            else:
                return ("no data found")    
            #Extraction for sextortion score
            self.Sxpattern = r'(sextortion\s?score:\s?\w{3,7})'
            self.match3 = re.search(self.Sxpattern,self.fgmiOut,re.IGNORECASE)
            if self.match3:
                self.Sxoutput = self.fgmiOut[self.match3.start():self.match3.end()]
            else:
                return ("no data found")
            return (self.Cboutput + '\n' + self.Sxoutput)
        else:
            return ("no data found")

    def analtics_Engine(self):
        self.authkey= os.environ['api_key']
        AnalyticAi.configure(api_key=self.authkey)
        self.model = AnalyticAi.GenerativeModel('gemini-1.5-flash')
        self.response = str(self.model.generate_content([self.prompt + self.input],
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        }))
        self.final = self.ext_Data(self.response)
        print( self.fgmiOut + '\n')
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

Instance = analyze(string)

Instance.analtics_Engine()
