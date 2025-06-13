class SimpleMath:
    def square(self, a):
        return a * a
    def cube(self, a):
        return a * a * a

if __name__ == "__main__":
    simple_math = SimpleMath()
    print(simple_math.square(3))
    print(simple_math.cube(3))