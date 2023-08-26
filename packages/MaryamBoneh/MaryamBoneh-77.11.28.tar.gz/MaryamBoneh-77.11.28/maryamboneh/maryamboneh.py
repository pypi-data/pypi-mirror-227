import argparse
import pkg_resources
from .json2turtle import json2turtle
        

def main():
    parser = argparse.ArgumentParser(description='Draw Maryam Boneh')
    parser.add_argument('--svg_file_path', type=str, 
                        default=pkg_resources.resource_filename('maryamboneh', "./maryam.json"), 
                        help='path to SVG file')
    parser.add_argument('--speed', type=int, default=32, help='turtle speed')
    args = parser.parse_args()

    json2turtle(args.svg_file_path, args.speed)


if __name__ == '__main__':
    main()
