===========
User Manual
===========

django Organice is composend of the following main components:

#. `Content Management`_ (Cms)
#. `Blog`_ (Zinnia)
#. `Newsletter`_

`Content Management`:index:
===========================

Editing your website is not much different from surfing the web.  When you're logged in to your website you will have
the django CMS toolbar on top of the page.  Slide the "Edit mode" button to the "ON" state, and some elements of the
page you're currently on start having additional toolbars to add and edit content in those areas.

You can safely modify content on the page without the website to change.  Only you can see the changes, and only as
long as you are in Edit mode.  When you're happy with the changes press the blue "Publish" button on the django CMS
toolbar to make your version visible to the world.

For more technical tasks like creating a navigation structure, adding pages, etc. the django CMS toolbar redirects you
to the Django administration interface.  Want to have an upfront first impression before using it?  Check out the
(slightly outdated) django CMS `video on frontend-editing`_.

`Blog`:index:
=============

Writing and publishing interesting articles now and then is called "blogging".  It's very similar to the usual editing
of your website, but still it's different because you get more features as a natural add-on:  Categories, tagging,
comments, publication dates, archives (yearly, monthly, daily), related entries, RSS feeds, etc.

On your website you simply go to the Blog area, and click on the "Add" link, which is available when you're logged in.
In the blog entry editor you have all functionality you already know from the content management section.  Modifying
existing blog entries works identical to the usual content changes on your website with the exception of publishing,
which is not available with an intermediate draft step:  All your changes are immediately visible online.

Note that in django Organice we also use the blog functionality for other use cases that are very similar to the usual
blogging, such as event agendas, job postings, press releases, download lists, etc.

`Newsletter`:index:
===================

Sending out news or updates to a circle of friends or customers is managed by the Newsletter component, which is
available from the Django administration interface when you're logged in to your website.  Simply click on
"Admin > Site Administration" on the django CMS toolbar, and go to the Newsletter section in Django administration.

This component has a couple of powerful features.  It's best explained having you watch the interesting French
`overview video`_ from the Emencia website.


.. _`video on frontend-editing`: http://vimeo.com/7126991
.. _`overview video`: http://vimeo.com/16793999
