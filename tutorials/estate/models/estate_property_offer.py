# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order='price desc'
    
    

    price = fields.Float()
    partner_id = fields.Many2one('res.partner', string='Buyer',required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
        ('pending', 'Pending'),
    ], default='pending',copy=False)
    # Champ Many2one qui référence la propriété à laquelle l'offre est associée
    property_id = fields.Many2one(
        'estate.property',        # modèle parent
        string='Property', 
        ondelete='cascade',        # permet de supprimer les offres associées si la propriété est supprimée
        required=True
    )
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_expired', inverse='_inverse_date_expired')
    
    
    
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'Le prix de l\'offre doit être strictement positif.')
    ]
    
    
    
    
    

    @api.depends('create_date', 'validity')
    def _compute_date_expired(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()  # Si create_date est vide, on prend la date du jour
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_expired(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days


    @api.onchange('date_deadline')
    def _onchange_date_deadline(self):
        # Met à jour validity en temps réel lorsqu'on modifie la date_deadline
        if self.date_deadline:
            if self.create_date:
                self.validity = (self.date_deadline - self.create_date.date()).days
            else:
                self.validity = (self.date_deadline - fields.Date.today()).days             
    
    
 
    def action_accept(self):
        for offer in self:
            # Vérifier qu'une offre n'est pas déjà acceptée pour cette propriété
            accepted_offers = offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted')
            if accepted_offers:
                raise UserError("Une offre a déjà été acceptée pour cette propriété.")
            offer.status = 'accepted'
            # Mettre à jour la propriété associée avec l'acheteur et le prix de vente
            offer.property_id.write({
                'partner_id': offer.partner_id.id,
                'selling_price': offer.price,
                'state': 'sold',
            })
    
    
    def unlink(self):
        for offer in self:
            if offer.status == 'accepted':
                # Réinitialiser les champs de la propriété associée
                offer.property_id.write({
                    'partner_id': False,
                    'selling_price': 0.0,
                    'state': 'new',  # Ou un autre état approprié
                })
        return super(EstatePropertyOffer, self).unlink()        
            

  
    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'        