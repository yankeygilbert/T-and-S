
#    This Module use the Gemini Ai Api to peform analysis on  provided content.
#    For programtic use cases Kindly use the class <Manalyze> and function <main()>
#    which accepts a dictionary of media contents, an image file,text file or video file. You can also  pass string Input.
#    The module dynamically selects the appropriate multimodal state for use with GEMINI
#        Example:
#            from Analysis import Manalyze
#            Variable = Manalyze(<**content**>)
#            #Execute 
#            Variable.main()

#            DEVELEOPED BY: GILBERT.B.YANKEY


from google.generativeai.types import HarmCategory, HarmBlockThreshold
import google.generativeai as AnalyticAi
import os, re, pathlib, time

#Text analysis
class Tanalyze:
    
    def __init__(self,input):
        #prompt for Gemini
        self.prompt = """Analyze this conversation for the risk of sextortion or cyberbulleying. 
            Format your ouput as follows exactly like this
            cyberbulleying score: (high,low,medium,)
            sextortion score: (high,low,medium)
            (Your Explanation)
            Take into consideration familiarity and relationship between parties but this factors should only affect the score if neccessary
            convo = """
        self.input = input
    #Ouput cleaning and extraction
    def ext_Data(self,output):
        self.gmiOut = output
        self.pattern = r'"text":\s(".*")'
        self.match = re.search(self.pattern,self.gmiOut)

        if self.match:
            self.gmiOut = output[self.match.start()+7:self.match.end()]
            self.fgmiOut = re.sub(r'\\n|\\','. ',self.gmiOut)
            #Extraction for cyber score
            self.Cbpattern = r'(cyberbulleying\s?score:\s?(\w.?\w?){3,7})'
            self.match2 = re.search(self.Cbpattern,self.fgmiOut,re.IGNORECASE)

            if self.match2:
                self.Cboutput = self.fgmiOut[self.match2.start():self.match2.end()]
            else:
                return (self.fgmiOut)    
            #Extraction for sextortion score
            self.Sxpattern = r'(sextortion\s?score:\s?(\w.?\w?){3,7})'
            self.match3 = re.search(self.Sxpattern,self.fgmiOut,re.IGNORECASE)

            if self.match3:
                self.Sxoutput = self.fgmiOut[self.match3.start():self.match3.end()]
            else:
                return (self.fgmiOut)

            return (list((self.Cboutput,self.Sxoutput,self.fgmiOut)))
        else:
            return (self.fgmiOut)
            
    #Gemini Call text mode Engine
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
        return(self.final)
        

#Multimodal
class Vanalyze(Tanalyze):
    def __init__(self,input):
        #prompt for gemini
        self.prompt = """Analyze the attached media file for the risk of sextortion or cyberbulleying. 
            Extract conversations and perfom analysis based on the conversations you extract.
            Format your ouput as follows exactly like this
            cyberbulleying score: (high,low,medium,)
            sextortion score: (high,low,medium)
            (Your Explanation)
            Take into consideration familiarity and relationship between parties but this factors should only affect the score if neccessary
            """
        self.input = input
    #Gemini Call Multimodal Engine
    def analtics_Engine(self):
        self.authkey= os.environ['api_key']
        AnalyticAi.configure(api_key=self.authkey)
        #media file Upload
        self.mediaFile = self.input
        self.vf = AnalyticAi.upload_file(path=self.mediaFile)

        #Verify Upload State
        while self.vf.state.name == "PROCESSING":
            print('.', end=' ')
            time.sleep(10)
            self.vf = AnalyticAi.get_file(self.vf.name)

            if self.vf.state.name == "FAILED":
                raise ValueError(self.vf.state.name)

        self.model = AnalyticAi.GenerativeModel('gemini-1.5-pro')
        self.response = self.model.generate_content(
            [self.prompt,self.vf],
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
            })
        self.response.resolve()
        self.response = str(self.response)
        AnalyticAi.delete_file(self.vf)
        self.final = self.ext_Data(self.response)
        return(self.final)

        
#Entry Point class
class Manalyze(Vanalyze):
    def __init__(self,input):
        self.input = input
      
    def main(self):
        #verify Input type
        if type(self.input) == type({'key':1}):
                for key,value in self.input.items():
                    if re.search(
                        r'[a-zA-Z]+\.[(jpeg)|(jpg)|(png)|(webp)|(heic)|(heif)]',value,re.IGNORECASE) or re.search(
                        r'[a-zA-Z]+\.[(wav)|(mp3)|(aiff)|(aac)|(ogg)|(flac)]',value,re.IGNORECASE) or re.search(
                        r'[a-zA-Z]+\.[(mp4)|(mpeg)|(mov)|(avi)|(x-flv)|(mpg)|(mpg)|(webm)|(wmv)|(3gpp)]',value,re.IGNORECASE) or re.search(
                        r'[a-zA-Z]+\.[(csv)|(json)|(xml)|(markdown)|(rtf)|(html)]',value,re.IGNORECASE):
                          print("....")
                    else:
                        return ("Unsupported file Type : " + value )

                Instance = Vanalyze(self.input)
                return(Instance.analtics_Engine())

        if  (re.search(
            r'[a-zA-Z]+\.[(jpeg)|(jpg)|(png)|(webp)|(heic)|(heif)]',self.input,re.IGNORECASE)) or (re.search(
            r'[a-zA-Z]+\.[(wav)|(mp3)|(aiff)|(aac)|(ogg)|(flac)]',self.input,re.IGNORECASE)) or (re.search(
            r'[a-zA-Z]+\.[(mp4)|(mpeg)|(mov)|(avi)|(x\-flv)|(mpg)|(mpg)|(webm)|(wmv)|(3gpp)]',self.input,re.IGNORECASE)) or (re.search(
            r'[a-zA-Z]+\.[(csv)|(json)|(xml)|(markdown)|(rtf)|(html)]',self.input,re.IGNORECASE)):
            Instance = Vanalyze(self.input)
            return(Instance.analtics_Engine())
           
        else:
            Instance = Tanalyze(self.input)
            return(Instance.analtics_Engine())
                
       
           