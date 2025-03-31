# -*- coding: utf-8 -*-

from xml.dom import ValidationErr
from odoo import models, fields,api 
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'
    
    

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today() + timedelta(days=90),copy=False )
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], default='new',required=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user, copy=False)
    partner_id = fields.Many2one( 'res.partner', string='Buyer')
    tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
    # Champ One2many : une propriété peut avoir plusieurs offres
    offer_ids = fields.One2many(
        'estate.property.offer',  # modèle enfant
        'property_id',            # champ Many2one dans le modèle enfant
        string='Offers'
    )
    total_area = fields.Float(string='Total Area',compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', ondelete='cascade',)
    



    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    # @api.depends('offer_ids.price')
    # def _compute_best_price(self):
    #     for record in self:
    #         record.best_price = record.expected_price
    #         for offer in record.offer_ids:
    #             if offer.price > record.best_price:
    #                 record.best_price = offer.price

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    # cette methode est appelée lorsqu'on modifie le champ garden
    # elle permet de mettre à jour les champs garden_area et garden_orientation
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
            return {
                'warning': {
                    'title': "Avertissement",
                    'message': "Le jardin est activé, la surface a été fixée à 10 et l'orientation à North."
                }
            }
        else:
            self.garden_area = 0
            self.garden_orientation = False
            return {
                'warning': {
                    'title': "Avertissement",
                    'message': "Le jardin est désactivé, les champs relatifs au jardin ont été réinitialisés."
                }
            }
        


    def action_cancel(self):
        for property in self:
            if property.state == 'sold':
                raise UserError("Une propriété vendue ne peut pas être annulée.")
            property.state = 'cancelled'


    def action_sold(self):
        for property in self:
            if property.state == 'cancelled':
                raise UserError("Une propriété annulée ne peut pas être vendue.")
            property.state = 'sold'
            
            
            
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Le prix attendu doit être strictement positif.')
    ]
    
    
    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Le prix de vente doit être positif.')
    ]
    
    
    
    
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue
            min_selling_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_selling_price, precision_rounding=0.01) == -1:
                raise UserError(
                    "Le prix de vente ne peut pas être inférieur à 90% du prix attendu."
                )
    
    