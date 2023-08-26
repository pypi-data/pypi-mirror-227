import pkg_resources
from .json2turtle import json2turtle


class MaryamBoneh:
    def __init__(self):
        pass

    @staticmethod
    def draw(svg_file_path):
        json2turtle(svg_file_path)
        

def main():
    MaryamBoneh.draw(pkg_resources.resource_filename('maryamboneh', "./maryam.json"))


if __name__ == '__main__':
    main()
