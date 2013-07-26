This file is for you to describe the remysmoke application. Typically
you would include information such as the information below:

Installation and Setup
======================

Install ``remysmoke`` using the setup.py script::

    $ cd remysmoke
    $ python setup.py install

Create the project database for any model classes defined::

    $ gearbox setup-app

Start the paste http server::

    $ gearbox serve

While developing you may want the server to reload after changes in package files (or its dependencies) are saved. This can be achieved easily by adding the --reload option::

    $ gearbox serve --reload

Then you are ready to go.
