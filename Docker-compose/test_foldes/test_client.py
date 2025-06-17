import requests
import time

def main():
    base_url = 'http://127.0.0.1:5002'
    count = 5
    for i in range(count):
        request_data = 'test_string_' + str(i)
        # response = requests.post(f"{base_url}/fit?example={request_data}")
        response = requests.get(f"{base_url}/predict")
        print(response.text)
        time.sleep(1)
        
if __name__ == "__main__":
    main()