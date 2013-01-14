Simple Google App Engine RSVP
=============================

I am a very, very basic Google App Engine RSVP system. I do weddings and parties. I'll be here all week, folks.

It's essentially just one RSVP form and a details page. It doesn't have a secret word system, because those are clunky.

It sends confirmation emails and theres a report you can view to see who's been RSVPing.

Features:
---------
- A form that takes participant info and stores it
- Automated confirmation emails
- Confirmation screen on submission
- Simple report for organisers to see who has RSVPed
- Details page for displaying event details
- Nothing else. That's the idea.

Originally loosely based on http://larry-laura-rsvp.googlecode.com

Possible future features:
- Optional "email the organiser" every time someone RSVPs
- More configuration so that you don't have to change my details out all over the place
- Separate config file so that all configuration is done in one place
- Option to pre-load invitees so you can see whose RSVP is outstanding

Installation
------------
You deploy this thing yourself as a google app engine app.
Prerequisites:
- [Python](http://http://python.org/) 2.6 or later
- [Google app engine SDK](http://developers.google.com/appengine/downloads) for Python
- A place to deploy to: You need a Google account and [empty app engine app created](http://appspot.com) (your_project_name.appspot.com address)

Creating Your Site
------------------
- Download and extract the source
- Remove any existing details and replace with your own in `app.yaml`, all template HTML, variables in `main.py`
- Test on your local computer by running `dev_appserver.py path_to_your_app` from the SDK and point a browser at `http://localhost:8080`
- Deploy to GAE site using the app engine tools: `appcfg.py update name_of_app_folder/`
- Share the link and watch the RSVPs roll in
- Party!
