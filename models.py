# -*- coding: utf-8 -*-

from openerp import models, fields, api


class AvantMetre(models.Model):
	_name ='gent.avantmetre'
	_inherit = 'mrp.bom'

	rubrique = fields.Char(string="Rubrique")
	nom = fields.Char(string="Nom")
	prix_total = fields.Float(string="Prix Total")
	
	# rubrique_ids =  fields.One2many(comodel_name='gent.avantmetre.rubrique', inverse_name='avantmetre_bom_id', copy=True)
	

# class Rubrique(models.Model):
# 	_name='gent.avantmetre.rubrique'
# 	name = fields.Char(string="Rubrique")
# 	avantmetre_bom_id = fields.Many2one(comodel_name='gent.avantmetre')
# 	avantmetre_bom_line_ids = fields.One2many('mrp.bom.line', 'bom_id', string='BoM Lines')