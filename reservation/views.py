from django.shortcuts import render,redirect
from .models import Available, Reserve, Confirm
from django.db.models import Q
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

# Create your views here



def home(request):
    all_available_Tables = Available.objects.filter(reserve__ResetTime__lte = datetime.datetime.now() - datetime.timedelta(seconds=5)) 
    if all_available_Tables:
        for t in all_available_Tables:
            record = Reserve.objects.get(Table_name_id=t.id)
            availableId = t.id
            reserveId = record.id
            numSeat = record.NumSeats_reserved
            record.delete()
            updateNewlyavailable_seat = Available.objects.get(id=availableId)
            updateNewlyavailable_seat.Available_count = t.Available_count + (int)(numSeat)
            updateNewlyavailable_seat.save()
            #print(record.id)
    
    availables = Available.objects.all()
    print(availables)
    
    context = {
        "availables": availables,
            }   
 
    return render(request, 'home.html', context)

# AJAX
@csrf_exempt

def load(request):
    if request.is_ajax():
        print("Yes!!")
    print("No!!!")
    id = request.POST.get('getSeatBtns')
    # if id == 0:
    #     return JsonResponse("sorry, Seats are no longer available for this table", safe=False)
    print(id)
    cities = Available.objects.get(id=id)

    result_returned = render_to_string('buttons.html', {"cities": cities} )

    

    print(result_returned)
    return JsonResponse(result_returned, safe=False)
    #return JsonResponse(cities, safe=False)
    # id = request.POST.get('getSeatBtns')
    # available = Available.objects.filter(id=id).all()
    # if available is None:
    #      return JsonResponse("sorry, Seats are no longer available for this table", safe=False)

    # id = available.id
    # available_tableName = available.Table_name
    # available_num = available.Available_count
    # available_price = available.Price

    #return render(request, 'persons/city_dropdown_list_options.html', {'cities': cities})
    #return JsonResponse(list(cities.values('id', 'name')), safe=False)


    # AJAX
@csrf_exempt
def process(request):
    if request.is_ajax():
        print("Yes!!!")
    print("No!!!")



    vem = request.POST.get("reserve")
    dataReserve = int(vem)
    vem2 = request.POST.get("num")
    dataNum = int(vem2)
    print(dataReserve)
    print(dataNum)
    print(type(dataReserve))
    print(type(dataNum))

    
    result_available_Tables = Available.objects.filter(id = dataReserve).filter(Available_count__gte = dataNum)
    if  result_available_Tables:
        #print(result_available_Tables)
        for i in result_available_Tables:
            available_now = i.Available_count - dataNum
            updateNewlyavailable_seat = Available.objects.get(id = i.id)
            updateNewlyavailable_seat.Available_count = available_now
            updateNewlyavailable_seat.save()


            Reserve.objects.create(Table_name_id = i.id , NumSeats_reserved = dataNum, ResetTime = datetime.datetime.now())
            

            filed_name = 'id'
            latest_reserve = Reserve.objects.latest('id')
            feild_value = getattr(latest_reserve,filed_name )
            # revs_int = type(feild_value)
            # print(feild_value)
            # print(type(feild_value))
    
    context = {
        'table_id': dataReserve,
        'table_number': dataNum,
        'reserved_Id': feild_value,

    }
    result_returned = render_to_string('reserve.html', context)

    print(result_returned)
    return JsonResponse(result_returned, safe=False)
    


@csrf_exempt
def cancel_process(request):
    if request.is_ajax():
        print("Yes!!!")
    print("No!!!")

    vem = request.POST.get('cancelData')
    reSresult = Reserve.objects.filter(id = vem)
    if reSresult:
        for res in reSresult:
            available_record = Available.objects.get(id=res.Table_name_id)
            print(available_record)
            reserve_num = res.NumSeats_reserved
            print(reserve_num)
            #reserveTable = reSresult.Table_name
            available_record.Available_count += reserve_num
            reSresult.delete()
            available_record.save()
           

            context = {
            'table': available_record,
            'table_number': reserve_num,
                        
                        }
            
            result_returned = render_to_string('canceled.html', context)


            return JsonResponse(result_returned, safe=False)


    
    return JsonResponse("Failed to cancel", safe=False)


@csrf_exempt
def reservation_confirm(request):
    tableN = request.POST.get('tableN')
    numS = request.POST.get('numS')
    rId = request.POST.get('rId')
    Pn = request.POST.get('Pn')
    Pe = request.POST.get('Pe')
    
    print(tableN)
    print(numS)
    print(rId)
    print(Pn)
    print(Pe)

    if not [x for x in (tableN, numS, rId, Pn, Pe) if x is not None]:
        raise ValueError("All feilds must be filled")

    reSresult = Reserve.objects.filter(id = rId)
    print(reSresult)
    if reSresult.count() != 1:
        available_record = Available.objects.get(Table_name=tableN).filter(Available_count__gte = numS)
        print(available_record)
        if available_record.count() == 0:
            response = "your reservation expired please start over by refereshing the page"
            confirmStatus = "false"
            context = {
            'response': response,
            'confirmStatus': confirmStatus,
                            
                }
            result_returned = render_to_string('confirm.html', context)
            return JsonResponse(result_returned, safe=False)
        else:
            for query_record in available_record:
                available_record.Available_count -= numS
                available_record.save()
                confirmVal = Confirm.objects.create(Table_name_id = query_record.id, Email_address = Pe, person = Pn, NumSeats_reserved = numS)


            response = "reservation secured! but you took a while to secured the seats"
            confirmStatus = "true"

            context = {
            'response': response,
            'confirmStatus': confirmStatus,
                        
            }

            result_returned = render_to_string('confirm.html', context)
            return JsonResponse(result_returned, safe=False)
    
    else:
        for query in reSresult:
            confirmVal = Confirm.objects.create(Table_name_id = query.Table_name_id, Email_address = Pe, person = Pn, NumSeats_reserved = numS)
            reSresult.delete()
            response = "reservation secured!"
            confirmStatus = "true"

            context = {
            'response': response,
            'confirmStatus': confirmStatus,
                            
                }
            result_returned = render_to_string('confirm.html', context)
            return JsonResponse(result_returned, safe=False)
        