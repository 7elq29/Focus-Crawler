import threading, time, multiprocessing
from spider.focus_spider import FocusSpider
from multiprocessing.pool import ThreadPool


class SpiderController:

    process_num = None
    thread_count = 1

    @staticmethod
    def _worker(args):
        q, thread_num = args
        print('Process #{}, thread #{}'.format(SpiderController.process_num, thread_num))
        waiting = 0
        spider = FocusSpider()
        while q.qsize() > 0 or waiting < 5:
            if q.qsize() == 0:
                waiting += 1
                time.sleep(5)
            else:
                url = q.get()
                for link in spider.parse(url):
                    q.put(link)
                q.task_done()
                waiting = 0

    @staticmethod
    def run(q, process_num):
        SpiderController.process_num = process_num
        pool = ThreadPool(SpiderController.thread_count)
        pool.map(SpiderController._worker, list(zip([q] * SpiderController.thread_count,
                                                    range(SpiderController.thread_count))))
        pool.close()
        pool.join()
