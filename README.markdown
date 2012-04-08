mPartsRegistry
=============

About
-----
<a href="http://mpartsregistry.appspot.com/">mPartsRegistry</a> is a simple interface to the <a href="http://partsregistry.org/">Registry of Standard Biological Parts</a> aimed
at mobile smartphone browsers. It's built using the <a href="http://partsregistry.org/Registry_API">Parts Registry API</a>, 
<a href="http://jquerymobile.com/">JQuery Mobile</a>, <a href="http://www.crummy.com/software/BeautifulSoup/">BeautifulSoup</a> and 
<a href="http://code.google.com/appengine/">Google App Engine</a>.

The goal is not to completely replicate the functionality of the Registry (at this stage
the API would not allow that anyhow), but to provide simple mobile-friendly interface to 
quickly look up important data about a Biobrick(tm) part in a laboratory setting, 
where accessing a desktop computer if often less convenient. 
In this context, you generally know the part name (eg B0034) that is written on a tube, 
but would like to quickly lookup some details (for instance, the size of the part in 
base pairs).

mPartsRegistry provides a simple 'bookmarking' feature, where a list of favorite parts can be
managed and stored on the device (via HTML5 localStorage).

mPartsRegistry is released under the MIT License. 
<br/>
<h3>Old screenshots of the jQTouch interface (it looks a little different now)</h3>
<br/>
 <img src="http://mpartsregistry.appspot.com/img/screenshot1.png" alt="mPartsRegistry screenshot, search page"/>
<br/> 
 <img src="http://mpartsregistry.appspot.com/img/screenshot2.png" alt="mPartsRegistry screenshot, GFP part page"/>
<br/> 
 <img src="http://mpartsregistry.appspot.com/img/QR_code.png" alt="QR code to http://mpartsregistry.appspot.com/#search"/>
<br/>
 **http://mpartsregistry.appspot.com/**
<br/>

Development and installation
----------------------------
If you just want to browse mPartsRegistry on your Webkit-enabled smartphone, 
go to <a href="http://mpartsregistry.appspot.com">http://mpartsregistry.appspot.com</a>
where there is a working version ready to use.

If you want to further develop mPartsRegistry and create your own custom installation, 
you'll need a need the 
<a href="http://code.google.com/appengine/downloads.html">App Engine SDK</a> and 
should follow the 
<a href="http://code.google.com/appengine/docs/python/gettingstarted/uploading.html">instructions on how to upload an app</a>.

Before you upload, you will need to change the *application:* name of the app in *src/app.yaml* 
from *mpartsregistry* to whatever you set it to in the App Engine dashboard.

Two convenience scripts are provided - *start-server.sh*, for starting the local development server, 
and *update-server.sh*, which uploads the app to App Engine. These scripts need to be edited to
reflect the path where you installed the App Engine SDK.

TODO
----
* Subpart support
* DNA feature support
* Twin support
