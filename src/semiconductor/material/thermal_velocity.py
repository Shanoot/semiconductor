
import os
import numpy as np
import scipy.constants as Const
from semiconductor.helper.helper import BaseModelClass
from semiconductor.material import vel_th_models
from semiconductor.material.bandgap_intrinsic import IntrinsicBandGap as Egi


class ThermalVelocity(BaseModelClass):

    '''
    This calculates the thermal velocity.

    inputs:
        1. material: (str)
            The elemental name for the material. Defualt (Si)
        2. temp: (float)
            The temperature of the material in Kelvin (300)
        3. author: (str)
            The author of the model to be used
    '''

    _cal_dts = {
        'material': 'Si',
        'temp': 300.,
        'author': None,
    }

    author_list = 'vel_th.yaml'
    vel_th = None

    def __init__(self, **kwargs):

        # update any values in cal_dts
        # that are passed
        self.calculationdetails = kwargs

        # get the address of the authors list
        author_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            self._cal_dts['material'],
            self.author_list)

        # get the models ready
        self._int_model(author_file)

        # initiate the first model
        self.change_model(self._cal_dts['author'])

    def update(self, **kwargs):
        '''
        a function to update the thermal velocity

        inputs:
            temperature: (optional)
                         in kelvin
            author:  (optional)
                    the author used.
                    If not provided the last provided author is used
                    If no author has been provided,  Couderc's model is used
        output:
            the thermal velocity in cm/s
        '''
        self.calculationdetails = kwargs

        # a check to make sure the model hasn't changed
        if 'author' in kwargs.keys():
            self.change_model(self._cal_dts['author'])

        if 'iEg_author' in self.vals.keys():

            Eg0 = Egi(
                material=self._cal_dts['material'],
                temp=0,
                author=self.vals['iEg_author'],
            ).update()
            Egratio = Eg0 / Egi(
                material=self._cal_dts['material'],
                temp=self._cal_dts['temp'],
                author=self.vals['iEg_author'],
            ).update()

        else:
            Egratio = None

        # if the model required the energy gap, calculate it
        self.vel_th_e, self.vel_th_h = getattr(vel_th_models, self.model)(
            self.vals, temp=self._cal_dts['temp'], Egratio=Egratio)

        return self.vel_th_e, self.vel_th_h
