import turtle
import svgpathtools


def svg2turtle(svg_file_path):
    paths, attributes = svgpathtools.svg2paths(svg_file_path)

    # Initialize Turtle graphics
    turtle.speed("fastest")
    turtle.title("Drawing Maryam Boneh")
    turtle.setup(640, 640)
    # turtle.tracer(1, 0)

    # Convert SVG paths to Turtle commands
    for path, attrib in zip(paths, attributes):
        turtle.pencolor(attrib['fill'])
            
        if 'fill' in attrib:
            turtle.fillcolor(attrib['fill'])  # Set fill color based on SVG fill attribute
            turtle.begin_fill()  # Start filling
            
        for segment in path:
            if isinstance(segment, svgpathtools.Line):
                turtle.penup()
                turtle.goto(segment.start.real - 320, -segment.start.imag + 320)
                turtle.pendown()
                turtle.goto(segment.end.real - 320, -segment.end.imag + 320)
            elif isinstance(segment, svgpathtools.CubicBezier):
                turtle.penup()
                turtle.goto(segment.start.real - 320, -segment.start.imag + 320)
                turtle.pendown()
                turtle.goto(segment.control1.real - 320, -segment.control1.imag + 320)
                turtle.goto(segment.control2.real - 320, -segment.control2.imag + 320)
                turtle.goto(segment.end.real - 320, -segment.end.imag + 320)
            # Add more cases for other segment types as needed

        if 'fill' in attrib:
            turtle.end_fill()  # End filling

    # Put text
    turtle.penup()
    turtle.goto(0, 220)
    turtle.pendown()
    turtle.write("I Love You", move=True, align="center", font=("Arial", 40, "normal")) 

    # Keep the window open until the user closes it
    print("Done")
    turtle.done()


if __name__ == '__main__':
    svg2turtle("maryamboneh/maryam.svg")
