def get_polygon(n):

    def shape(start_point, angle, length):
        print(f'Start_point: {start_point}')
        print(f'Angle: {angle}')
        print(f'Length: {length}')
        for i in range(n):
            print(f'Side {i+1}')

    return shape


draw_triangle = get_polygon(3)
draw_triangle(start_point=0, angle=30, length=15)