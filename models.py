# -*- coding: utf-8 -*-

from openerp import models, fields, api


class AvantMetre(models.Model):
	_inherit = 'mrp.bom'
	_name = "gent.avantmetre"

	bom_line_ids =  fields.One2many('gent.avantmetre.line', 'bom_id', 'BoM Lines', copy=True)
	rubrique = fields.Char(string="Rubrique")
	nom = fields.Char(string="Nom")
	prix_total = fields.Float(string="Prix Total")
	state = fields.Selection([
        ('simple', "Simple"),
        ('avant_metre', "Avant Métré"),
        ('sous_detail', "Sous détail"),
    ], default='simple')

class AvantMetreLine(models.Model):
	_inherit = "mrp.bom.line"
	_name = 'gent.avantmetre.line'

	bom_id =  fields.Many2one('gent.avantmetre', 'Parent BoM', ondelete='cascade', select=True, required=True)





