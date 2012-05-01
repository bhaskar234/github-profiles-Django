# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from githubprofiles.models import Users,Repos
from django.template import Context,loader
from django.shortcuts import render_to_response
import json,requests,urllib,urllib2




def repoinfo(request,name,owner):
    repoinfo_list=Repos.objects.filter(owner=owner,name=name)
    return render_to_response('githubprofiles/index.html',{'template':'repoinfo','repoinfo_list':repoinfo_list})

def repos(request,login):
    repos_list=Repos.objects.filter(owner=login)
    return render_to_response('githubprofiles/index.html',{'template':'repos','repos_list':repos_list})

def userinfo(request,login):
    userinfo_list=Users.objects.get(login=login)
    t=loader.get_template('githubprofiles/index.html')
    c=Context({
        'template':'userinfo',
        'userinfo_list': userinfo_list,
        })
    return HttpResponse(t.render(c))

def showusers(request):
    users_list=Users.objects.all()
    t=loader.get_template('githubprofiles/index.html')
    c=Context({
        'template':'showusers',
        'users_list':users_list,
        })
    return HttpResponse(t.render(c))


def index(request):
    
    r=auth(request)
    if r is not None :
        return r 
    if("access_token" in request.session):
        str=request.session['access_token']
        if(request.session['access_token']!="" and request.session['access_token']!=None ):
               
    
            url="https://api.github.com/user?access_token="+request.session['access_token']  
            req=urllib2.Request(url)
            response=urllib2.urlopen(req)
            
            
            r=response.read()
            j=json.loads(r)
            request.session['login']=j['login']
      
            n=Users.objects.filter(login=j['login'])
            msg=""
            if(n.count()==0):
                
                userkeys={"type","login","collaborators","public_repos","public_gists","private_gists","followers","gravatar_id","html_url","url","created_at"}
                userdict={key: value for (key, value) in j.items() if key in userkeys}
                userdict['private_repos']=j['plan']['private_repos']
                u=Users(**userdict)
                u.save()
                
                
                url="http://github.com/api/v2/json/repos/show/"+j['login']
                req=urllib2.Request(url)
                response=urllib2.urlopen(req)
                r=response.read()
                j=json.loads(r)


                repokeys={"url","homepage","watchers","open_issues","created_at","pushed_at","has_issues","fork","has_downloads","private","name","description","forks","owner","has_wiki"}
                for i in range(len(j['repositories'])):
                    repodict={key: value for (key, value) in j['repositories'][i].items() if key in repokeys}
                    repo=Repos(**repodict)
                    repo.save()
                msg="Your Profile created successfully"
            else:
                msg="Your profile already exists"
    return render_to_response('githubprofiles/index.html',{'template':'msg','msg':msg})
    
def logout(request):
    del request.session['access_token']
    del request.session['access_token_status']
    return HttpRedirect("/githubprofiles/home")



def auth(request):
    
    redirecturi="http://"+request.META['HTTP_HOST']+request.path
    client_secret="20ee6fd2deaed712409544d28f683dc7ead68501";

    getTokenUrl="https://github.com/login/oauth/access_token?client_id=799c118a4784b2e967f8&redirect_uri="+redirecturi+"&client_secret="+client_secret

    getCodeUrl = "https://github.com/login/oauth/authorize?client_id=799c118a4784b2e967f8&redirect_uri="+redirecturi+"&scope=user,public_repo"

    getAccessToken=0
    if("access_token"  in request.session):
        if(request.session['access_token']=="" or request.session['access_token']==None) :
            getAccessToken=1
        elif(request.session['access_token_status']=="error"):
            getAccessToken=1
            
    else:
        getAccessToken=1
    if(getAccessToken==1):
        if("code" in request.REQUEST):
        
            if((request.REQUEST['code']!="") or (request.REQUEST['code']!=None)):
                code=request.REQUEST['code']
                values={'code':code}
                data=urllib.urlencode(values)
                req=urllib2.Request(getTokenUrl,data)
                
                response=urllib2.urlopen(req)
                r=response.read()
              	tokenstr=""
              	tokenstr=r.split("&")
                l=tokenstr[0].split("=")
              	request.session['access_token']=l[1]
              	request.session['access_token_status']=l[0]
              	if(request.session['access_token_status']=="error"):
                    return HttpResponseRedirect(getCodeUrl)
              	
              	
		
                
            else:
                return HttpResponseRedirect(getCodeUrl)
	 
        else:
            return HttpResponseRedirect(getCodeUrl) 
        
    

    
