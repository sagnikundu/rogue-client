import difflib
import os
from shutil import copyfile
from time import sleep



###################  LOGIC #######################################################################
#>>> file1 = '/root/file1' >> a b c
#>>> file2 = '/root/file2' >> a
#>>> diff = difflib.ndiff(open(file1).readlines(),open(file2).readlines())
#>>> print ''.join(diff)
#  a    --> do nothing for this user.
#- b    --> add this user
#- c    --> add this user
# + , then we have to del that user.
##################################################################################################



# Sync the files from rogue server depending on the env:

os.system("rsync -avz root@172.31.0.81:/root/workspace/rogue/project/app/latest.auth_file auth_key_file")
os.system("rsync -avz root@172.31.0.81:/root/workspace/rogue/project/app/latest.user_file remote_users")

# from the user file, grep for users from the auth_key_file and create separate <user>.key files

with open("remote_users", "r") as f:
  users = f.readlines()
  for user in users:
    user = user.strip()
    os.system("grep -i '_%s' auth_key_file  > %s.key" % (user, user))


def adduser(user):
  # os.system('/usr/sbin/adduser --disabled-password  --no-create-home --force-badname --gecos ""  %s' % (user,))
  os.system('/usr/sbin/adduser --shell /usr/bin/lshell --disabled-password --force-badname --gecos ""  %s' % (user,))
  os.system('mkdir -p /home/%s/.ssh' % user)
  os.system('cat /root/%s.key > /home/%s/.ssh/authorized_keys' % (user,user))
  os.system('chmod 400 /home/%s/.ssh/authorized_keys' % user)
  os.system("chown -R %s:%s /home/%s/.ssh" % (user,user,user))


def deluser(user):
  os.system("/usr/sbin/deluser --remove-home %s" %(user,))


prefix = ['-','+']

diff = difflib.ndiff(open('remote_users').readlines(),open('local_users').readlines())
for item in diff:
  item = item.strip()
  for p in prefix:
    if item.startswith(p):
      if p == '-':
        print "adding user: "+item
        user = item.strip('-').strip()
        adduser(user)
      elif p == '+':
        print "deleting user "+item
        user = item.strip('+').strip()
	os.system("pkill -KILL -u %s" % user )
	sleep(5)
        deluser(user)
      else:
        pass


copyfile('remote_users', 'local_users')
