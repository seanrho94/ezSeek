# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import JobSearchForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from search_views.search import SearchListView
from search_views.filters import BaseFilter
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from .models import *
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ( 
    View,
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)

def Home(request):
    return render(request, 'index.html', {'title':'home'})  

class JobFilter(BaseFilter):
    search_fields = {
        'search_text' : ['title'],

    }      

class JobListView(SearchListView):
    model = Post
    template_name = 'jobs.html'
    #context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    form_class = JobSearchForm
    filter_class = JobFilter


#class JobDetailView(DetailView):
    #model = Post
    #template_name = 'jobDetail.html'

def JobDetailView(request, pk):
    #jobs = Post.objects.get(pk=pk)
    jobs = get_object_or_404(Post, pk=pk)
    is_applied = False
    if (jobs.applied.filter(id=request.user.id).exists()):
        is_applied = True
    context = {
        'object':jobs,
        'is_applied':is_applied
    }
    return render(request, "jobDetail.html", context)


class CompanyListView(ListView):
    model = Company
    template_name = 'companies.html'
    context_object_name = 'companies'
    ordering = ['name']
    paginate_by = 10

class CompanyDetailView(DetailView):
    model = Company
    template_name = 'companyDetail.html'

class JobseekerDetailView(DetailView):
    model = JobSeeker
    template_name = 'jobseekerDetail.html'

#View all the jobs that is posted by the user(company).
class UserJobListView(ListView):
    model = Post
    template_name = 'userJob.html' 
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



#-------------------------JobSeeker user job features-------------------------#
#Apply for a job
def Apply(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.is_ajax():
            jobs = Post.objects.get(id=pk)
            applications = Application.objects.filter(js_id=JobSeeker.objects.get(user=request.user),job_id=jobs)
            is_applied = False
            if (jobs.applied.filter(id=request.user.id).exists()):
                return JsonResponse({'error':'You have already applied for this job'}, status=403)
            else:
                newApplication = Application.objects.create(js_id=JobSeeker.objects.get(user=request.user),job_id=jobs, company_id=Company.objects.get(user=jobs.author))
                newApplication.save()
                jobs.applied.add(request.user)
                is_applied = True
                context = {
                    'object':jobs,
                    'is_applied':is_applied
                }
                html = render_to_string('applyButton.html', context, request=request) #pass to Json
                return JsonResponse({'form': html})
    else:
        return redirect('/login/?next=/job/%s' %pk)

#View applications
class MyApplicationListView(UserPassesTestMixin, ListView):
    model = Application
    template_name = 'myApplication.html'  
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(JobSeeker, user=self.request.user)
        return Application.objects.filter(js_id=user).order_by('-application_id')

    def test_func(self):
        currentUser = self.kwargs['username'] #magic kwargs!!!
        if self.request.user.username == currentUser:
            return True
        raise Http404("You are not allowed to view other Jobseeker's personal application page.")

#-------------------------Company user job features-------------------------#

#View all of the posted jobs from the personal job listings.
class MyJobListView(UserPassesTestMixin, ListView):
    model = Post
    template_name = 'myJob.html'  
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def test_func(self):
        currentUser = self.kwargs['username'] #magic kwargs!!!
        if self.request.user.username == currentUser:
            return True
        raise Http404("You are not allowed to view other company's personal job listing page.")

#View the job detail from the personal job listings.
class MyJobDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Post
    template_name = 'myJobDetail.html'
    context_object_name = 'posts'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        raise Http404("You are not allowed to view other company's personal job listing page.")

#Delete the job from the personal job listings. Redirects to myJob page after deleting.
class MyJobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'jobDelete.html'
   
    def test_func(self):
        post = self.get_object()
        if self.request.user.first_name == 'c' and self.request.user == post.author:
            return True
        else:
            raise Http404("You are not allowed to delete this job")
    
    def get_success_url(self):
        return reverse_lazy('myJob', kwargs={'username': self.object.author.username})

#View applicants for that job.
class MyApplicantListView(UserPassesTestMixin, ListView):
    model = Application
    template_name = 'myApplicant.html'  
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        job_id = Post.objects.get(id=self.kwargs['pk'])
        return Application.objects.filter(job_id = job_id )

    def test_func(self):
        job_id = Post.objects.get(id=self.kwargs['pk'])
        test = self.request.user
        if self.request.user == job_id.author:
            return True
        else:
            raise Http404(test)
#Post a job
class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    template_name = 'postJob.html'
    fields = ['title', 'content']

    
    def form_valid(self, form):
        if self.request.user.first_name =='c':
            form.instance.author = self.request.user
            #form.instance.company_id = self.request.user
            messages.success(self.request, 'Job posted!')
            return super().form_valid(form)
        else:
            return redirect('/')

    def test_func(self):
        if self.request.user.first_name == 'c':
            return True
        else:
            raise Http404("You need to login as Company user in order to post a job")

#Update the job from the public ('find jobs' page) job listings.
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'postJob.html'
    fields = ['title', 'content']

    
    def form_valid(self, form):
        if self.request.user.first_name =='c':
            form.instance.author = self.request.user
            messages.success(self.request, 'Job Updated!')
            return super().form_valid(form)
        else:
            return redirect('/')

    def test_func(self):
        post = self.get_object()
        if self.request.user.first_name == 'c' and self.request.user == post.author:
            return True
        else:
            raise Http404("You are not allowed to update this job")

#Delete the job from the public ('find jobs' page) job listings.
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'jobDelete.html'
    success_url = reverse_lazy('jobs')
   
    def test_func(self):
        post = self.get_object()
        if self.request.user.first_name == 'c' and self.request.user == post.author:
            return True
        else:
            raise Http404("You are not allowed to delete this job")

#Accept applicant
def AcceptApplicant(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.user.first_name == 'c':
                application = Application.objects.filter(application_id=pk)
                for object in application:
                    object.status = 'Accepted - You will get contacted shortly.'
                    object.save()
                    job_id = object.job_id_id
                    js_id = object.js_id
                    messages.success(request, '%(js_id)s is accepted' % {'js_id': js_id} )
                    return redirect('myApplicant', job_id)

#Reject applicant
def RejectApplicant(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.user.first_name == 'c':
                application = Application.objects.filter(application_id=pk)
                for object in application:
                    object.status = 'Rejected'
                    object.save()
                    job_id = object.job_id_id
                    js_id = object.js_id
                    messages.warning(request, '%(js_id)s is rejected' % {'js_id': js_id})
                    return redirect('myApplicant', job_id)

