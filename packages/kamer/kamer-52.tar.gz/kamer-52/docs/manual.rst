.. _manual:


.. raw:: html

    <br>


.. title:: Manual


.. raw:: html

    <center>

manual
######

.. raw:: html

    </center>
    <br>


**NAME**

 ``KAMER`` - Reconsider OTP-CR-117/19


**SYNOPSIS**

 ::

  kamer <cmd> [key=val] 
  kamer <cmd> [key==val]
  kamer [-c] [-d] [-v]


**DESCRIPTION**


 ``KAMER`` is a python3 IRC bot is intended to be programmable  in a
 static, only code, no popen, no user imports and no reading modules from
 a directory, way. It can show genocide and suicide stats of king netherlands
 his genocide into a IRC channel, display rss feeds and log simple text
 messages, source is `here <source.html>`_.



**INSTALL**

 with sudo::

  $ python3 -m pip install kamer

 as user::

  $ pipx install kamer

 or download the tar, see::

  https://pypi.org/project/kamer


**USAGE**


 list of commands::

    $ kamer cmd
    cmd,err,flt,sts,thr,upt

 start a console::

    $ kamer -c
    >

 start additional modules::

    $ kamer mod=<mod1,mod2> -c
    >

 list of modules::

    $ kamer mod
    cmd,err,flt,fnd,irc,log,mdl,mod,
    req, rss,slg,sts,tdo,thr,upt,ver

 to start irc, add mod=irc when
 starting::

     $ kamer mod=irc -c

 to start rss, also add mod=rss
 when starting::

     $ kamer mod=irc,rss -c

 start as daemon::

    $ kamer mod=irc,rss -d
    $ 


**CONFIGURATION**


 *irc*

 ::

    $ kamer cfg server=<server>
    $ kamer cfg channel=<channel>
    $ kamer cfg nick=<nick>

 *sasl*

 ::

    $ kamer pwd <nsvnick> <nspass>
    $ kamer cfg password=<frompwd>

 *rss*

 ::

    $ kamer rss <url>
    $ kamer dpl <url> <item1,item2>
    $ kamer rem <url>
    $ kamer nme <url< <name>


**COMMANDS**


 ::

    cmd - commands
    cfg - irc configuration
    dlt - remove a user
    dpl - sets display items
    ftc - runs a fetching batch
    fnd - find objects 
    flt - instances registered
    log - log some text
    mdl - genocide model
    met - add a user
    mre - displays cached output
    nck - changes nick on irc
    now - genocide stats
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    req - reconsider
    rss - add a feed
    slg - slogan
    thr - show the running threads
    tpc - genocide stats into topic


**FILES**

 ::

    ~/.local/bin/kamer
    ~/.local/pipx/venvs/kamer/
    /usr/local/bin/kamer
    /usr/local/share/docs/kamer


**AUTHOR**


 ::
 
    Bart Thate <bthate@dds.nl>


**COPYRIGHT**

 ::

    KAMER is Public Domain.
