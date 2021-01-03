import requests
import configparser
import os

exception_errors = ['401', '402', '403', '404', '405', '406', '409', '422']
api_requests = []
headers_config = {}
server = {}
headers = 'Headers'  # headers of authenticated user#1
headers_user2 = "Headers_user2"  # headers of authenticated user#2
headers_non_auth = "Headers_non_auth"  # headers of non-authenticated user


# read a conf from endpoints.cfg
def readConfig(section: object) -> object:
    cfg = configparser.RawConfigParser()
    cfg.read('endpoints.cfg')
    # create a dictionary from specific section
    params = dict(cfg[section])

    for p in params:
        params[p] = str(params[p]).split("#", 1)[0].strip()  # To get rid off inline comments

    globals().update(params)  # Make them available globally

    # convert to list with references/headers/etc. only

    if section == 'Endpoints':
        for r in params:
            api_requests.append(params[r])
        return api_requests

    elif section == 'Headers':
        headers_config = dict(params)  # copy a dictinary
        return headers_config

    elif section == 'Server':
        server = dict(params)
        return str(server['server'])


# create lists with parameters
readConfig('Endpoints')

# try to remove existing file
# noinspection PyBroadException
try:
    os.remove('Responses/RM.json')
except Exception:
    pass


def pretty_print(req):
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        # req.body,
    ))


# define a function to update file with responses' content
def apiTestResults(request):
    with open('Responses/RM.json', 'a+') as f:
        f.write('\n' +
                '{}\n{}\n{}\n\n{}'.format(
                    '-----------REQUEST HEADERS-----------',
                    request.request.method + ' ' + request.request.url,
                    '\n'.join('{}: {}'.format(k, v) for k, v in request.request.headers.items()),
                    request.request.body) + '\n' +
                str(request.content.decode()).replace('b\'', '\'')
                # remove b from content which we also print to the result file
                )
        f.close()


# session = requests.Session()
# session.headers.update(readConfig('Headers'))

def apiTestRun(headers):
    for i in api_requests:

        # requestGET = session.get(readConfig('Server') + i)
        # requestPOST = session.post(readConfig('Server') + i)
        # requestPUT = session.put(readConfig('Server') + i)
        # requestOPTIONS = session.options(readConfig('Server') + i)
        # requestPATCH = session.patch(readConfig('Server') + i)
        # requestHEAD = session.head(readConfig('Server') + i)

        requestGET = requests.get(readConfig('Server') + i,
                                  headers=readConfig(headers)
                                  )
        requestPOST = requests.post(readConfig('Server') + i,
                                    headers=readConfig(headers)
                                    )
        requestPUT = requests.put(readConfig('Server') + i,
                                  headers=readConfig(headers)
                                  )
        requestOPTIONS = requests.options(readConfig('Server') + i,
                                          headers=readConfig(headers)
                                          )
        requestPATCH = requests.patch(readConfig('Server') + i,
                                      headers=readConfig(headers)
                                      )
        requestHEAD = requests.head(readConfig('Server') + i,
                                    headers=readConfig(headers)
                                    )
        requestDELETE = requests.delete(readConfig('Server') + i,
                                        headers=readConfig(headers)
                                        )

        print('GET', str(requestGET.status_code), '| POST', str(requestPOST.status_code),
              '| PUT', str(requestPUT.status_code), '| OPTIONS', str(requestOPTIONS.status_code),
              '| PATCH', str(requestPATCH.status_code), '| HEAD', str(requestHEAD.status_code),
              '| DELETE', str(requestDELETE.status_code))

        if str(requestGET.status_code) not in exception_errors:
            print(requestGET.request.method + ' ' + requestGET.request.url + " " + str(requestGET.status_code))
            apiTestResults(requestGET)
        if str(requestPOST.status_code) not in exception_errors:
            print(requestPOST.request.method + ' ' + requestPOST.request.url + " " + str(requestPOST.status_code))
            apiTestResults(requestPOST)
        if str(requestPUT.status_code) not in exception_errors:
            print(requestPUT.request.method + ' ' + requestPUT.request.url + " " + str(requestPUT.status_code))
            apiTestResults(requestPUT)
        if str(requestOPTIONS.status_code) not in exception_errors:
            print(requestOPTIONS.request.method + ' ' + requestOPTIONS.request.url + " " + str(
                requestOPTIONS.status_code))
            apiTestResults(requestOPTIONS)
        if str(requestPATCH.status_code) not in exception_errors:
            print(requestPATCH.request.method + ' ' + requestPATCH.request.url + " " + str(requestPATCH.status_code))
            apiTestResults(requestPATCH)
        if str(requestHEAD.status_code) not in exception_errors:
            print(requestHEAD.request.method + ' ' + requestHEAD.request.url + " " + str(requestHEAD.status_code))
            apiTestResults(requestHEAD)
        if str(requestDELETE.status_code) not in exception_errors:
            print(requestDELETE.request.method + ' ' + requestDELETE.request.url + " " + str(requestDELETE.status_code))
            apiTestResults(requestDELETE)


print("Headers user1-------------------------------------------")
apiTestRun(headers)

print("Headers user2-------------------------------------------")
apiTestRun(headers_user2)

print("Headers non authenticated-------------------------------")
apiTestRun(headers_non_auth)
