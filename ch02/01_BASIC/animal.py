# 01. 찐 시작
# # 이렇게 선언하면, 클래스 변수와 인스턴트 변수 혼란 야기
# class Animal:
#     height=30

# 클래스 선언 시, 이렇게 생성자에서 초기화해야 명확하게 구분됨
class Animal:
    def __init__(self):
        self.height = 30

animal1 = Animal()
animal2 = Animal()
print(animal1.height)
print(animal2.height)

# 인스턴트 변수에 추가
animal1.height = 10
print(animal1.height)
print(animal2.height)

print(animal1.__dict__) # animal1 객체의 내용을 dict으로 반환
print(animal2.__dict__)

