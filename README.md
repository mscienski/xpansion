# xpansion
expand abbreviations in slack

A quick and dirty python WSGI script for deployment to Heroku to respond to `/xpansion [acronym]` in slack

Pulls Wikipedia pages for the acronym/initialism (e.g. http://www.wikipedia.org/wiki/PSA) and picks a random list entry to respond with.
