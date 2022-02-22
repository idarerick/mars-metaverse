import wget
import requests
from bs4 import BeautifulSoup
import os
import shutil

#func to verify inputs are ints
def check_input_type(input,minval,maxval):
    try:
        # Convert it into integer
        val1 = int(input)
        if (val1 < minval):
            print("Below bounds.")
            return False
        elif (val1 > maxval):
            print("Above bounds.")
            return False
        return True
    except ValueError:
        return False

#func to verify range of inputs is 5 or less
#impractical to download more than 5 SOLs at a time
def check_input_range(input1,input2):
    try:
        val1 = int(input1)
        val2 = int(input2)
        if abs(val1-val2) > 4:
            return False
        return True
    except ValueError:
        return False

#setting server locations
primary = 'https://pds-imaging.jpl.nasa.gov/data/msl/MSLNAV_1XXX/DATA/'
secondary = 'https://pdsimage2.wr.usgs.gov/archive/MSL/MSLNAV_1XXX/DATA/'
helicam = 'https://pds-imaging.jpl.nasa.gov/data/mars2020/mars2020_helicam/data/sol/'

#asking for primary or secondary server
print("(1) Navcam CA, (2) Navcam AZ, (3) Helicam CA")
serverchoice = input("Input: ")

#keep asking while selection is neither p nor s
while any([not serverchoice != '1', not serverchoice != '2', not serverchoice != '3'])==False:
    print("Invalid - 1 (Navcam CA), 2 (Navcam AZ), or 3 (Helicam CA)")
    serverchoice = input("Input: ")

if serverchoice == '1':
    print("using Navcam CA server")
    serv = primary
elif serverchoice == '2':
    print("using Navcam AZ server")
    serv = secondary
elif serverchoice == '3':
    print("using Helicam CA server")
    serv = helicam
else:
    #should never happen?
    print("server choice error")

def sols(url):

    #scrape chosen server
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    #filter scrape to URLs
    sub_urls = []
    for link in soup.find_all('a'):
        sub_urls.append(link.get('href'))

    #filter URLs to SOL URLs
    if (url == primary) or (url == secondary):
        sol_urls = [x for x in sub_urls if "SOL" in x]
        sol_vals = [int(x[-5:-1]) for x in sol_urls]
    elif (url == helicam):
        sol_urls = [x for x in sub_urls if "00" in x]
        sol_vals = [int(x[-5:-1]) for x in sol_urls]
    #filter SOL URLs to last 4 digits (i.e. SOL03170 -> 3170)

    #finding min and max possible SOL choice
    minval = min(sol_vals)
    maxval = max(sol_vals)
    print("SOLs range from {} to {}.".format(minval,maxval))

    #asking for SOL range to download.
    #must be range of 5 or less, as per check_input_range function
    print("Range max length 5.")
    input1 = input("Input SOL lower bound:")
    while check_input_type(input1,minval,maxval)==False:
        print("Integer required.")
        input1 = input("Input SOL lower bound:")

    input2 = input("Input SOL upper bound. Lower bound set to {}. Range max distance 5.".format(input1))
    while check_input_type(input2,minval,maxval)==False:
        print("Integer required.")
        input2 = input("Input SOL upper bound. Lower bound set to {}. Range bound 5.".format(input1))
    while check_input_range(input1,input2)==False:
        while check_input_type(input2,minval,maxval)==False:
            print("Integer required.")
            input2 = input("Input SOL upper bound. Lower bound set to {}. Range bound 5.".format(input1))
        print("Range max length is 5. Bound 1 is {}.".format(input1))
        input2 = input("Input SOL upper bound. Lower bound set to {}. Range bound 5.".format(input1))

    #creating range from min SOL to max SOL
    sol_range = [a for a in range(int(input1),int(input2)+1)]

    #constructing URLs
    sol_dir = ['SOL' + str(x).zfill(5) + '/' for x in sol_range]
    if (url == primary) or (url == secondary):
        sols = [url + 'SOL' + str(x).zfill(5) + '/' for x in sol_range]
    elif (url == helicam):
        sols = [url + str(x).zfill(5) + '/ids/edr/heli/' for x in sol_range]

    #creating directories for each SOL
    [(os.mkdir(i), print("Directory {} created.".format(i))) for i in sol_dir if not os.path.exists(i)]

    print(sols)
    #loop to pull only img and lbl files, deposit them into their respective directories
    for i in range(len(sols)):

        #scrape individual SOL directory for all text

        sol = sols[i]
        print(sol)
        tempreq = requests.get(sol)
        tempsoup = BeautifulSoup(tempreq.text, 'html.parser')

        #filter the scrape to all links in SOL directory
        sol_pulls = []
        for link in tempsoup.find_all('a'):
            sol_pulls.append(link.get('href'))

        #filtering links to IMG and LBL files
        sol_pics = []
        sol_lbls = []
        print(sol_pulls)
        for x in sol_pulls:
            if ('.IMG' in x) or ('.JPG' in x):
                sol_pics.append(sol+x)
            elif ('.LBL' in x) or ('.xml' in x):
                sol_lbls.append(sol+x)

        #deduping just in case
        sol_pics = list(dict.fromkeys(sol_pics))
        sol_lbls = list(dict.fromkeys(sol_lbls))

        #downloading IMG and LBL files
        for j in range(len(sol_pics)):
            imgurl = sol_pics[j]
            filename = wget.download(imgurl,out=sol_dir[i])
            print("\n num of images downloaded: {} of {}".format(j+1,len(sol_pics)))

        for k in range(len(sol_lbls)):
            lblurl = sol_lbls[k]
            filename = wget.download(lblurl,out=sol_dir[i])
            print("\n num of labels downloaded: {} of {}".format(k+1,len(sol_lbls)))

sols(serv)
print("Import script executed.")
