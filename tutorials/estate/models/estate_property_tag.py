# -*- coding: utf-8 -*-

from odoo import models, fields 

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    #Tri par ordre alphabétique
    #Notez que l'ordre croissant est implicite. Ainsi, asc peut être omis : _order = "name".
    _order = 'name asc'
    


    name = fields.Char(required=True)
    color = fields.Integer(string='Color')
    
    
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'Le nom du tag doit être unique.')
    ]