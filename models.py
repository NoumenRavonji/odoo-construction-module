# -*- coding: utf-8 -*-

from openerp import models, fields, api


class AvantMetre(models.Model):
	_name ='gent.avantmetre'
	_inherit = 'mrp.bom'

	rubrique = fields.Char(string="Rubrique")
	nom = fields.Char(string="Nom")
	prix_total = fields.Float(string="Prix Total")


	# @api.model
	# def create(self,values):
	# 	print values
	# 	return super(AvantMetre, self).create(values)
