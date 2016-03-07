__author__ = 'Frenky'
import subprocess
import time
import datetime
import urllib2
import zipfile
from StratosphereConfig import __StratosphereConfig__
import StratosphereOutput


def download_file(url):
    StratosphereOutput.show('Downloading updates.', 2)

    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    StratosphereOutput.show(("Downloading: %s Bytes: %s" % (file_name, file_size)), 2)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl = len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        StratosphereOutput.show(status, 2)
    f.close()


def unzips(name):
    StratosphereOutput.show('Unziping file.', 3)
    fh = open(name + '.zip', 'rb')
    z = zipfile.ZipFile(fh)
    for i in z.namelist():
        z.extract(i, "./" + name)
    fh.close()


def download_manager():
    StratosphereOutput.show("Downloading new update.", 1)
    # Download classes StratosphereFlow, StratosphereWindow..
    download_file(__StratosphereConfig__.get_string_url_to_classes())
    # Download Models
    download_file(__StratosphereConfig__.get_string_url_to_models())
    unzips('models')
    # Download Modules
    download_file(__StratosphereConfig__.get_string_url_to_modules())
    unzips('modules')


def check_if_update():
    date_update = datetime.datetime.strptime(__StratosphereConfig__.get_string_date_string(), '%Y-%m-%d')
    date_now = datetime.datetime.now()
    if date_update < date_now:
        if __StratosphereConfig__.get_bool_forbidden() is False:
            StratosphereOutput.log('Downloading files.')
            download_manager()
            StratosphereOutput.show('Set config file.', 1)
            __StratosphereConfig__.set_config()
        else:
            StratosphereOutput.show("Updating is forbidden!", 1)


if __name__ == "__main__":

    # checking if
    check_if_update()

    # Path to Stratospehere Window
    path = 'C:\\Users\\frenk\\Documents\\Skola\\Stratosphere\\StratosphereWindowsIPS'

    # Create process.
    command = ('cat ' + path + '\\test8.binetflow | python ' + path + '\\StratosphereFlow.py')
    p = subprocess.Popen(command, shell=True)

    # Wait until process terminates.
    while True:
        if p.poll() is None:
            StratosphereOutput.show("Process is still runnning...", 3)
            time.sleep(__StratosphereConfig__.get_int_check_if_process_work())
        else:
            # This is coment for testig mode.
            # p = subprocess.Popen(command, shell=True)
            pass
    StratosphereOutput.show(("Process ended, ret code:", p.returncode), 2)
