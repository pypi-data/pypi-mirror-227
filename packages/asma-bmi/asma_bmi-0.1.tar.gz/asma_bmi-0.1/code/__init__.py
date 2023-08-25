def calculate_bmi(weight,height):
    bmi= weight /(height**2)
    return bmi


weight= float (input("enter your weight IN KG :"))
height= float(input("enter your Height IN MATAR :"))

bmi=calculate_bmi(weight,height)
print((bmi),round(bmi,2))