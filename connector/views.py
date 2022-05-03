
import os
from zipfile import ZipFile
from django.conf import settings
from django.http import  HttpResponseRedirect
from django.shortcuts import redirect, render
import tensorflow as tf
from connector.forms import RegisterForm
from media.extractor import resumeExtractor 
from .apps import ConnectorConfig
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from client_talent_connector import settings 
from sklearn.metrics.pairwise import cosine_similarity

dict_model=ConnectorConfig.dict_model
model=ConnectorConfig.model

def home(request):
    return render(request,'connector/home.html')

def upload(request):
    
    if request.method=='POST':
        
        uploaded_file=request.FILES['file-name']
        job_description=request.POST["job-Description"]
        
        job_prob = model.predict(tf.convert_to_tensor([job_description]))
        index=job_prob.argmax()
        job_catego=dict_model[index]
        
        
        fs=FileSystemStorage()
        file_name_truncated=str(uploaded_file.name).split('.')[0]
        # print("uploaded file name: ",uploaded_file.name)        
        fs.save(uploaded_file.name,uploaded_file)
        file_path=os.path.join(settings.MEDIA_ROOT,uploaded_file.name)
        output=[]
        resume_name=[]
        similarity_prob=[] 
        try:
            with ZipFile(file_path,'r') as zpfile:
                zpfile.extractall('./extracted')
                for file_name in os.listdir(os.path.join("./extracted")):
                    file_path=os.path.join('./extracted',file_name)
                    cleaned_resume=resumeExtractor(file_path=file_path)
                    resume_prob = model.predict(tf.convert_to_tensor([cleaned_resume]))
                    index = resume_prob.argmax()
                    
                    predicted=[dict_model[index]]
                    output.extend(predicted)
                    resume_name.append(file_name)
                    similarity=cosine_similarity(job_prob,resume_prob)[0]
                    similarity_prob.append(similarity.tolist()[0]*100)
                    os.remove(file_path)
        except:
            return render(request,'connector/home.html')
        
        try:
            os.rmdir(os.path.join("./extracted",file_name_truncated))
            os.remove(f"./media/{uploaded_file.name}")
        except:
            pass 
        predicted=list(zip(output,resume_name))
            
        
    return render(request,'connector/home.html',context={'predicted':predicted,"similarity":similarity_prob,"job_catego":job_catego})

    
def register(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home/')
        else:    
            form=RegisterForm()
            return redirect("/register/")
    elif request.method=='GET':
        
        return render(request,'connector/register.html')
    
def login(request):

    return render(request,'connector/login.html')

    





































