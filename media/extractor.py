import textract
import nltk
import re
import string
from nltk.corpus import stopwords
nltk.download('stopwords')

stopwords_set = set(stopwords.words('english')+['``',"''"])
def clean_resume_text(resume):
    resume = resume.lower()
    resume = re.sub('http\S+\s*',' ',resume) #to remove url
    resume = ''.join([w for w in resume if not w.isdigit()]) # remove the digits
    resume = re.sub('RT|cc',' ',resume) # to remove RT and cc
    resume = re.sub('#\S+','',resume) # to remove hastags
    resume = re.sub('@\S+',' ',resume) # to remove mentions
    resume = ''.join([w for w in resume if w not in string.punctuation])# to remove puntuations
    resume = re.sub('\W',' ',resume)
    #resume = ''.join([w for w in resume if w not in stopwords_set])
    resume = re.sub(r'[^\x00-\x7f]',r' ',resume)
    resume = re.sub('\s+',' ',resume)# to remove extra spaces
    return resume

def resumeExtractor(file_path):
    text = textract.process(file_path)
    cleaned_resume=clean_resume_text(str(text))
    return cleaned_resume




