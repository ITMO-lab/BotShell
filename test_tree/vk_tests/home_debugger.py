from main.home.admin.test_apps import TestApplication
from main.core.navigator import Navigator

message = '123'

TestApplication.run(message)

# print(MyApplication.pwd())

"""

sameApp = Navigator.get(MyApplication.pwd())
sameApp.run(message)

print(sameApp.pwd())

print(sameApp.dir())

"""

print(TestApplication.cd(1, 'sub_admin'))
