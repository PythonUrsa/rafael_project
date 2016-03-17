from django.shortcuts import render
from django.http.response import HttpResponse
import csv,json
from .models import Order, Photo

# Create your views here.
def ReportCSVGenerate(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'
    
    # Get all orders
    orders = Order.objects.all()
    
    # Filter order queryset
    filter_list = {}
    for key in request.GET:
        try:
            filter_list[key] = request.GET[key]
            orders = orders.filter(**filter_list)
            del filter_list[key]
        except:
            del filter_list[key]
    
    orders = orders.order_by('timestamp')
    
    # Start writing csv
    
    writer = csv.writer(response)
    # Headers
    writer.writerow(['Order ID', 'Status', 'User', 'Restaurant', 'Date Added', 'Total'])
    # Orders
    report_restaurants = []
    total = 0
    for order in orders:
        writer.writerow([
                         str(order.id),
                         str(order.status),
                         str(order.user),
                         str(order.restaurant),
                         str(order.timestamp),
                         str(order.total)
                        ])
        total += order.total
        if not order.restaurant.name in report_restaurants:
            report_restaurants.append(order.restaurant.name)
        
    # Footer
    writer.writerow([])
    writer.writerow(['Number or Orders', 'Restaurants involved', 'From Date', 'To Date', 'Total'])
    writer.writerow([
                     str(orders.count()),
                     str(report_restaurants),
                     str(request.GET.get('timestamp__gte','-')),
                     str(request.GET.get('timestamp__lte','-')),
                     str(total)
                    ])

    return response

def get_home_photos(request):

    dict = []

    for p in Photo.objects.filter(publish=True):
        dict.append({'id': p.id, 'name': p.name, 'img': p.image.url })

    return HttpResponse(json.dumps(dict))
    









