GITHUB

$ git init
$ git add .
$ git commit -m "First commit"
$ git remote add origin remote repository URL
    # Sets the new remote
    $ git remote -v
    # Verifies the new remote URL

WITH PYCHARM START HERE

$ git push origin master

With Pycharm; you only need to push.

<small class="mr-2">with <span class="text-muted">{{tag.tags.all|join:", "}}</span></small>

--- let the result of the search be rendered...

#################################################################
#################################################################  Get all Tagged Objects by Specific User
#################################################################

from django.contrib.auth.models import User
from taggit.models import Tag

u = User.objects.get(username=username)
tags = Tag.objects.filter(object__owner=u)

#################################################################
#################################################################  DJANGO TAGGIT
#################################################################

>>> apple = Food.objects.create(name="apple")
>>> apple.tags.add("red", "green", "delicious")
>>> apple.tags.all()
[<Tag: red>, <Tag: green>, <Tag: delicious>]
>>> apple.tags.remove("green")
>>> apple.tags.all()
[<Tag: red>, <Tag: delicious>]
>>> Food.objects.filter(tags__name__in=["red"])
[<Food: apple>, <Food: cherry>]