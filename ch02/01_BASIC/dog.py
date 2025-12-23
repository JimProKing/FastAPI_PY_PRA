# 02. 클래스 상속

## 오버라이드:: 하위 클래스에서 재정의
# 구현부
class Animal:
    height = 30

    def get_height(self):
        print(f"Animal:: {self.height}")

# class Dog(Animal): ## 상속 받음
#     height = 20
    
#     def get_height(self):
#         # return super().get_height()
#         print(f"Dog:: {self.height}")
# # 출력
# dog = Dog()
# print(dog.get_height())

# 부모 클래스에 접근

class Dog(Animal):
    height = 20

    def get_height(self):
        # return super().get_height()
        print(f"Parent:: {super().height}")

dog = Dog()
print(dog.get_height())