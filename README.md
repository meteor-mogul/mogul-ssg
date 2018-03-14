# Meteor Mogul static site generator (mogul-ssg)

## What

Generate a "static site" from a Meteor Mogul app.  A static site is a bundle that does not need an open server connection, so it can run on any web server or directly from a filesystem.

Once the code is in a browser, then all the client-side code can run there.

This is a work-in-progress.  Apps that are intended to be static sites will need to be designed so they work without a server connection.

The basic idea is to use web mirroring software to make a copy of the `.html`, `.js`, `.css` and font code that Meteor bundles into a single-page app.

Some filenames need to be cleaned up, and then the SPA can be hosted by any web server without needing Node.js on the server.  All the code runs on the browser; the server just sends it all when requested.

## Why

I would like to use Meteor Mogul to write my static web site to be hosted on Netlify, without having to worry about Netlify doing anything more than serve up files when requested by a browser.

Being able to create a bundle that does not require a Node.js server also makes it easier to share demos.  For example, using python's SimpleHTTPServer module it's very easy to run a static site:

```
$ cd <path-to-static-site-files>
$ python -m SimpleHTTPServer <port>
```

## How

Being a work-in-progress, this is a bit more involved than ideal.  Here are the steps to get it working.

1. Compile and install (if necessary) a recent version of [`wget`](https://www.gnu.org/software/wget/)
1. Start two shells
1. In one of the shells, start your Meteor Mogul app listening on localhost:3000 (or whatever port you want).
1. In the other shell, prepare a directory for the static site files and run the static site generator scripts:

```
$ cd <root-dir-for-static-sites>
$ mkdir <static-site-dir>
$ mogul-ssg.sh <static-site-dir> <optional-app-URL>
$ python static-site.py <static-site-dir>
```

`mogul-ssg.sh` runs `wget`, mirroring files to `<static-site-dir>` and connecting by default to `http://localhost:3000/` unless you give it another application URL to try.

`static-site.py` renames files and replaces links in `index.html` with the renamed files.

To test your static site files:

```
$ cd <static-site-dir>
$ python -m SimpleHTTPServer <port>
```

Then you can browse `http://localhost:<port>` to test the static site version of your app.
