import json
import turtle

def json2turtle(input_json_path, speed=32):
    turtle.speed("fastest")
    turtle.title("Drawing Maryam Boneh")
    turtle.setup(640, 640)
    turtle.tracer(speed, 0)

    with open(input_json_path, 'r') as input_json:
        json_data = json.load(input_json)
        
        for path in json_data:
            turtle.pencolor(path["fill"])
            turtle.fillcolor(path["fill"])  # Set fill color based on SVG fill attribute
            turtle.begin_fill()  # Start filling

            for segment in path["segments"]:
                if segment['command'] == "line":
                    turtle.penup()
                    turtle.goto(segment["start"]["real"] - 320, segment["start"]["imag"] + 320)
                    turtle.pendown()
                    turtle.goto(segment["end"]["real"] - 320, segment["end"]["imag"] + 320)
                elif segment['command'] == "cubic":
                    turtle.penup()
                    turtle.goto(segment["start"]["real"] - 320, segment["start"]["imag"] + 320)
                    turtle.pendown()
                    turtle.goto(segment["control1"]["real"] - 320, segment["control1"]["imag"] + 320)
                    turtle.goto(segment["control2"]["real"] - 320, segment["control2"]["imag"] + 320)
                    turtle.goto(segment["end"]["real"] - 320, segment["end"]["imag"] + 320)

            turtle.end_fill()

    # Put text
    turtle.penup()
    turtle.goto(0, 220)
    turtle.pendown()
    turtle.write("I Love You", move=True, align="center", font=("Arial", 40, "normal")) 

    # Keep the window open until the user closes it
    print("Done")
    turtle.done()

if __name__ == "__main__":
    json2turtle('maryamboneh/maryam.json')
