Python Bitcoin GPU Miner
=======================================

This is a forked version of m0mchil's version.  I plan on doing some reworking to the client in the near future, for now this exists to be an easy installation version of the library.


## Installation (OSX)


I have only tested this on Mac OSX, but it should work on other *nix variants.

Pre-requisites:

*   XCode
*   Python 2.6.1
*   Boost (for PyOpenCL, see: http://wiki.tiker.net/PyOpenCL/Installation/Mac)

Let's get Boost installed.  My recommended way is through [brew](http://mxcl.github.com/homebrew/):

``` ruby -e "$(curl -fsSL https://raw.github.com/gist/323731)";
    brew install boost;
```

Site back and relax for this one, it took half an hour to compile on my brand new laptop.

Let's get [virtualenv](http://www.virtualenv.org/en/latest/) up and running.  This is going to be used to isolate our install of the miner.

``` easy_install virtualenv ```

Now let's create our new virtual environment:

``` virtualenv ~/.miner;
    cd ~/.miner;
    source bin/activate
 ```
 
Now the version of python and site-packages will be localized to this directory.  

Lastly, we will need to install numpy.  Due to some weirdness with PyOpenCL and the way it expects to find numpy we can't list it as a dependency in setup.py so it needs to be done by hand.

``` pip install numpy ```

After that we can install the miner:

``` pip install https://github.com/unscene/bitcoin-gpu-miner/tarball/master ```

##Usage

If you want detailed instructions run:

``` gpu_miner --help ```

To join a pooler like mining.bitcoin.cz you could issue the following on a *nix based system:

``` nohup gpu_miner -o api.bitcoin.cz -p 8332 -u <username>.<password> --pass <password> -d 0 & ```

This will detach the process from the shell and you can go on your merry way.