import os.path
testfile = os.path.join(os.path.dirname(__file__), '..', 'README.rst')
if __name__=="__main__":
    import doctest
    doctest.testfile(testfile)
