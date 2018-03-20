# Meteor Mogul static site generator (mogul-ssg)

## What

Generate a "static single-page application (SPA)" from a Meteor Mogul app.  A static SPA is an app that does not need to keep open a server connection, so it can run on any web server or directly from a filesystem.

With a static SPA, once the server has delivered the code bundle to a browser, its job is done.  The client-side code can run in the browser and no further communication with the server is necessary.

This is a work-in-progress.  Meteor Mogul apps that are intended to be static will need to be designed so they work without a server connection.

Meteor takes care of bundling code into a single-page app (SPA).  The basic idea of `mogul-ssg` is to use web mirroring software to make a copy of all the images, fonts and other assets along with the `.html`, `.js`, and `.css` code that Meteor bundles into a SPA.

With a few tweaks, a Meteor SPA can become a static SPA that can be hosted by any web server without needing Node.js on the server.  All the code runs on the browser; the server just sends the static SPA once when requested by a client.

## Why

I would like to use Meteor Mogul to write a web site to be hosted on [Netlify](https://www.netlify.com/), without having to worry about Netlify doing anything more than serve up a bundle of files when requested by a browser.

Creating a static SPA that does not require a Node.js server also makes it easier to share demos.  For example, using python's SimpleHTTPServer module it's very easy to serve a static SPA:

```
$ cd <path-to-static-spa-files>
$ python -m SimpleHTTPServer <port>
```

The set of packages used by `meteor-base` includes some that try to keep a DDP connection going to the server.  While an app will continue to work even if its DDP connection requests fail, it is annoying and wasteful to have these requests being made over the network by a static SPA, so those packages are removed to prevent needless DDP requests going to the server.

Generating a static SPA from a regular Meteor SPA removes DDP packages to eliminate spurious `Failed to load resource: the server responded with a status of 404 (File not found)` errors when the client asks for `/sockjs/info?cb=<token>`.

## How

First, write your app in Meteor per usual, except don't rely on any continuing connection to the server.  Avoid DDP, Accounts, Mongo, any other server-side code.  Routes, etc. should all be done in client code only.

To make your life simple, use client-side routing to follow Meteor's standard pattern of a single-page application which will consist of one `.html` file called `index.html`.  That one `.html` file will load all of the `.js` and `.css` code your app needs.  It will also have links to all the fonts, images and other assets your app needs.

Once your Meteor app is working, run the `mogul-ssg.sh` script from this repo to make a copy of the `.html`, `.js`, and `.css` code that meteor bundles up for you, plus a copy of all the fonts, images and other assets your app needs.

Two programs do the actual copying.

First, PhantomJS gets the `index.html` and saves the DOM after the JavaScript has had a chance to do its thing.

Then [`wget`](https://www.gnu.org/software/wget/) processes the `index.html` file to get all the pre-requisites.  The `mogul-ssg.sh` shell script runs `wget` with a set of arguments that makes copies all of the required files.  Then, after the SPA bundle has been generated, `mogul-ssg.sh` calls the `staticify-spa.py` script which tweaks filenames and links and removes DDP packages to make the bundle into a static SPA.

Being a work-in-progress, this is a bit more involved than ideal.  Here are the steps to get it working:

1. Start two shells.
1. From one of the shells try the following steps.
1. Try `$ phantomjs --version` to see if you already have `phantomjs`.  If you don't: download a recent version of [`PhantomJS`](http://phantomjs.org/download.html).
1. Try `$ wget --version` to see if you already have `wget`.  If you don't: download, compile and install a recent version of [`GNU wget`](https://www.gnu.org/software/wget/).
1. Make sure both `phantomjs` and `wget` are in your PATH.  I recommend installing them in `/usr/local/bin`.  
1. Start your Meteor Mogul app.  By default it will start listening for HTTP messages on port 3000 of localhost.

```
$ cd <path-to-meteor-app>
$ meteor
```

1. In the other shell, prepare a directory for the static SPA bundle and run the static site generator script:

```
$ cd <root-dir-for-static-sites>
$ mkdir <static-site-dir>
$ mogul-ssg.sh <static-site-dir> <optional-app-URL>
```

`mogul-ssg.sh` runs `wget`, mirroring files to the `<static-site-dir>` you specify and connecting by default to `http://localhost:3000/` unless you give it another application URL to try.  For example, if you want to bundle up a Meteor app running at http://your.staging.server.us and store the files in a `~/Sites/static-spa` folder, you could do `mogul-ssg.sh ~/Sites/static-spa http://your.staging.server.us`.

`staticify-spa.py` does a bit of work on the bundle to make the static SPA work and not send DDP requests to the server:

1. Renames files to remove hash values.
2. Replaces links in `index.html` with the renamed files.
3. Removes DDP packages so client doesn't send DDP requests to the server.

To test your static SPA once the script has finished:

```
$ cd <static-site-dir>
$ python -m SimpleHTTPServer <port>
```

Then you can browse `http://localhost:<port>` to test the static version of your app.  If your app runs entirely client side it will work; if it requires any ongoing connection to the server it won't.

Once your static SPA is working, you can simply copy the bundle to any host to publish it.
