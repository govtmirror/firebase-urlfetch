# web-client

An element providing a starting point for a web client using just Polymer Web Components.  It has a responsive layout with a title and menu area.  The content area is used to display web component "pages" which should have a menu item that that points to them via a matching "pagename" attribute.  Some sample pages are included in the demo, which will be expanded over time.  

Each content element is expected to implement setUp() and shutDown() methods which are called upon selection for display from the web-client.  Each content element also needs to implement a helpMe() method to provide context sensitive help.

Each content element is expected to manage its own data.  Certainly a great place for a firebase element. There is a "loading" dialog message in the web-client which can be called via a custom events "openMsg" and "closeMsg" from the pages.  It is possible for those events to conflict with those from other pages.  One might want to close the dialog on setUP() just in case its state is unknown?


## Dependencies

Element dependencies are managed via [Bower](http://bower.io/). You can
install that via:

    npm install -g bower

Then, go ahead and download the element's dependencies:

    bower install


## Playing With Your Element

If you wish to work on your element in isolation, we recommend that you use
[Polyserve](https://github.com/PolymerLabs/polyserve) to keep your element's
bower dependencies in line. You can install it via:

    npm install -g polyserve

And you can run it via:

    polyserve

Once running, you can preview your element at
`http://localhost:8080/components/web-client/`, where `web-client` is the name of the directory containing it.


## Testing Your Element  (not implemented yet, deadlines for a one-man operation ...)

Simply navigate to the `/test` directory of your element to run its tests. If
you are using Polyserve: `http://localhost:8080/components/web-client/test/`

### web-component-tester

The tests are compatible with [web-component-tester](https://github.com/Polymer/web-component-tester).
Install it via:

    npm install -g web-component-tester

Then, you can run your tests on _all_ of your local browsers via:

    wct

#### WCT Tips

`wct -l chrome` will only run tests in chrome.

`wct -p` will keep the browsers alive after test runs (refresh to re-run).

`wct test/some-file.html` will test only the files you specify.
