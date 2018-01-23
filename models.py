# -*- coding: utf-8 -*-

from openerp import models, fields, api

# class gent(models.Model):
#     _name = 'gent.gent'

#     name = fields.Char()

class AvantMetre(models.Model):
	_name ='gent.avantmetre'
	_inherit = 'mrp.bom'

	