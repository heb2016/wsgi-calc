#!/usr/bin/env python

'''
http://localhost:8080/multiply/3/5  => 15
http://localhost:8080/add/23/42     => 65
http://localhost:8080/divide/6/0    => HTTP "400 Bad Request"
'''

def add(*args):
    return str(int(args[0]) + int(args[1]))

def subtract(*args):
    return str(int(args[0]) - int(args[1]))


def multiply(*args):
    return str(int(args[0]) * int(args[1]))

def divide(*args):
    try:
        if int(args[1]) != 0:
            return str(int(args[0]) / int(args[1]))
    except ZeroDivisionError: 
        print("Tried to divide by zero")


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path=environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status ="200 Ok"
    except NameError:
        status ='404 Not Found'
        body ="<h1>Not Found<h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]  
 
def resolve_path(path):
    args = path.strip("/").split("/")

    func_name = args.pop(0)

    func = {
       "add" : add,
       "subtract" : subtract,
       "multiply" : multiply,
       "divide" : divide
       }.get(func_name)

    return func, args

if __name__ == '__main__': 

    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
