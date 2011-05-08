Introduction
============

Hip hop music is notorious for adding extra information into the artist
and track names. This script helps you normalize and move those pesky
``(Feat. Some Artist)`` strings in your iTunes library. The script
allows you to make a selection in iTunes, then run the script against
those tracks from the command line.

Code Repository
  https://github.com/claytron/claytron.featuring
PyPi
  http://pypi.python.org/pypi/claytron.featuring/
Issues
  https://github.com/claytron/claytron.featuring/issues

Installation
------------

This script can be installed with pip. I would also recommend installing
it into a virtualenv::

    $ pip install -U claytron.featuring

Usage
-----

You can see the usage string from the ``-h`` option::

    $ featuring_fix -h
    Usage: featuring_fix [options]
    
    This script will allow you to modify the tracks in your iTunes database.
    Select the items that you want to modify in iTunes, then run this script from
    the command line using the options below. The "featuring" strings will be
    normalized and added to the comment tag as (Featuring Some Artist). The
    previous contents of the comment will be left intact.
    
    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -r, --real-run        Change the iTunes database (default: False)
      -c, --with-csv        Write change info into a CSV file
      -w, --featuring-with  Take care of 'with'
      -n, --no-parens       Process the tracks without parenthesis (be CAREFUL
                            with this option, since "featuring" is a common word)

By default the script does not modify the iTunes database since there is
no real undo in iTunes. If you want to see what the result of the
modification will be, you can run ``featuring_fix`` with the csv output
option::

    $ featuring_fix -c

If you want to modify the files in your library, you must use the ``-r``
option::

    $ featuring_fix -r

WARNING: This can take a long time to process a large selection of
tracks. If you want to run it against your whole library, make sure and
have some music playing, then go grab a coffee.

Featuring Styles
----------------

There are many different ways in which a track can be tagged as
"featuring" an artist. A few examples::

    Featuring Mr. Lif
    Feat. Mr. Lif
    Ft. Mr. Lif
    f. Mr. Lif
    f/Mr. Lif
    with Mr. Lif
    w/Mr. lif

And I'm sure there are other incarnations of these EVIL strings.
Currently the script can handle all but the ``w/`` and ``f/`` items from
the list above.
