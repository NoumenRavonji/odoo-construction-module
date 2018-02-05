
# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.api import Environment as env
import openerp.addons.decimal_precision as dp


class AvantMetre(models.Model):
	_inherit = 'mrp.bom'
	_name = "gent.avantmetre"

	# bom_line_ids =  fields.One2many('gent.avantmetre.line', 'bom_id', 'BoM Lines', copy=True)
	rubrique_line_ids =  fields.One2many('gent.avantmetre.rubrique', 'avantmetre_id', 'Rubrique', copy=True)
	nom = fields.Char(string="Nom")
	prix_total = fields.Float(string="Prix Total")
	
	state = fields.Selection([
        ('simple', "Simple"),
        ('avant_metre', "Avant Métré"),
        ('sous_detail', "Sous détail"),
    ], default='simple')

	partner_id=fields.Many2one('res.partner', 'Client', required=True, select=True)
	#rubrique_last = ""
	
	@api.model
	def create(self,vals,context=None):
		print "Produit"
		print vals
		product_id = vals['product_tmpl_id']
		print "hello"
		# ma_liste = vals['rubrique_line_ids'][0][2]['rubrique_bom_line_ids']
		print vals['rubrique_line_ids'][0][2]['rubrique_bom_line_ids'][0][2]['product_id']
		ouv_elt = vals['rubrique_line_ids'][0][2]['rubrique_bom_line_ids'][0][2]['product_id']
		self.env['product.template'].browse([product_id]).write({'gent_type': 'chantier'})
		self.env['product.template'].browse([ouv_elt]).write({'gent_type': 'ouvrage_elementaire'})
		return super(AvantMetre,self).create(vals)



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

class AvantMetreRubrique(models.Model):
	_name = "gent.avantmetre.rubrique"

	rubrique = fields.Char("Rubrique")
	rubrique_bom_line_ids = fields.One2many('gent.avantmetre.line', 'bom_id', 'BoM Lines', copy=True)
	avantmetre_id =  fields.Many2one('gent.avantmetre', 'Parent BoM', ondelete='cascade', select=True, required=True)

	# @api.model
	# def create(self,values, context=None):
	# 	print "A identifier"
	# 	print values

	# 	return super(AvantMetreRubrique,self).create(values)



class AvantMetreLine(models.Model):
	_inherit = "mrp.bom.line"
	_name = 'gent.avantmetre.line'
	
	bom_id =  fields.Many2one('gent.avantmetre.rubrique', 'Parent BoM', ondelete='cascade', select=True, required=True)
	rubrique = fields.Char(string="Rubrique")

class Product2(models.Model):
	_inherit = "product.template"

	gent_type = fields.Selection([('chantier','Chantier'),('ouvrage_elementaire','Ouvrage Elementaire'),('composant_materiaux','Composant Materiaux'),('composant_materiel','Composant Materiel'),('composant_main_d_oeuvre','Composant main d\'oeuvre')])

class Bde(models.Model):
	_inherit = "sale.order"
	

	avantmetre = fields.Many2one(comodel_name='gent.avantmetre', required=True)
	# @api.model
	# def onchange_pricelist_id(self,pricelist_id, order_lines, context=None):
	# 	context = context or {}
	# 	if not pricelist_id:
	# 		return {}
	# 		value = {
	# 		'currency_id': self.pool.get('product.pricelist').browse(self.env.cr, self.env.uid, pricelist_id, context=context).currency_id.id
	# 		}
	# 	if not order_lines or order_lines == [(6, 0, [])]:
	# 		return {'value': value}
	# 		warning = {
	# 			'title': _('Pricelist Warning!'),
	# 			'message' : _('If you change the pricelist of this order (and eventually the currency), prices of existing order lines will not be updated.')
	# 		}
		#return {'warning':{}, 'value': value}

	# @api.onchange('partner_id')
	# def alert(self):
	# 	return {
 #        'warning': {
 #            'title': "Something bad happened",
 #            'message': "It was very bad indeed",
 #        }
 #    }

	@api.onchange('avantmetre')
	def on_change_avantmetre(self):
		print "AVANT METRE CHANGE"
		result = []
		domain = []
		self.order_line = result
		print self.avantmetre.partner_id
		print "price_list"
		# print self.pricelist_id
		self.partner_id = self.avantmetre.partner_id
		for rubrique_line in self.avantmetre.rubrique_line_ids:
			rubrique = self.env['sale_layout.category'].create({"name": rubrique_line.rubrique, "sequence": 10})
			for line in rubrique_line.rubrique_bom_line_ids:
				# print line.product_id
				
				vals = self.pool.get('sale.order.line').product_id_change(self.env.cr, self.env.uid, [], self.pricelist_id.id, line.product_id.id, line.product_qty, line.product_uom.id, 0, False, '', self.partner_id.id)
				vals['value'].update({
					'delay': 0,
					'state': "draft",
	              'product_id': line.product_id.id,
	              'product_uom': line.product_uom,
	              'product_uom_qty': line.product_qty,
	              'price_unit': 0,
	              'sale_layout_cat_id': rubrique
	            })
				result.append(vals['value'])
				
		self.order_line = result

class GentSaleOrderLine(models.Model):
	_inherit = "sale.order.line"
	mo_line = fields.One2many('gent.bde.composant', 'gent_order_line_id', "Main d'oeuvre", copy=True)
	materiel_line = fields.One2many('gent.bde.composant', 'gent_order_line_id', "Matériels", copy=True)
	materiaux_line = fields.One2many('gent.bde.composant', 'gent_order_line_id', "Matériaux", copy=True)



class BdeLine(models.Model):
	_name = 'gent.bde.composant'

	gent_order_line_id = fields.Many2one('sale.order.line', 'Parent Order Line',ondelete='restrict', select=True, readonly=True)


	product_id =  fields.Many2one('product.product', 'Product', domain=[('sale_ok', '=', True)], change_default=True, ondelete='restrict', required=True)
	price_unit = fields.Float('Unit Price', required=True, digits_compute= dp.get_precision('Product Price'))
	price_subtotal =  fields.Float('Montant')
	product_uom_qty =  fields.Float('Quantity', digits_compute= dp.get_precision('Product UoS'), required=True)
	product_uom = fields.Many2one('product.uom', 'Unit of Measure ', required=True)




