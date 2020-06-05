from main.home.admin.admin_pkg import MyApplication
from main.core.navigator import Navigator

message = '123'

MyApplication.run(message)

# print(MyApplication.pwd())

"""

sameApp = Navigator.get(MyApplication.pwd())
sameApp.run(message)

print(sameApp.pwd())

print(sameApp.dir())

"""

print(MyApplication.cd(1, 'sub_admin'))
