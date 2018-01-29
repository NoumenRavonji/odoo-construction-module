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
	
	partner_id=fields.Many2one('res.partner', 'Client', required=True, select=True)
	#rubrique_last = ""
	
	@api.onchange("bom_line_ids")
	def bom_lines_change(self):
		print "CHANGE"
		rubrique_str = ""
		result =[]
		for line in self.bom_line_ids:
			rubrique_str = line.rubrique
			result.append((0,0,{'product_efficiency': line.product_efficiency, 'product_qty': line.product_qty, 'product_id': line.product_id, 'product_uom': line.product_uom, 'rubrique': line.rubrique}))
		# result.append((0,0,{'rubrique': rubrique_str, 'product_efficiency': 1.0, 'product_qty': 1.0, 'product_uom': 1}))
		#self.rubrique_last = rubrique_str
		#self.bom_line_ids = result

		pass



		# return super(AvantMetre, self).create(value)




class AvantMetreLine(models.Model):
	_inherit = "mrp.bom.line"
	_name = 'gent.avantmetre.line'
	
	bom_id =  fields.Many2one('gent.avantmetre', 'Parent BoM', ondelete='cascade', select=True, required=True)
	rubrique = fields.Char(string="Rubrique")

class Bde(models.Model):
	_inherit = "sale.order"
	
	avantmetre = fields.Many2one(comodel_name='gent.avantmetre')
	# avantmetre = fields.Char(string="Avant-métré")
	# state = fields.Selection([
	# 	'avantmetre' : fields.many2one('res.avantmetre',string="Avant-métré",required=True)
	# ],default='entreprise')
