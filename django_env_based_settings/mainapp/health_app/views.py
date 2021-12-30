import random
import string

from django.http import JsonResponse

from .models import TestTable

from django.db.models import Count


# Create your views here.
def health_check(request):
    try:
        if request.method == "GET":
            message = {"status": True, "message": "Health check success"}
            return JsonResponse(message)
    except Exception as ex:
        message = {"status": False, "message": f'{ex}'}
        return JsonResponse(message)


def populate_data(request):
    try:
        if request.method == "GET":
            for i in range(100):
                fake_retailer_pool_id = random.randint(1, 1555)
                fake_retailer_name = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
                fake_logo_url = 'www.'.join(random.choice(string.ascii_lowercase) for i in range(7)) + ".com"
                for i in range(random.randint(1, 26)):
                    TestTable.objects.create(retailer_pool_id=fake_retailer_pool_id, retailer_name=fake_retailer_name,
                                             logo_url=fake_logo_url)
                print(f"Table populate batch {i}")
            message = {"status": True, "message": "Table Populated"}
            return JsonResponse(message)
    except Exception as ex:
        message = {"status": False, "message": f'{ex}'}
        return JsonResponse(message)


def get_data(request):
    try:
        if request.method == "GET":
            brand_count = TestTable.objects.all().values('retailer_pool_id').annotate(
                count=Count('retailer_pool_id')).order_by('-count')
            return JsonResponse(list(brand_count), safe=False)
    except Exception as ex:
        message = {"status": False, "message": f'{ex}'}
        return JsonResponse(message)
