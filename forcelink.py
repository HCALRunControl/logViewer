from os import symlink, remove
import errno
# copied over from https://github.com/jhakala/Vg
def force_symlink(target, linkName):
    try:
        symlink(target, linkName)
    except OSError, e:
        if e.errno == errno.EEXIST:
            print "  >>> removing symlink %s and creating a replacement to point to %s" % ( linkName, target )
            remove(linkName)
            symlink(target, linkName)
