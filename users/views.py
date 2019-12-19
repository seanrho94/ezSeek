# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from RS.models import *


def register(request):
    return render(request, 'register.html', {'title':'register'})

def jsRegister(request):
    if request.method == 'POST':
        form = JobSeekerSignUpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = form.cleaned_data.get('username')
            user = form.save()
            user.refresh_from_db()
            user.first_name = 'i'
            user.save()
            jobseeker = JobSeeker(user=user, name = cd.get('name'), bio = cd.get('bio'),location = cd.get('location'), phone_no = cd.get('phone_no'), qualification = cd.get('qualification'), profession = cd.get('profession'))
            jobseeker.save()
            messages.success(request, 'Account created for ' + username)
            return redirect('login')
    else:
        form = JobSeekerSignUpForm()
    return render(request, 'jsRegister.html', {'form': form})


def companyRegister(request):
    if request.method == 'POST':
        form = CompanySignUpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = form.cleaned_data.get('username')
            user = form.save()
            user.refresh_from_db()
            user.first_name = 'c'
            user.save()
            company = Company(user=user, name=cd.get('name'), industry=cd.get('industry'), location=cd.get('location'), bio=cd.get('bio'))
            company.save()
            messages.success(request, 'Account created for ' + username)
            return redirect('login')
    else:
        form = CompanySignUpForm()
    return render(request, 'companyRegister.html', {'form': form})

@login_required
def profile(request):
    if request.user.is_authenticated:
        if request.user.first_name == 'i':    
            if request.method == 'POST':
                profile = JobSeeker.objects.get(user=request.user)
                u_form = JobseekerUpdateForm(request.POST, instance=profile)
                p_form = ProfileUpdateForm(request.POST,
                                           request.FILES,
                                           instance=request.user.profile)
                if u_form.is_valid() and p_form.is_valid():
                    u_form.save()
                    p_form.save()
                    messages.success(request, 'profile updated')
                    return redirect('profile')

            else:
                profile = JobSeeker.objects.get(user=request.user)
                u_form = JobseekerUpdateForm(instance=profile)
                p_form = ProfileUpdateForm(instance=request.user.profile)
            context = {
                'u_form': u_form,
                'p_form': p_form,
                'jobseeker': profile,
            }

            return render(request, 'profile.html', context)
        else:
            if request.user.first_name == 'c':
                if request.method == 'POST': 
                    profile = Company.objects.get(user=request.user) 
                    u_form = CompanyUpdateForm(request.POST, instance=profile)
                    p_form = ProfileUpdateForm(request.POST,
                                           request.FILES,
                                           instance=request.user.profile)
                    if u_form.is_valid() and p_form.is_valid(): 
                        u_form.save()
                        p_form.save()
                        messages.success(request, 'profile updated')
                        return redirect('profile')
                else:
                    profile = Company.objects.get(user=request.user)
                    u_form = CompanyUpdateForm(instance=profile)
                    p_form = ProfileUpdateForm(instance=request.user.profile)
                context = {
                    'u_form': u_form,
                    'p_form': p_form,
                    'company': profile,
                }
                
                return render(request, 'profile.html', context)    
