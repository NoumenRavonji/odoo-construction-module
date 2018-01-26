# -*- coding: utf-8 -*-

from openerp import models, fields, api


class AvantMetre(models.Model):
	_inherit = 'mrp.bom'
	_name = "gent.avantmetre"

	bom_line_ids =  fields.One2many('gent.avantmetre.line', 'bom_id', 'BoM Lines', copy=True)
	nom = fields.Char(string="Nom")
	prix_total = fields.Float(string="Prix Total")
	state = fields.Selection([
        ('simple', "Simple"),
        ('avant_metre', "Avant Métré"),
        ('sous_detail', "Sous détail"),
    ], default='simple')
	
	@api.onchange('bom_line_ids')
	def on_change_bom_line_ids(self):
		print "CHANGE"
		i = 0
		rubrique_str = ""
		# for line in bom_line_ids:
		# 	print line
		# 	if(i == 1):
		# 		rubrique_str = line[2]['rubrique']

		# 	i = i+1
		# 	print line

		print "CHANGE LOOP"
		print self.bom_line_ids

		for line in self.bom_line_ids:
			print line
			if(i == 1):
				rubrique_str = line[2]['rubrique']

		print rubrique_str


		pass

class AvantMetreLine(models.Model):
	_inherit = "mrp.bom.line"
	_name = 'gent.avantmetre.line'

	bom_id =  fields.Many2one('gent.avantmetre', 'Parent BoM', ondelete='cascade', select=True, required=True)
	rubrique = fields.Char(string="Rubrique")

class Bde(models.Model):
	_inherit = "sale.order"
