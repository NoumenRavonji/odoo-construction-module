# -*- coding: utf-8 -*-

from openerp import models, fields, api


class AvantMetre(models.Model):
	_name ='gent.avantmetre'
	_inherit = 'mrp.bom'