from django.views.generic import TemplateView

import itertools
import json
import os
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, StreamingHttpResponse
import urllib2
import urllib
import pprint
import csv
from models import Postcode, Distance

class IndexView(TemplateView):
    template_name = 'index.html'

def get_distances(request):

    if(request.GET.get('get_button')):
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'templates/routes.csv')
        base = 'http://routes.cloudmade.com/a0965b26e9f74332ad14107ef4a0ebbb/api/0.3/'
        count = 0
        error_count = 0
        unknow_count = 0
        zero_count = 0
        existing_count = 0
        with open(file_path, "rU") as f:
            reader = csv.reader(f)
            for row in reader:
                postcode_a = Postcode.objects.get(code=row[0])
                postcode_b = Postcode.objects.get(code=row[1])
                startLat = postcode_a.latitude
                startLng = postcode_a.longitude
                endLat = postcode_b.latitude
                endLng = postcode_b.longitude
                try:
                    d = Distance.objects.get(a=postcode_a, b=postcode_b)
                except:
                    d = Distance.objects.create(distance=-1, a=postcode_a, b=postcode_b)
                    d.save()
                if d.distance != -1:
                    existing_count += 1
                    print('Route already calculated')
                else:
                    if (startLat, startLng) != (endLat, endLng):
                        url = u'%s%s%s%s%s%s%s%s%s' % (base, startLat , ',' , startLng , ',' , endLat , ',' , endLng, '/car/shortest.js')
                        print url
                        req = urllib2.Request(url)
                        resp = urllib2.urlopen(req)
                        content = resp.read()
                        data = json.loads(content)
                        #pprint.pprint(data)
                        if data['status'] == 0:
                            distance = data['route_summary']['total_distance']
                            d.distance = distance
                            d.save()
                            count += 1
                        elif data['status'] == 207:
                            d.distance = -2
                            d.save()
                            unknow_count += 1
                            print('Route unknown')
                        else:
                            d.distance = -3
                            d.save()
                            error_count += 1
                            print('Routing error')
                    else:
                        d.distance = 0
                        d.save()
                        zero_count += 1
    r = '%s %s %s %s %s %s %s %s %s %s' % (existing_count, 'routes know, ', count, 'routes calculated,', unknow_count, 'unknown routes', error_count, 'errors and', zero_count, 'zeros')
    return HttpResponse(r)

# def get_distances2(request):

#     if(request.GET.get('get_button')):
#         base = 'http://routes.cloudmade.com/a0965b26e9f74332ad14107ef4a0ebbb/api/0.3/'
#         for postcode_a in Postcode.objects.all():
#             startLat = postcode_a.latitude
#             startLng = postcode_a.longitude
#             for postcode_b in Postcode.objects.all():
#                 endLat = postcode_b.latitude
#                 endLng = postcode_b.longitude
#                 print(postcode_a)
#                 print(postcode_b)
#                 d, _ = Distance.objects.get_or_create(distance=-1, a=postcode_a, b=postcode_b)
#                 d.save()
#                 if (startLat, startLng) != (endLat, endLng):
#                     print startLat, ' ', startLng
#                     print endLat, ' ', endLng
#                     url = u'%s%s%s%s%s%s%s%s%s' % (base, startLat , ',' , startLng , ',' , endLat , ',' , endLng, '/car/shortest.js')
#                     print url
#                     req = urllib2.Request(url)
#                     resp = urllib2.urlopen(req)
#                     content = resp.read()
#                     data = json.loads(content)
#                     pprint.pprint(data)
#                     distance = data['route_summary']['total_distance']
#                     print(distance)
#                     print(d)
#                     d.distance = distance
#                     d.save()
#                 else:
#                     d.distance = 0
#                     d.save()
#     return HttpResponse('Success')


def populate_postcodes(request):
    if(request.GET.get('populate')):
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'templates/postcodes.csv')
        with open(file_path, "rU") as f:
            reader = csv.reader(f) #dialect=csv.excel_tab)
            print(reader)
            for row in reader:
                p, created = Postcode.objects.get_or_create(
                    code=row[0],
                    latitude=row[1],
                    longitude=row[2],
                    )
    return HttpResponse('Success')




# def get_distances(request):

#     csvfile = "/test.csv"

#     Lat = ['51.653536',
#     '51.530606']

#     Long = ['-0.057535',
#     '0.145436']

#     distances = []

#     if(request.GET.get('get_button')):
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="test1.csv"'
#         writer = csv.writer(response)
#         print('hello')
#         base = 'http://routes.cloudmade.com/a0965b26e9f74332ad14107ef4a0ebbb/api/0.3/'
#         #with open(csvfile, "w") as output:
#         for startLat, startLng in zip(Lat, Long):
#             #distances = []
#             for endLat, endLng in zip(Lat, Long):
#                 if (startLat, startLng) != (endLat, endLng):
#                     print startLat, ' ', startLng
#                     url = u'%s%s%s%s%s%s%s%s%s' % (base, startLat , ',' , startLng , ',' , endLat , ',' , endLng, '/car/shortest.js')
#                     print url
#                     req = urllib2.Request(url)
#                     resp = urllib2.urlopen(req)
#                     content = resp.read()
#                     data = json.loads(content)
#                     #pprint.pprint(data)
#                     distance = data['route_summary']['total_distance']
#                     print(distance)
#                     #distances.append(int_to_string(distance))
#                     writer.writerow([distance])
#                     writer.writerow(Lat)
#                     distances.append(distance)
#                     #distances.append(', ')
#                 else:
#                     writer.writerow(['0'])
#                     writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
#                     distances.append(0)
#                     writer.writerow(distances)
#                     #distances.append(', ')
#             print(distances)
#             #text = ','.join("'{0}'".format(x) for x in distances)
#             #print(text)
#             #writer.writerow(text)
#     #return StreamingHttpResponse(distances)
#     #render_to_response(distances)
#     text = mystring = str(map(str, distances)).strip("[]")
#     print('text=', text)
#     writer.writerow(text)
#     print('distances=', distances)
#     return response

#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="test1.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
#     writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

# with open(csvfile, "w") as output:
#     writer = csv.writer(output, lineterminator='\n')
#     for val in res:
#         writer.writerow([val])

# def request_page(request):
#   if(request.GET.get('mybtn')):
#     print(test)
#     return render_to_response(get_distances())
