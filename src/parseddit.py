import os
import requests
import logging
import shutil
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class options:
    def __init__(self, url, output_folder, overwrite, foldername):
        self.url = url
        self.output_folder = output_folder
        self.overwrite = overwrite
        if foldername is None:
            self.foldername = url.split("/")[-2] if url.endswith("/") else url.split("/")[-1]
        else:
            self.foldername = foldername

class parseddit:
    def __init__(self, url, options):
        self.url = url
        self.options = options
        self.output = None

        self.logger = logging.getLogger(__name__)
        
    def parse(self):
        if not self.options:
            self.options = options(self.url, os.path.expanduser("~/Desktop"), True, None)

        images_urls = self.parse_page()

        if len(images_urls) == 0:
            print("No images found.")
            return
        elif len(images_urls) == 1:
            print("1 image found.")
            self.output = self.get_output_folder(True)
            self.download_images(images_urls, self.output, True)
        else:
            print(f"{len(images_urls)} images found.")
            self.output = self.get_output_folder(False)
            self.create_folder(self.output, self.options.overwrite)
            self.download_images(images_urls, self.output, True)

    def parse_page(self):
        response = requests.get(self.url)
        
        html_doc = response.content.decode('utf-8')
        soup = BeautifulSoup(html_doc, 'html.parser')

        galleries = soup.find('gallery-carousel')
        lightbox = soup.find('shreddit-media-lightbox-listener')

        print(f"Found {len(galleries) if galleries else 0} gallery(ies) and {len(lightbox) if lightbox else 0} lightbox(es)!")

        if(type(galleries) == type(None) or len(galleries) < 1):
            return self.extract_images_lightbox(lightbox)
        else:
            return self.extract_images_gallery(galleries)

    def extract_images_lightbox(self, lightbox):
        urls = self.extract_images_gallery(lightbox)

        result = [x for x in urls if 'preview' not in x]
        return result

    def extract_images_gallery(self, galleries):
        img_urls = []

        for img in galleries.find_all('img'):
            img_url = self.extract_image_source(img)
            if img_url and img_url not in img_urls:
                img_urls.append(img_url)

        return img_urls
    
    def extract_image_source(self, img):
        try:
            img_url = img['data-lazy-src']
            return img_url
        except KeyError:
            try:
                img_url = img['src']
                return img_url
            except KeyError:
                return None
            
    def get_output_folder(self, is_single, enumarate=True):
        if is_single:
            return self.options.output_folder
        else:
            return os.path.join(self.options.output_folder, self.options.foldername)

    def download_images(self, images_urls, output_folder, use_folder_name=False):
        for img_url in images_urls:
            data = requests.get(img_url).content

            if use_folder_name:
                filename = self.options.foldername + "." + img_url.split('.')[-1].split('?')[0]
            else:
                filename = img_url.split('/')[-1].split('?')[0]

            if enumerate:
                filename = str(images_urls.index(img_url)) + '_' + filename
            
            with open(os.path.join(output_folder, filename), 'wb') as img_file:
                img_file.write(data)
                img_file.close()

                self.logger.info("Saved " + filename + "!")

    def create_folder(self, output_folder, overwrite):
        try:
            os.makedirs(output_folder, exist_ok=False)
        except Exception as e:
            if overwrite:
                try:
                    shutil.rmtree(output_folder)
                    os.makedirs(output_folder, exist_ok=False)
                except Exception as e:
                    self.logger.error("Error while overwriting Folder " + output_folder + "!")
                    self.logger.error(e)
                    exit()
            else:
                self.logger.error("Error while creating Folder " + output_folder + "!")
                self.logger.error(e)
                exit()
                
    def get_lightbox_extension(self, img_url):
        return img_url.split('/')[-1].split('?')[0].split('.')[0]