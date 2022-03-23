import sys
import os
import time
from robot.libraries.BuiltIn import BuiltIn
from robot.output.logger import LOGGER

class runKeywordAsync:
    def __init__(self):
        self._thread_pool = {}
        self._thread_pool['default']={}
        self._last_thread_handle = 1
        self._last_thread_handle_pool = {}
        self._last_thread_handle_pool['default'] = 1 

    def run_method_async(self, keyword, *args, **kwargs):
        handle = self._last_thread_handle_pool['default']
        thread = self._threaded_method(keyword, *args, **kwargs)
        thread.start()
        self._thread_pool['default'][handle] = thread
        self._last_thread_handle_pool['default'] = int(self._last_thread_handle_pool['default']) + 1
        return handle
    
    def run_method_async_with_custom_pool(self, pool, keyword, *args, **kwargs):
        if pool not in self._thread_pool:
            self._thread_pool[pool] = {}
            self._last_thread_handle_pool[pool] = 1        
        handle = self._last_thread_handle_pool[pool]
        thread = self._threaded_method(keyword, *args, **kwargs)
        thread.start()
        self._thread_pool[pool][handle] = thread
        self._last_thread_handle_pool[pool] = int(self._last_thread_handle_pool[pool]) + 1
        return handle

    def run_keyword_async(self, keyword, *args):
        handle = self._last_thread_handle_pool['default']
        thread = self._threaded(keyword, *args)
        thread.start()
        self._thread_pool['default'][handle] = thread
        self._last_thread_handle_pool['default'] = int(self._last_thread_handle_pool['default']) + 1 
        return handle
    
    def run_keyword_async_with_custom_pool(self, pool ,keyword, *args):
        if pool not in self._thread_pool:
            self._thread_pool[pool] = {}
            self._last_thread_handle_pool[pool] = 1
        handle = self._last_thread_handle_pool[pool]
        thread = self._threaded(keyword, *args)
        thread.start()
        self._thread_pool[pool][handle] = thread
        self._last_thread_handle_pool[pool] = int(self._last_thread_handle_pool[pool]) + 1
        return handle

    def wait_async_all(self, pool='default', timeout=60):
        timeout = int(timeout)
        results = []
        if pool not in self._thread_pool:
            raise Exception("Pool " + pool + " has not been created")
        for thread in self._thread_pool[pool]:
            thread_id = str(thread)
            try:
              result = self._thread_pool[pool][thread].result_queue.get(True, timeout)
              results.append(result)
            except:
              for thread in self._thread_pool[pool]:
                  self._thread_pool[pool][thread].terminate()
              self._last_thread_handle_pool[pool] = 1
              raise Exception("Process " + thread_id + " Failed")
        self._thread_pool[pool] = {}
        self._last_thread_handle_pool[pool] = 1
        return results

    def get_async_return(self, handle, pool='default', timeout=60):
        timeout = int(timeout)
        if handle in self._thread_pool[pool]:
            try:
              result = self._thread_pool[pool][handle].result_queue.get(True, timeout)
              del self._thread_pool[handle]
              return result
            except:
              raise Exception("Process " + str(handle) + " Failed")
        else:
            raise Exception("Passed Process id " + str(handle) + " is not a valid id")

    def _threaded_method(self, keyword, *args, **kwargs):
        from multiprocessing import Queue
        from multiprocessing import Process

        def wrapped_f(q, *args, **kwargs):
            ''' Calls the decorated function and puts the result in a queue '''
            ret = BuiltIn().call_method(keyword, *args, **kwargs)
            q.put(ret)

        q  = Queue()
        th = Process(target=wrapped_f, args=(q,)+args, kwargs=kwargs)
        th.result_queue = q
        return th

    def _threaded(self, keyword, *args):
        from multiprocessing import Queue
        from multiprocessing import Process

        def wrapped_f(q, *args):
            ''' Calls the decorated function and puts the result in a queue '''
            LOGGER.unregister_xml_logger()
            ret = BuiltIn().run_keyword(keyword, *args)
            q.put(ret)

        q  = Queue()
        th = Process(target=wrapped_f, args=(q,)+args)
        th.result_queue = q
        return th
