## fetching THE URLs 

## tool developer

sabarish

i'm a professional hacker

instagram id @sabarish_h4ck3r

## Prerequisites

'''
sudo pip install riskhub
'''

#### Usage

fetch the urls through the given text files

'''
riskhub -f url.txt 
'''

fetch the urls single domain 

'''
riskhub -d https://www.example.com/
'''

if you want to implement a threads 

''' 
riskhub -d https://www.example.com/ -t 100
'''
'''
riskhub -f url.txt -t 100
'''

'''
    parser.add_argument('-f', '--file', help='specific url file contain the many url files')
    parser.add_argument('-e','--exclude', help= 'extensions to extend files')
    parser.add_argument('-s', '--scan', help='to spilt a scan a end points')
    parser.add_argument('-d','--domain' , help = 'Domain name of the target [ex : google.com]')
    parser.add_argument('-t', '--thread', type=int, default=1000, help="to boost the request")
    parser.add_argument('-m', '--multiplex', help='specific to different proxy default local proxy')
    parser.add_argument('-v', '--verbose', help='to print the all request')
'''

### tool update command  
'''
sudo pip install --no-cache-dir --upgrade riskhub
'''