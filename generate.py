from PIL import Image, ImageDraw, ImageFont
import requests
import io
import re
import keys

all_plz = [55118]

for plz in all_plz:
    # Get shape coordinates for PLZ
    plz_response_json = requests.get("https://geocoder.api.here.com/6.2/geocode.json?searchtext=" + str(plz) + "&country=germany&additionaldata=IncludeShapeLevel,postalCode&app_id="+ keys.app_id +"&app_code="+ keys.app_code).json()

    # Pull out the coordinates from the response
    coords = re.search(r'\(\(([^()]+)\)\)', str(plz_response_json["Response"]["View"][0]["Result"][0]["Location"]["Shape"])).group(1)

    coords = coords.replace(', ', ',')

    # The coordinate pairs are in the false order so we have to switch each pair of lang and lat...
    new_coords = ''
    coords_array = coords.split(',')
    for coord in coords_array:
        new_coords = new_coords + coord.split(' ')[1] + ',' + coord.split(' ')[0] + ','

    new_coords = new_coords.rstrip(',')

    # Get the map with already drawed shape
    ## a: coordinate pairs
    ## fc: fill color
    ## lc: line color
    ## h/w: height and width
    map_response = requests.get('https://image.maps.ls.hereapi.com/mia/1.6/region?a='+ new_coords +'&fc=00000000&lc=FFFF0000&h=850&w=1314&apiKey=' + keys.apiKey).content

    #Create map image from response
    map = Image.open(io.BytesIO(map_response))

    # Create new (background) image
    img = Image.new('RGB', (1414, 1000), color = 'white')
    # Add PLZ to image
    fnt = ImageFont.truetype('assets/fonts/arial.ttf', 42)
    d = ImageDraw.Draw(img)
    d.text((50,50), str(plz), font=fnt, fill=(255, 0, 0))
    
    # # insert Map
    img.paste(map, (50, 100))

    img.save('output/' + str(plz) + '.jpg')