import ctypes

# 加载动态链接库
ll = ctypes.cdll.LoadLibrary
lib = ll("C:\\Users\\zhangle\\test.so")

# 调用动态链接库中的函数，并打印返回值
result = lib.foo(1, 3)
print("Result:", result)

# 打印完成消息
print('***finish***')

# import ctypes
# so = ctypes.cdll.LoadLibrary
# lib = so("C:\\Users\\zhangle\\testcpp.so")
# print( 'display()')
# lib.display()
# print ('display(100)')
# lib.display_int(100)

