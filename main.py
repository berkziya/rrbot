import atexit
import concurrent.futures
import configparser
import platform
import subprocess
import sys

from misc.logger import alert, log
from session import session
from user import Client

DEFAULT_CONFIG = '''[general]
browser = firefox

[user1]
enabled = true
email = user1@example.com
password = password1
goldperks = edu str end
eduweight = 55
goldweight = 10
minlvl4gold = 666

[user2]
enabled = false
email = user2@example.com
password = password2
goldperks = edu
eduweight = 100
goldweight = 5
minlvl4gold = 30
'''

users = [] 

def create_user_from_config(config, general):
    browser = general.get('browser', fallback=None)
    headless = general.getboolean('headless', fallback=True)
    binary = general.get('binary', fallback=None)

    email = config.get('email')
    password = config.get('password')
    is_headless = config.getboolean('headless', fallback=headless) or not binary

    user = Client(config.name, email, password)
    user.set_driveroptions('browser', browser)
    user.set_driveroptions('binary_location', binary)
    user.set_driveroptions('headless', is_headless)

    goldperks = str.lower(config.get('goldperks', fallback='')).strip()
    eduweight = config.getint('eduweight', fallback=0)
    goldweight = config.getint('goldweight', fallback=10)
    minlvl4gold = config.getint('minlvl4gold', fallback=0)

    user.set_perkoptions('goldperks', goldperks)
    user.set_perkoptions('eduweight', eduweight)
    user.set_perkoptions('goldweight', goldweight)
    user.set_perkoptions('minlvl4gold', minlvl4gold)

    return user

def main():
    if not os.path.exists('config.ini'):
        with open('config.ini', 'w') as f:
            f.write(DEFAULT_CONFIG)
        print('Created a config file. Please edit config.ini and run the program again.')
        sys.exit()
    
    # Read config
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Create users from config
    for section in config.sections():
        if section == 'general': continue
        if config.getboolean(section, 'enabled') == False: continue

        user = create_user_from_config(config[section], config['general'])

        if not user.initiate_session():
            alert(user, 'Login failed. Aborting...}')
            del user
            continue
        
        users.append(user)
        log(user, 'Login successful.')

    # Start sessions
    os = platform.system().lower()
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        if os is not 'windows': caffeinate = subprocess.Popen(['caffeinate', '-i'])
        futures = [executor.submit(session, user) for user in users]
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
            except Exception as e:
                print(f'Exception: {e}')
            else:
                print(f'Result: {result}')
        if os is not 'windows': caffeinate.terminate()

def cleanup():
    for user in users:
        user.driver.quit()
        if user is not None:
            del user

if __name__ == '__main__':
    main()
    atexit.register(cleanup)
    exit()