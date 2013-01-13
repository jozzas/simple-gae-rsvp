#!/usr/bin/env python

import os
import datetime
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
#from appengine_utilities import sessions

template.register_template_library('django.contrib.humanize.templatetags.humanize')

DEBUGGING = False
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
CONFIRMATION_EMAIL_SUBJECT = "RSVP Confirmation for J and J's wedding"
EMAIL_SENDER_ADDRESS = "John and Julia <jozzas@gmail.com>"
DEADLINE = datetime.date(2012, 12, 25)

JQUERY_DATE_FORMAT = '%m/%d/%Y'
JsDate = lambda pydate: pydate.strftime(JQUERY_DATE_FORMAT)
Names = lambda party: [p.name for p in party.people.order('creation_date')]

class Rsvp(db.Model):
  """Represents one party, meaning one invitation receipient."""
  creation_date = db.DateTimeProperty(auto_now=True)
  is_coming  = db.BooleanProperty(required=True)
  main_name  = db.StringProperty(required=True)
  main_email = db.EmailProperty(required=True)
  main_phone = db.StringProperty(required=True)
  num_guests = db.IntegerProperty(required=True)
  name2 = db.StringProperty()
  req2  = db.StringProperty()
  name3 = db.StringProperty()
  req3  = db.StringProperty()
  name4 = db.StringProperty()
  req4  = db.StringProperty()
  name5 = db.StringProperty()
  req5  = db.StringProperty()
  
  def sorted_attrs(self):
    _out = []
    for key in sorted(self.__dict__):
      if key not in ['_Model__namespace','_app', '_entity','_parent','_parent_key']:
        _out.append(self.__dict__[key])
    return _out

class RequestHandler(webapp.RequestHandler):
  """Subclass RequestHandler to add some convenience methods."""
  def WriteTemplate(self, filename, template_vars):
    """Write out to a template in the standard template directory."""
    template_vars['deadline'] = DEADLINE # always include RSVP due date
    self.response.out.write(template.render(os.path.join(TEMPLATE_DIR, filename), template_vars))

  def DEBUG(self, msg):
    if not DEBUGGING:
      return
    self.response.out.write('DEBUG: ' + msg + '<br />')

  def ERROR(self, msg, filename='error.html', template_vars={}):
    template_vars['errormessage'] = msg
    self.WriteTemplate(filename, template_vars)

  def NAVERROR(self):
    self.WriteTemplate('get_keyword.html', {'errormessage': 'Sorry, browsing directly to that page is not supported.  Please re-enter your secret word.'})

  def get(self):
    self.NAVERROR()

class LandingWithoutKeyword(RequestHandler):
  """Initial Page that shows RSVP form """
  def get(self):
    self.WriteTemplate('is_coming.html', {})

class Details(RequestHandler): #Was detailspage
  def get(self):
    self.WriteTemplate('details.html',{})

class ProcessRequest(RequestHandler):
  def post(self):
    """Process an RSVP request. Store info."""
    
    self.DEBUG(str(self.request.arguments()))
    
    is_coming = self.request.get('coming')
    if is_coming == 'Yes':
      is_coming = True
    else:
      is_coming = False
    
    main_name = self.request.get('name')
    main_email = self.request.get('email')
    main_phone = self.request.get('phone')
    num_guests = int(self.request.get('totalnumber'))
    
    name2 = self.request.get('2name')
    req2  = self.request.get('2spec')
    name3 = self.request.get('3name')
    req3  = self.request.get('3spec')
    name4 = self.request.get('4name')
    req4  = self.request.get('4spec')
    name5 = self.request.get('5name')
    req5  = self.request.get('5spec')
    
    self.DEBUG("RSVP Submitted, num guests "+str(num_guests))
    self.DEBUG("Is coming? " + str(is_coming)) 
    
    Rsvp(is_coming=is_coming,main_name=main_name,main_email=main_email,
             main_phone=main_phone, num_guests=num_guests,
             name2=name2,req2=req2,
             name3=name3,req3=req3,
             name4=name4,req4=req4,
             name5=name5,req5=req5).put()
    
    self.sendconfirmation(is_coming, main_email, main_name)
    
    self.WriteTemplate('details.html', {'name':main_name, 'is_coming':is_coming, 'not_coming':not is_coming})
  
  def get(self):
    """ Request without form, send to details page"""
    self.WriteTemplate('details.html', {})
  
  def sendconfirmation(self, is_coming, to_email, name):
    """Send a multipart MIME message to the person who just RSVPd."""
    template_vars = {'is_coming':is_coming,
                    'not_coming':not is_coming,
                    'name': name}
    
    text = template.render(os.path.join(TEMPLATE_DIR, 'email_confirmation.txt'), template_vars)
    html = template.render(os.path.join(TEMPLATE_DIR, 'email_confirmation.html'), template_vars)
    mail.send_mail(sender=EMAIL_SENDER_ADDRESS,
                   to='%s <%s>' % (name, to_email),
                   subject=CONFIRMATION_EMAIL_SUBJECT,
                   body=text,
                   html=html)

class Report(RequestHandler):
  def get(self):
    coming = []
    not_coming = []
    by_cdate = lambda p: sorted(p, key=cdate, reverse=True)
    
    for party in Rsvp.all():
      if party.is_coming:
        coming.append(party)
      else:
        not_coming.append(party)
    
    cdate = lambda p: p.creation_date
    by_cdate = lambda p: sorted(p, key=cdate, reverse=True)
    template_vars = {'coming': by_cdate(coming),
                     'not_coming': by_cdate(not_coming)}
    self.WriteTemplate('report.html', template_vars)

def main():
   application = webapp.WSGIApplication([('/', LandingWithoutKeyword),
                                         ('/details', Details),
                                         ('/process_request',ProcessRequest),
                                         #('/test', PopulateTestData),
                                         #('/secretword', SecretWord),
                                         #('/yesorno', YesOrNo),
                                         #('/savedetails', PartyDetails),
                                         #('/tripdetail', TripDetails),
                                         ('/totallysafeforwork', Report)],
                                        debug=DEBUGGING)
   util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
