# -*- coding: utf-8 -*-

from openerp import models, fields, api

class AvantMetre(models.Model):
	_name = 'gent.avantmetre'

	name = fields.Char(string="Title", required=True)
	description = fields.Text()
# class gent(models.Model):
#     _name = 'gent.gent'

#     name = fields.Char()

# -*- coding: utf-8 -*-
