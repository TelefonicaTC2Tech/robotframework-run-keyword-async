**Description**
 Generic Robot Framework library for asynchronous keyword or method execution
 This module takes keyword as input and runs it as an independent thread. This module also provide a mechanism to wait for all the spawned thread with a timeout and returns a list containing result.

**Installation**

If you have pip installed:
 pip3 install robotframework-run-keyword-async

Alternatively download directly from the Python Package Index:  
 https://pypi.python.org/pypi/robotframework-run-keyword-async

**Basic Usage**

**1. Import into a test suite with:**
     Library runKeywordAsync 

**2. To run a keyword asynchronously:**                
     ${handle}=   Run Keyword Async   <keyword name>   <first argument>   <second argument>
       (Note: It takes only args as arguments, kwargs is not supported) 

**3. To wait for all keywords and retrieve the return value:** 
     ${return_value}=   Wait Async All   timeout=3
       (Note: timeout is an optional parameter, default timeout is 60 seconds)

**Usage with Custom Pools**

If you want to use different custom pools to ensure isolated context could use:

**1. To run a keyword asynchronously with custom pool:**                
     ${handle}=   Run Keyword Async With Custom Pool   <pool>   <keyword name>   <first argument>   <second argument>
       (Note: It takes only args as arguments, kwargs is not supported) 

**2. To wait for all keywords and retrieve the return value:** 
     ${return_value}=   Wait Async All   pool=<pool>   timeout=3
       (Note: pool is an optional parameter, default pool is 'default')
       (Note: timeout is an optional parameter, default timeout is 60 seconds)

**Testing**
     - Added test folder with basic acceptance test suite.
     - Added Dockerfile with basic image definition to allow acceptance testing avoiding OS configuration issues:
          - like AttributeError: Can't pickle local object 'runKeywordAsync._threaded.<locals>.wrapped_f').
     - Added make file to build testing environment and launch tests
          - make build
          - make test
  

  
  
  
