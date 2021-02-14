from scrapy import cmdline
import time
import multiprocessing
import logging
from local_settings import settings

command = 'scrapy crawl %s' % settings['name']
loop = True
if settings['name'] == 'sinastaticlink1':
    command += ' -a syear=%d -a smonth=%d -a sday=%d -a eyear=%d -a emonth=%d -a eday=%d' % (settings['syear'],
                                                                                             settings['smonth'],
                                                                                             settings['sday'],
                                                                                             settings['eyear'],
                                                                                             settings['emonth'],
                                                                                             settings['eday'])
    loop = False
elif settings['name'] == 'sinastaticlink2':
    loop = False
if settings['name'] == 'sinadetail':
    delay = 1
elif settings['name'] == 'sinadynamiclink':
    delay = 1


class run:
    def task(self):
        cmdline.execute(command.split())

    def main_run(self):
        if loop:
            while True:
                pp = multiprocessing.Process(target=self.task)
                logging.info('pp run ')
                pp.start()
                pp.join()
                time.sleep(1)
        else:
            self.task()


if __name__ == '__main__':
    obj = run()
    obj.main_run()
