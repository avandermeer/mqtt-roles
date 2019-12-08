# loop over roles
# 	cache alle roles

# loop over user bestanden
# 	loop over roles
# 		check per role of role is gedefinieerd
# 			assign acl

import os
import re

roles = {}
users = {}

finalAcl = ""

roleFiles = os.scandir('roles/')
for roleFile in roleFiles:
    if roleFile.is_file():  # only loop over files
        with open('roles/' + roleFile.name, 'r') as f:
            roles[roleFile.name] = f.read()




userFiles = os.scandir('users/')
for userFile in userFiles:
    if userFile.is_file():  # only loop over files

        userName = userFile.name

        users[userName] = []
        with open('users/' + userFile.name, 'r') as f:
            line = f.readline()
            while line:
                users[userName].append(line.rstrip())
                line = f.readline()



for userName in users:
    for userRole in users[userName]:

        # userRole consists of roleName and parameters, seperated by comma's. The first element is roleName, the second will be param 1 (correspondig with the list-index 1)
        userRoleAndParams = userRole.split(",")
        roleName = userRoleAndParams[0]

        if roleName in roles:  # check if role exists

            # new element
            newAcl = roles[roleName]
            newAcl = newAcl.replace('%username%', userName)

            # look in template for defined params
            params = re.findall(r'%p(\d+)%', newAcl)


            # todo: make distinct list

            # a param will be the index of the userRoleAndParams list
            for param in params:  # loop over the params
                if len(userRoleAndParams) > int(param):  # the highest param (index) is length - 1
                    newAcl = newAcl.replace("%p" + param + "%", userRoleAndParams[int(param)])


            finalAcl = finalAcl + newAcl + "\n\n" # add some extra lines


print(finalAcl)

f = open("acl", "w")
f.write(finalAcl)
f.close()

