# Django Bookmarks app [![Build Status](https://travis-ci.org/zsolthajdu/django_bookmarks.svg?branch=master)](https://travis-ci.org/zsolthajdu/django_bookmarks) [![Known Vulnerabilities](https://snyk.io/test/github/zsolthajdu/django_bookmarks/badge.svg)](https://snyk.io/test/github/zsolthajdu/django_bookmarks)

Django app to store and access website bookmarks.
* Uses the [Django Rest framework](http://www.django-rest-framework.org) to provide a REST api.
* Uses the [Django Tagging](http://django-tagging.readthedocs.io/en/develop/) app to provide tagging of bookmarks.
  
## Current features
* adding bookmark urls and tags that are associated with the bookmark.
* looking up bookmarks by tag
* updating bookmarks
* deleting bookmarks
* private and public bookmarks. Public ones are visible without user login. Accessing private ones requires login.


# Description
The app can be used through an REST API to add/retrieve bookmark information.
Currently it doesn't provide html templates or user interface of any kind. It only deals with the management of bookmark information.

# Installation
## Get the app source
Get the app source package from Github:
```
git clone git@github.com:zsolthajdu/django_bookmarks.git .
```
Then you have to copy the bookmarks directory to you django project's directory.

## Using Bookmarks in a Django application
Once you copied the 'bookmarks' directory to the top folder of your Django project:

* Add 'bookmarks' to the INSTALLED_APPS setting of you project in settings.py.
* Run the command 'manage.py migrate' to update your project's database with the necessary table(s).

Also make sure Bookmarks' dependencies:

* the Django Rest Framework app
* the Django Tagging app

are also installed and included in your Django project.


# API
## Adding new bookmark
You have to log in as a Django user in order to be able to add new bookmarks.  
The details describing the bookmark has to be passed to the app in a POST request.  
The information has to be in JSON format, with the following fields included:

```language=javascript
{
  'url' : 'http://www.example.com',
  'title' : 'The Example Page',
  'description' : 'My favorite website !!',
  'tags' : 'favorites,example,bookmarks',
  'public' : false
}
```
  
* _url_ : the bookmark URL. It is a mandatory field. Max length is 2048 characters.
* _title_ : Max length is 255 characters.
* _description_ : Max length is 2048 characters.
* _tags_ : Comma separated list of tags associtated with the new bookmark. The max length of individual tags is determined by the MAX_TAG_LENGTH setting of the Tagging application.
* _public_ : Boolean value, default = 'false'. If set to true, the bookmark will be returned to users not logged in with any Django account.

## Getting list of all bookmarks
Requested by sending a GET request to the main bookmarks application url.  
Returns all bookmarks associated with current user, in JSON format.

The JSON object will include the following fields:
```
{
    "count": 211, // Number of bookmarks in the full list (all pages combined),
    "next":  "/bookmarks/page=4" // REST api to get next page of results or null if last page,
    "previous": "/bookmarks/page=2" // REST api to get previous page of results or null if this is the first page,
    "results": [  // An 'count' sized array of the bookmark objects.
        {
            "id": 23 ,//The database id number of this bookmark,
            "title": .. ,// Bookmark entry title,
            "owner": .. ,//The user who created this bookmark,
            "created": .. ,// creation date
            "description": .. , // bookmark description
            "url":  .., // bovokmark url
            "public": true,  // true if the bookmark can be accessed without logging in
            "tags": [ // list of tags associated with the bookmark
                "tag1",
                "tag2",
            ]
        }
    ]
}
```

The following examples assume that the app is accessed through the __/bookmarks__ path.

### Supported arguments
* page : to request a specific page of the results. Default is 1.
* page_size : Number of bookmarks in a single page of results. Default is 50.

Example: to get the second page of result with 25 items per page:
 ../bookmarks/?page_size=25&page=2

## Bookmark queries by ID
GET http://...../bookmarks/42  
Returns details of just bookmark 42, in JSON format.

## Bookmark queries by tag
Use a GET request with url __/tags__ added to the main application access point. Followed by a comma separated list of tags you want to search for.  
GET http://...../bookmarks/tags/tag1,tag2  

## Searching for a word
Use a GET request with url __/search__ added to the main application access point. Followed by a search term that the app will look for in bookmark titles and descriptions:

GET http://...../bookmarks/search/searchterm


## Bookmark queries by creation date
To find bookmarks that were created on a particular day, month or year, you can use the __/date/__ API.
Than specify the date, month and day as further path elements after /date/ , separated by a slash.

GET http://...../bookmarks/date/YEAR  
GET http://...../bookmarks/date/YEAR/MONTH  
GET http://...../bookmarks/date/YEAR/MONTH/DAY

## Getting a list of all tags
The same api that does tag search can also reutrn the full list of the current user's tags when called without any tags to search for.

GET http://...../bookmarks/tags

