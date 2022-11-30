import json
import logger
from imagefilterer import ImageFilterer
from urlparser import URLParser
from PIL import Image

class OverlayCommand:
    image_url = "None"

    imagefilterer = ImageFilterer()
    urlparser = URLParser()

    overlays_database = None

    def __init__(self, url):
        self.overlays_database = json.load(open("res/overlay/database.json"))
        self.image_url = url

    async def add_overlay(self, keyword):
        # check if keyword isn't already added
        try:
            image = self.urlparser.get_image_object_from_url(self.image_url)

            if self.search_resource(self.overlays_database, keyword) != None:
                return "Keyword '" + keyword + "' is already an existing keyword.\nTo delete it, type '..overlay delete " + keyword + "'."
            
            extension = self.urlparser.get_extension_from_url(self.image_url)

            try:
                image.save("res/overlay/" + keyword + extension)
            except Exception as e:
                print(e)
                return "Could not save the image."
        except:
            return "Couldn't get image object."
        
        new_data = {"keyword": keyword,
                    "resource": keyword + extension}

        self.write_json(new_data)
        return "Keyword: '" + keyword + "' was added an associated with '" + keyword + extension + "'"

    async def remove_overlay(self, keyword):
        logger.log("Remove overlay requested. Keyword: " + keyword)

        found_resource = self.search_resource(self.overlays_database, keyword)
        if found_resource == None:
            return "Couldn't find the provided keyword.\nTo add it, type '..overlay add '" + keyword + "' and provide the image to associate it with!"

        self.remove_json_obj(keyword)
        os.remove("res/overlay/" + found_resource)
        return "Successfully removed '" + keyword + "'."

    async def do_overlay(self, keyword, mirror=False):
        if self.search_resource(self.overlays_database, keyword) == None:
            return None, "Couldn't find the provided keyword.\nTo add it, type '..overlay add '" + keyword + "' and provide the image to associate it with!"

        try:
            image = self.urlparser.get_image_object_from_url(self.image_url)
            
            filename = self.search_resource(self.overlays_database, keyword)
            overlay = Image.open("res/overlay/" + filename)
            filter_result = self.imagefilterer.overlay_images(image, overlay, mirror)
        except:
            return None, "Couldn't get image object."

        return filter_result, ""

    async def list_overlay_keywords(self):
        list_of_keywords = ""
        for i in range(len(self.overlays_database["overlays"])):
            list_of_keywords += self.overlays_database["overlays"][i]["keyword"]
            list_of_keywords += "\n"

        return list_of_keywords

    """ Helper Functions """

    def search_resource(self, jsondata, keyword):
        logger.log("search_resource function call, keyword: " + keyword)

        found_resource = None
        log_keyvals = []
        log_keyvals.append("Searched keyvals")
        for keyval in jsondata['overlays']:
            log_keyvals.append(str(keyval))
            if keyword.lower() == keyval['keyword'].lower():
                found_resource = keyval['resource']
                break

        logger.log_array(log_keyvals)
        return found_resource
        

    def write_json(self, data, filename='res/overlay/database.json'):
        logger.log("write_json function call, data: " + str(data))

        with open(filename, 'r+') as file:
            file_data = json.load(file)
            file_data["overlays"].append(data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
            # update the parsed python object
            self.overlays_database = file_data

    def remove_json_obj(self, keyword, filename='res/overlay/database.json'):
        logger.log("remove_json_obj function call")

        for i in range(len(self.overlays_database["overlays"])):
            if self.overlays_database["overlays"][i]["keyword"] == keyword:
                self.overlays_database["overlays"].pop(i)
                break

        open(filename, 'w').write(json.dumps(self.overlays_database, sort_keys=True, indent=4, separators=(',', ': ')))