# 데코레이터 - 함수를 인자로 받아서, 새로운 함수를 return
import time

# 데코레이터 정의
def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 함수 시작 시간 기록
        result = func(*args, **kwargs)  # 함수 실행
        end_time = time.time()  # 함수 종료 시간 기록
        print(f"Execution time: {end_time - start_time:.4f} seconds")  # 실행 시간 출력
        return result
    return wrapper


@time_decorator
def example_function(n):
    total = 0
    for i in range(n):
        total += i
    return total

# 함수 호출
## example_function()만 실행했지만, 얘는 time_decorator 이기 때문에, 측정 시간도 출력
## 즉, time_decorator가 포장지 역할을 수행함
result = example_function(1000000)
print(f"Result: {result}")
