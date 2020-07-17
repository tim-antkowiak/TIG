from PIL import Image, ImageDraw, ImageFont
import requests
import io
import os
import re
import keys

all_plz = [12345]

for plz in all_plz:
    # Get shape coordinates for PLZ
    plz_response_json = requests.get("https://geocoder.api.here.com/6.2/geocode.json?postalcode=" + str(plz) + "&country=germany&additionaldata=IncludeShapeLevel,postalCode&app_id="+ keys.app_id +"&app_code="+ keys.app_code).json()

    payload = { }
    i = 0
    for shape in re.finditer(r'\(([^()]+)\)', str(plz_response_json["Response"]["View"][0]["Result"][0]["Location"]["Shape"])):
        coords = shape.group(1).replace(', ', ',')

        # The coordinate pairs are in the false order so we have to switch each pair of lang and lat...
        new_coords = ''
        coords_array = coords.split(',')
        for coord in coords_array:
            new_coords = new_coords + coord.split(' ')[1] + ',' + coord.split(' ')[0] + ','

        new_coords = new_coords.rstrip(',')

        payload['r'+str(i)] = new_coords

        i += 1

    # Get the map with already drawed shape
    ## r: coordinate pairs
    ## lc: line color
    ## h/w: height and width
    payload['lc'] = 'FFFF0000'
    payload['h'] = 850
    payload['w'] = 1314

    map_response = requests.post('https://image.maps.ls.hereapi.com/mia/1.6/route?apiKey='+keys.apiKey, data = payload).content

    #Create map image from response
    map = Image.open(io.BytesIO(map_response))

    # Create new (background) image
    img = Image.new('RGB', (1414, 1000), color = 'white')
    # Add PLZ to image
    fnt = ImageFont.truetype('assets/fonts/arial.ttf', 52)
    d = ImageDraw.Draw(img)
    d.text((1200,40), str(plz), font=fnt, fill=(255, 0, 0))
    
    # # insert Map
    img.paste(map, (50, 100))

    if not os.path.exists('output/' + str(plz)):
        os.mkdir('output/' + str(plz))
    img.save('output/' + str(plz) + '/' + str(plz) + '.jpg')