from django.shortcuts import render,HttpResponseRedirect



def test(request):
    return render(request,'guide.html')