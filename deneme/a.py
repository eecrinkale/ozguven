
def funcha(input):
    newsayi = input + 100
    return "çift" , newsayi

def funchb(input):
    newsayi = input - 100
    return "tek" , newsayi

sayi = 21

if sayi % 2 == 0:
    cikti1, ciktı2 = funcha(sayi)
else:
    cikti1, ciktı2 = funchb(sayi)


print(cikti1)
print(ciktı2)