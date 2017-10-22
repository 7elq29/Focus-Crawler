from spider.spider_controller import SpiderController
from spider.focus_spider import FocusSpider

import multiprocessing


lock = multiprocessing.Lock()
shared_queue = multiprocessing.Queue()
cpu_num = 1  # multiprocessing.cpu_count()
start_urls = ['https://en.wikipedia.org/wiki/Main_Page']


def run_process(args):
    squeue, process_num = args
    SpiderController.run(squeue, process_num)


def start():
    manager = multiprocessing.Manager()
    q = manager.Queue()
    for url in start_urls:
        q.put(url)
    pool = multiprocessing.Pool(processes=cpu_num)
    pool.map(run_process, list(zip([q] * cpu_num, range(cpu_num))))

    pool.close()
    pool.join()


if __name__ == '__main__':
    start()
    # s = FocusSpider()
    # s.parse("https://en.wikipedia.org/wiki/Main_Page")

