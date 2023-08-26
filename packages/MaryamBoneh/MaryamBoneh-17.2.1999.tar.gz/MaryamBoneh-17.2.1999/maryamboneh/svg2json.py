import json
import svgpathtools


def json2turtle(input_svg_path, output_json_path):
    output_json = []
    paths, attributes = svgpathtools.svg2paths(input_svg_path)
    for path, attrib in zip(paths, attributes):
        output_path = {}
        output_path["fill"] = attrib['fill']
        output_path["segments"] = []
        for segment in path:
            if isinstance(segment, svgpathtools.Line):
                output_path["segments"].append({"command": "line",
                                    "start": {"real": segment.start.real, "imag": -segment.start.imag},
                                    "end": {"real": segment.end.real, "imag": -segment.end.imag}})

            elif isinstance(segment, svgpathtools.CubicBezier):
                output_path["segments"].append({"command": "cubic",
                                    "start": {"real": segment.start.real, "imag": -segment.start.imag},
                                    "control1": {"real": segment.control1.real, "imag": -segment.control1.imag},
                                    "control2": {"real": segment.control2.real, "imag": -segment.control2.imag},
                                    "end": {"real": segment.end.real, "imag": -segment.end.imag}})
                
        output_json.append(output_path)

    with open(output_json_path, 'w') as outfile:
        json.dump(output_json, outfile)


if __name__ == "__main__":
    input_svg_path = "maryamboneh/maryam.svg"
    output_json_path = "maryamboneh/maryam.json"
    json2turtle(input_svg_path, output_json_path)
