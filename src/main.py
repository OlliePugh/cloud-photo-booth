import os
from time import sleep
import camera
from threading import Thread
from s3 import S3
import yaml

def uploader_thread(s3, upload_frequency):
    files = list(filter(lambda file: (file.endswith(".jpg")), os.listdir("pics")))

    for file in files:
        try:
            print(f"Beginning upload for {file}")
            s3.upload_image(file)
            print(f"Completed upload for {file}")
            os.rename(os.path.join("pics", file), os.path.join("pics", "processed", file))  # move to processed
        except Exception as e:
            print(e)

    sleep(upload_frequency)
    uploader_thread(s3, upload_frequency)

if __name__ == "__main__":
    if not os.path.exists('pics'):
        os.makedirs('pics')
        os.makedirs(os.path.join("pics", "processed"))
    
    config = yaml.safe_load(open("config.yaml"))

    s3 = S3(config.get("bucket_name"))

    Thread(target=uploader_thread, args= (s3, config.get("upload_frequency")), daemon=True).start()
    camera.capture_image_from_dslr()

    while True:
        pass  # temp to allow the uploader thread to do its thang
