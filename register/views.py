# Create your views here.
from register.models import Event, Activity, School, Chaperone, Student
import datetime
from django.template import Context, loader
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext

def index(request):
	events_list = Event.objects.all()
	current_events_list = []
#	if len(events_list) == 0:
#		events_list.append("There are no upcoming events!")
#		current_events_list = events_list
	for e in events_list:
		if e.date_held >= datetime.datetime.today():
			current_events_list.append(e)

	template = loader.get_template('index.html')
	context = Context({
				'current_events_list': current_events_list,
	})
	return HttpResponse(template.render(context))

def detail(request, event_id):
	try:
		e = Event.objects.get(pk=event_id)
		template = loader.get_template('detail.html')
		context = Context({
				'Event':e,
		})	

	except Event.DoesNotExist:
		raise Http404
	return HttpResponse(template.render(context))	
#	return HttpResponse("You're looking at the details for event %s." % event_id)

#display the registration form
def registrationForm(request, event_id):
	e = get_object_or_404(Event, pk=event_id)
	#template = loader.get_template('register.html')
	number_of_students = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	grades = ['7','8','9','10', '11', '12']
	activity_list = e.activity_set.all()
	#context = Context({
	#		'Event':e, 'activity_list':activity_list, 'number_of_students':number_of_students, 'grades_list':grades, 
	#})
	return render_to_response('register.html',{'Event':e, 'activity_list':activity_list, 'number_of_students':number_of_students, 'grades_list':grades},  context_instance=RequestContext(request))

#	return HttpResponse(template.render(context))

#perform the register action
def register(request, event_id):
	e = Event.objects.get(id=event_id)
	try:
		e.school_set.create(
			event = event_id,
			school_name=request.POST['schoolName'],
			video_contest_p = request.POST['videoContest']
		)
		#Add the chaperones to the db and tie them to the school
		e.chaperone_set.create(
			event = event_id,
			chaperone_name = request.POST['chaperoneName1'],
			email_address = request.POST['chaperoneEmail1'],
			group=e.school_set.get(school_name=request.POST['schoolName'])
		)
		e.chaperone_set.create(
			event = event_id, 
			chaperone_name = request.POST['chaperoneName2'], 
			email_address = request.POST['chaperoneEmail2'], 
			group=e.school_set.get(school_name=request.POST['schoolName'])
		)
		#Add the students to the db and tie them to the school
		for kid in range(10):
			e.student_set.create(
				event = event_id, 
				group = e.school_set.get(school_name=request.POST['schoolName']), 
				student_name = request.POST['studentName'+str(kid+1)],
				grade = request.POST['studentGrade'+str(kid+1)],
				activity1 = e.activity_set.get(name = request.POST['studentActivity1_'+str(kid+1)]),
				activity2 = e.activity_set.get(name = request.POST['studentActivity2_'+str(kid+1)])
			)
	except Event.DoesNotExist:
		raise Http404
	else:	
		e.save()
		return HttpResponseRedirect(reverse('register.views.thanks', args=(event_id)))


def thanks(request, event_id):
	try:
		e = Event.objects.get(pk=event_id)
		template = loader.get_template('thanks.html')
		context = Context({
				'Event':e,
		})

	except Event.DoesNotExist:
		raise Http404
	return HttpResponse(template.render(context))


