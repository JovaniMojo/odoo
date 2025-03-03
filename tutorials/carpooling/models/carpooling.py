# -*- coding: utf-8 -*-

from odoo import models, fields

class carpooling(models.Model):
    _name ='carpooling.carpooling'
    _description = """ this is a model for carpooling"""

    name = fields.Char(string="Name")
    taken_seats = fields.Integer(string="Taken Seats")




