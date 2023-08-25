import logging
logger = logging.getLogger(__name__)

class PlaysoundException(Exception): pass

def _canonicalizePath(path):
    import sys
    if sys.version_info[0] >= 3: return str(path)
    else: return path

def _playsoundWin(sound, block = True):
    sound = _canonicalizePath(sound)

    if any((c in sound for c in ' "\'()')):
        from os       import close, remove
        from os.path  import splitext
        from shutil   import copy
        from tempfile import mkstemp
        
        fd, tempPath = mkstemp(prefix = 'PS', suffix = splitext(sound)[1])
        logger.info('Made a temporary copy of {} at {} - use other filenames with only safe characters to avoid this.'.format(sound, tempPath))
        copy(sound, tempPath)
        close(fd)
        try: _playsoundWin(tempPath, block)
        finally: remove(tempPath)
        return

    from ctypes import c_buffer, windll
    from time   import sleep

    def winCommand(*command):
        bufLen = 600
        buf = c_buffer(bufLen)
        command = ' '.join(command).encode('utf-16')
        errorCode = int(windll.winmm.mciSendStringW(command, buf, bufLen - 1, 0))
        if errorCode:
            errorBuffer = c_buffer(bufLen)
            windll.winmm.mciGetErrorStringW(errorCode, errorBuffer, bufLen - 1)
            exceptionMessage = ('\n    Error ' + str(errorCode) + ' for command:''\n        ' + command.decode('utf-16') +'\n    ' + errorBuffer.raw.decode('utf-16').rstrip('\0'))
            logger.error(exceptionMessage)
            raise PlaysoundException(exceptionMessage)
        return buf.value

    if '\\' in sound: sound = '"' + sound + '"'

    try:
        logger.debug('Starting')
        winCommand(u'open {}'.format(sound))
        winCommand(u'play {}{}'.format(sound, ' wait' if block else ''))
        logger.debug('Returning')
    finally:
        try: winCommand(u'close {}'.format(sound))
        except PlaysoundException: logger.warning(u'Failed to close the file: {}'.format(sound));pass

def _handlePathOSX(sound):
    sound = _canonicalizePath(sound)

    if '://' not in sound:
        if not sound.startswith('/'):
            from os import getcwd
            sound = getcwd() + '/' + sound
        sound = 'file://' + sound

    try: sound.encode('ascii');return sound.replace(' ', '%20')
    except UnicodeEncodeError:
        try: from urllib.parse import quote
        except ImportError: from urllib import quote

        parts = sound.split('://', 1)
        return parts[0] + '://' + quote(parts[1].encode('utf-8')).replace(' ', '%20')


def _playsoundOSX(sound, block = True):
    try: from AppKit import NSSound
    except ImportError:
        logger.warning("playsound could not find a copy of AppKit - falling back to using macOS's system copy.")
        sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/PyObjC')
        from AppKit import NSSound

    from Foundation import NSURL
    from time       import sleep

    sound = _handlePathOSX(sound)
    url   = NSURL.URLWithString_(sound)
    if not url: raise PlaysoundException('Cannot find a sound with filename: ' + sound)

    for i in range(5):
        nssound = NSSound.alloc().initWithContentsOfURL_byReference_(url, True)
        if nssound: break
        else: logger.debug('Failed to load sound, although url was good... ' + sound)
    else: raise PlaysoundException('Could not load sound with filename, although URL was good... ' + sound)
    nssound.play()

    if block: sleep(nssound.duration())

def _playsoundNix(sound, block = True):
    sound = _canonicalizePath(sound)

    from os.path import abspath, exists
    try: from urllib.request import pathname2url
    except ImportError: from urllib import pathname2url

    import gi
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst

    Gst.init(None)

    playbin = Gst.ElementFactory.make('playbin', 'playbin')
    if sound.startswith(('http://', 'https://')):
        playbin.props.uri = sound
    else:
        path = abspath(sound)
        if not exists(path):
            raise PlaysoundException(u'File not found: {}'.format(path))
        playbin.props.uri = 'file://' + pathname2url(path)


    set_result = playbin.set_state(Gst.State.PLAYING)
    if set_result != Gst.StateChangeReturn.ASYNC:
        raise PlaysoundException(
            "playbin.set_state returned " + repr(set_result))

    logger.debug('Starting play')
    if block:
        bus = playbin.get_bus()
        try: bus.poll(Gst.MessageType.EOS, Gst.CLOCK_TIME_NONE)
        finally: playbin.set_state(Gst.State.NULL)
            
    logger.debug('Finishing play')

def _playsoundAnotherPython(otherPython, sound, block = True, macOS = False):
    from inspect    import getsourcefile
    from os.path    import abspath, exists
    from subprocess import check_call
    from threading  import Thread

    sound = _canonicalizePath(sound)

    class PropogatingThread(Thread):
        def run(self):
            self.exc = None
            try: self.ret = self._target(*self._args, **self._kwargs)
            except BaseException as e: self.exc = e

        def join(self, timeout = None):
            super().join(timeout)
            if self.exc: raise self.exc
            return self.ret

    if not exists(abspath(sound)): raise PlaysoundException('Cannot find a sound with filename: ' + sound)

    playsoundPath = abspath(getsourcefile(lambda: 0))
    t = PropogatingThread(target = lambda: check_call([otherPython, playsoundPath, _handlePathOSX(sound) if macOS else sound]))
    t.start()
    if block: t.join()

from platform import system
system = system()

if system == 'Windows': playsound = _playsoundWin
elif system == 'Darwin':
    playsound = _playsoundOSX
    import sys
    if sys.version_info[0] > 2:
        try: from AppKit import NSSound
        except ImportError:
            logger.warning("playsound is relying on a python 2 subprocess. Please use `pip3 install PyObjC` if you want playsound to run more efficiently.")
            playsound = lambda sound, block = True: _playsoundAnotherPython('/System/Library/Frameworks/Python.framework/Versions/2.7/bin/python', sound, block, macOS = True)
else:
    playsound = _playsoundNix
    if __name__ != '__main__':
        try:
            import gi
            gi.require_version('Gst', '1.0')
            from gi.repository import Gst
        except:
            logger.warning("playsound is relying on another python subprocess. Please use `pip install pygobject` if you want playsound to run more efficiently.")
            playsound = lambda sound, block = True: _playsoundAnotherPython('/usr/bin/python3', sound, block, macOS = False)

del system

if __name__ == '__main__':
    from sys import argv
    playsound(argv[1])
