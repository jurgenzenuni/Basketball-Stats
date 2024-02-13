x = 121

num = str(x)
result = ""
for i in num:
    result += i
result = result[::-1]
if result == num:
    print(True)
else: print(False)

class Solution:
    def isPalindrome(self, x: int) -> bool:
        num = str(x)
        result = ""
        for i in num:
            result += i
        result = result[::-1]
        return result == num