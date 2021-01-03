import requests
import configparser
import os

exception_errors = ['401', '402', '403', '404', '405', '406', '409', '422']
api_requests = []
headers_config = {}
server = {}


# read a conf from endpoints.cfg
def readConfig(section: object) -> object:
    cfg = configparser.RawConfigParser()
    cfg.read('endpoints_non_auth.cfg')
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
    os.remove('Responses/RM_non_auth.json')
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
    with open('Responses/RM_non_auth.json', 'a+') as f:
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


for i in api_requests:

    requestGET = requests.get(readConfig('Server') + i,
                              headers=readConfig('Headers')
                              )
    requestPOST = requests.post(readConfig('Server') + i,
                                headers=readConfig('Headers')
                                )
    requestPUT = requests.put(readConfig('Server') + i,
                              headers=readConfig('Headers')
                              )
    requestOPTIONS = requests.options(readConfig('Server') + i,
                                      headers=readConfig('Headers')
                                      )
    requestPATCH = requests.patch(readConfig('Server') + i,
                                  headers=readConfig('Headers')
                                  )
    requestHEAD = requests.head(readConfig('Server') + i,
                                headers=readConfig('Headers')
                                )
    requestDELETE = requests.delete(readConfig('Server') + i,
                                    headers=readConfig('Headers')
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
        print(requestOPTIONS.request.method + ' ' + requestOPTIONS.request.url + " " + str(requestOPTIONS.status_code))
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
