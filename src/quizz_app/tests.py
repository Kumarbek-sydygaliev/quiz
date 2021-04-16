from django.test import TestCase

# Create your tests here.

numbers = [4213, 2143, 1243]

a = []
for num in numbers[::3]:
    try:
        try:
            a.append([
                numbers[numbers.index(num)],
                numbers[numbers.index(num) + 1],
                numbers[numbers.index(num) + 2]
            ])
        except:
            a.append([
                numbers[numbers.index(num)],
                numbers[numbers.index(num) + 1],
            ])
    except:
        a.append([
            numbers[numbers.index(num)],
        ])

print(a)