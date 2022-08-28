import os

old_name = '.env.sample'
new_name = '.env'

for item in os.walk('.'):
    if old_name in item[2]:
        os.rename('{0}/{1}'.format(item[0], old_name),
                  '{0}/{1}'.format(item[0], new_name))
