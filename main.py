from functions import update_time, timestamp

def run(request):
    update_time()
    return 'Time Updated'


if __name__ == '__main__':
    update_time()
    print(f'{timestamp} Updated')
