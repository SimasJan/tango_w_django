from django.shortcuts import render
from django.http import HttpResponse
from . import views

# importing the Category, Page models
from rango.models import Category, Page

def index(request):
	# Query the database for a list of ALL categories currently stored. # Order the categories by no. likes in descending order.
	# Retrieve the top 5 only - or all if less than 5.
	# Place the list in our context_dict dictionary
	# that will be passed to the template engine.
	category_list = Category.objects.order_by('-likes')[:5] # '-' in '-likes' indicates that we want them by desc order.
	# fetching page objects, ordering by most views
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories': category_list,'pages': page_list}
	
	# Return a rendered response to send to the client.	
	return render(request, 'rango/index.html', context_dict)

def about(request):
	context_dict = {'boldmessage': 'Salmon Entertainment.'}
	return render(request, 'about/about.html', context=context_dict)
	#about_page = "Rango says here is the about page</br><a href='/rango/'>Home</a>"
	#return HttpResponse(about_page)

def show_category(request, category_name_slug):
	# create a context dictionary which we can pass
	# to the template rendering engine.
	context_dict = {}

	try:
		# Can we find a category name slug with the given name?
		# If we can't, the .get() method raises a DoesNotExist exception.
		# So the .get() method returns one model instance or raises an exception.
		category = Category.objects.get(slug=category_name_slug)

		# Retrieve all of the associated pages.
		# Note that filter() will return a list of page objects or an empty list
		pages = Page.objects.filter(category=category)

		# Adds our results list to the template context under pages.
		context_dict['pages'] = pages
		# we also add the category objects from
		# the databse to the context dictionary.
		# We'll use this in the template to verify that the category exists.
		context_dict['category'] = category
	except Category.DoesNotExist:
		# We get here if we didn't find the specified category. Don't do anything -
		# the template will display the "no category" message for us.
		context_dict['category'] = None
		context_dict['pages'] = None
		
	# render the response and return it to the client.
	return render(request, 'rango/category.html', context_dict)
