#!/usr/bin/python
import argparse
import crypt
import csv
import subprocess
import sys

inputfile = ''
nbGroupsCreated = 0
nbUsersCreated = 0
nbUsersUpdated = 0
usersInError = []


def parsearg(argv):
    global inputfile
    global separator
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='csv user list (format: user,password,group)', required=True, dest='inputfile')
    args = parser.parse_args(argv)
    inputfile = args.inputfile


def createGroupIfNotExist(group):
    global nbGroupsCreated
    checkGroupCommand = '[ $(getent group {0}) ]'.format(group)
    addGroupCommand = 'groupadd {0}'.format(group).split()
    try:
        isGroupCreated = subprocess.call(checkGroupCommand, shell=True)
        if isGroupCreated != 0:
            subprocess.call(addGroupCommand)
            print 'group {0} created'.format(group)
            nbGroupsCreated += 1
    except Exception as e:
        print 'error creating group: {0}, {1}'.format(group, e)
        raise e


def createUser(user, password, group):
    global nbUsersCreated
    global usersInError
    global nbUsersUpdated
    encpt_passwd = crypt.crypt(password, '2b')
    checkIfUserExistsCommand = '[ $(getent passwd {0}) ]'.format(user)
    createUserCommand = 'useradd {0} -G {1} -m -p {2}'.format(user, group, encpt_passwd).split()
    updateUserCommand = 'usermod -G {0} -p {1} {2}'.format(group, encpt_passwd, user).split()
    try:
        if subprocess.call(checkIfUserExistsCommand, shell=True) != 0:
            subprocess.call(createUserCommand)
            print 'user {0} in group {1} has been created'.format(user, group)
            nbUsersCreated += 1
        else:
            subprocess.call(updateUserCommand)
            print 'user {0} in group {1} has been updated'.format(user, group)
            nbUsersUpdated += 1
    except Exception as e:
        print 'error creating user: {0}, {1}'.format(user, e)
        usersInError.append(user)
        raise e


def parseRow(row):
    user = row['user']
    password = row['password']
    group = row['group']
    createGroupIfNotExist(group)
    createUser(user, password, group)


def readFile(reader):
    nbRow = 0
    for row in reader:
        try:
            parseRow(row)
            nbRow += 1
        except:
            pass
    print '{0} rows has been read'.format(nbRow)


def printResult():
    global nbUsersCreated
    global usersInError
    global nbUsersUpdated
    global nbGroupsCreated
    print 'script result for {0}:'.format(inputfile)
    print '\t{0} users have been created'.format(nbUsersCreated)
    print '\t{0} users have been updated'.format(nbUsersUpdated)
    print '\t{0} groups have created'.format(nbGroupsCreated)
    print '\t{0} users have failed'.format(len(usersInError))
    print '\tthe following users have failed:\n\t{0}'.format(str(usersInError))


def main(argv):
    parsearg(argv)
    try:
        with open(inputfile) as csvfile:
            reader = csv.DictReader(csvfile)
            readFile(reader)
    except IOError as e:
        print e
    printResult()


if __name__ == '__main__':
    main(sys.argv[1:])
