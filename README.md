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
- Option to pre-load invitees so you can see whose RSVP is outstanding

Installation
------------
You deploy this thing yourself as a google app engine app.
Prerequisites:
- Google app engine utilities installed (you need these to deploy your site)
- Google account and app engine app created (your deployment target)

Instructions:
- Download the source
- Remove my details and replace with your own (especially app.yaml so you deploy to the right place)
- Deploy to GAE using the app engine tools
- Party