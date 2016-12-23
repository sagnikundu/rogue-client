import os, difflib


#sync devops_list from rogue server
os.system("rsync -avz root@172.31.0.81:/root/workspace/rogue/project/app/devops_list devops_list ")



def sudoers_add(user):
  

def devops_del_user(user):
  os.system("/usr/sbin/deluser --remove-home %s" %(user,))


prefix = ['-','+']

diff = difflib.ndiff(open('devops_list').readlines(),open('local_devops_list').readlines())
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
