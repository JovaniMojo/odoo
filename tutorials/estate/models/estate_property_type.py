# -*- coding: utf-8 -*-

from odoo import models, fields 

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'sequence, name asc'


    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property',  # model name
        'property_type_id',  # field in estate.property that relates to estate.property.type
        string='Properties'
    )
    sequence = fields.Integer( help='Pour aider a mettre le type de propriété dans un ordre spécifique.')
    
    
    
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Le nom du type de propriété doit être unique.')
    ]