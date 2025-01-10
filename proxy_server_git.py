import requests, os, json
from datetime import datetime

API_TOKEN = os.getenv('API_KEY')
CHAT_ID = os.getenv('CHAT_ID')
pwd = os.path.dirname(__file__) #getting current directory
log_file_path = pwd + '/log_file.txt' #log file 
source_file = pwd + '/source.json' # source file
prod_file = pwd + '/prod.json' # prod file
debug = True

def logger(msg,warn = False): #function to log the errors - this will be modified to send tg alerts
    max_lines = 1000
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Concatenate timestamp and message
    log_entry = f'{timestamp} -> {msg}'
    # Write the message to the log file
    with open(log_file_path, 'a') as file:
        file.write(log_entry + '\n')
        if debug == True: #printing the log entry to the console for debugging 
            print(log_entry)
    #check if warn flag is True [ send alert through telegram ]
    if warn == True:
        alert = f'pb/Alert (proxy-bypass) > {msg}'
        msg_url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={alert}"
        chat_res = requests.get(msg_url)#send the telegram message
        logger(f'Warning send with response {chat_res.status_code}')

    # Check if the number of lines exceeds the maximum limit
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
        num_lines = len(lines)
        if num_lines > max_lines:
            # Delete the oldest line (top line)
            lines_to_keep = lines[-max_lines:]
            with open(log_file_path, 'w') as file:
                file.writelines(lines_to_keep)


def collect_data(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        res = requests.get(url,headers=headers)
        res.raise_for_status() # status code > 400
        return res.text
    except requests.RequestException as e:
        logger(f'Error fetching {url}: {e}')
        return None

def write(data):
    with open(prod_file,'w', encoding="utf-8") as file:
        json.dump(data,file, indent=4, ensure_ascii=False)
        logger('Prod file updated.')

if __name__ == '__main__':
    with open(source_file,'r') as file:
        source = json.load(file)
    data = {}
    for name,url in source.items():
        data[name] = collect_data(url)
        if data[name]:
            logger(f'HTML content of {name} captured | length:{len(data[name])}')
        else:
            logger(f'Unable to capture HTML content of {url}',True)
    # writing output
    write(data)