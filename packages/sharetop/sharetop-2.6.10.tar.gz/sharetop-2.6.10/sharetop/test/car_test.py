from sharetop.core.car.car_detail import get_car_sales


token = "73b6539c457a646e"

d = get_car_sales(token, car_type='suv', pub_date='202302')

print(d)