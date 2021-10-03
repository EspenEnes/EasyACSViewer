import yaml
from PyQt6.QtWidgets import QFileDialog


class Serializer():

    @staticmethod
    def serialize(data, config):
        with open(QFileDialog.getSaveFileName()[0], 'w+') as stream:
            yaml.dump_all([data, config], stream)


    @staticmethod
    def deserrialize():
        with open(QFileDialog.getOpenFileName()[0], 'r') as stream:
            signalLayout, PLC_Config = [data for data in yaml.load_all(stream, yaml.Loader)]
        return signalLayout, PLC_Config


