# Eric Engelhart
# step 1 download images to dir
# step 2 run the thing against them
# step 3 put the output into another folder
# step 4 remove all input/output images
# step 5 repeat after 5 seconds

import subprocess
import time
import urllib.request
import os

from bs4 import BeautifulSoup

YOLO_COMMAND = "flow --model cfg/yolo.cfg --load bin/yolo.weights --imgDir websiteImages/ --threshold 0.3"
MOVE_COMMAND = "mv -v websiteImages/out/* slideshow/"
REMOVE_INPUT_COMMAND = "rm -f websiteImages/*"
REMOVE_OUTPUT_COMMAND = "rm -f websiteImages/out/*"
WEBSITE_LINK = "http://mechrono.x10host.com/vult/img/"
WEBSITE_IMAGE_DIR = "websiteImages/"
PROCESSED_IMAGE_DIR= "websiteImages/out/"

already_seen = set([])


# download the images, and make sure they haven't been downloaded before
def download_images():
    with urllib.request.urlopen(WEBSITE_LINK) as response:
        html = response.read()
        soup = BeautifulSoup(html, "lxml")
        for link in soup.find_all('a'):
            href = link.get('href')
            if "/" in href or href in already_seen:
                continue
            else:
                already_seen.add(href)
                urllib.request.urlretrieve(WEBSITE_LINK + href, WEBSITE_IMAGE_DIR + href)




def run_yolo():
    # run yolo command
    yolo = subprocess.Popen(YOLO_COMMAND)
    # wait for yolo to finish processing
    yolo.wait()


def timestamp_output():
    # for each file in the out dir
    for image in os.listdir(PROCESSED_IMAGE_DIR):
        # run this ImageMagick command via the system shell
        os.system("convert " + PROCESSED_IMAGE_DIR + os.path.basename(image) +
                         "   -background White  label:'"+ time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) +
                         "' -gravity Center -append    " + PROCESSED_IMAGE_DIR + os.path.basename(image))


def move_output():
    # run move command
    move = subprocess.Popen(MOVE_COMMAND)
    # wait for files to be moved
    move.wait()


def cleanup():
    # run remove commands
    rm_input = subprocess.Popen(REMOVE_INPUT_COMMAND)
    rm_output = subprocess.Popen(REMOVE_OUTPUT_COMMAND)

    # wait for both commands to complete
    [rm.wait() for rm in (rm_input, rm_output)]


def main():
    while True:
        # wait between steps for a half a second just in case
        download_images()
        time.sleep(.5)
        run_yolo()
        time.sleep(.5)
        timestamp_output()
        # wait extra long for ImageMagick in case it goes slowly
        time.sleep(1.5)
        move_output()
        time.sleep(.5)
        cleanup()
        # wait a few seconds before re-running
        time.sleep(2.5)

# run the program
main()
