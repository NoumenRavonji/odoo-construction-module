
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
		# self.env['product.template'].browse([ouv_elt]).write({'gent_type': 'ouvrage_elementaire'})
		for i in vals['rubrique_line_ids'][0][2]['rubrique_bom_line_ids']:
			j=i[2]['product_id']
			self.env['product.template'].browse([j]).write({'gent_type': 'ouvrage_elementaire'})
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

	coeff= fields.Many2one(comodel_name="gent.coeff")

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
	mo_lines_subtotal = fields.Float('Total')



class BdeLine(models.Model):
	_name = 'gent.bde.composant'

	gent_order_line_id = fields.Many2one('sale.order.line', 'Parent Order Line',ondelete='restrict', select=True, readonly=True)


	product_id =  fields.Many2one('product.product', 'Product', domain=[('sale_ok', '=', True)], change_default=True, ondelete='restrict', required=True)
	price_unit = fields.Float('Unit Price', required=True, digits_compute= dp.get_precision('Product Price'))
	price_subtotal =  fields.Float('Montant', compute='_compute_subtotal')
	product_uom_qty =  fields.Float('Quantity', digits_compute= dp.get_precision('Product UoS'), required=True)
	product_uom = fields.Many2one('product.uom', 'Unit of Measure ', required=True)

	@api.depends('price_unit','product_uom_qty')
	def _compute_subtotal(self):
		for record in self:
			record.price_subtotal = record.price_unit * record.product_uom_qty

class Coeff(models.Model):
	_name="gent.coeff"
	_rec_name = "coeff"
	frais_1 = fields.Float("Frais Généraux proportionnel au débourse", compute = "_compute_frais_1")
	frais_2 = fields.Float("Bénéfice brut et frais proportionnel au prix de revient", compute = "_compute_frais_2")
	frais_3 = fields.Float("Frais proportionnel au prix de règlement", compute = "_compute_frais_3")

	frais_11 = fields.Float("Frais d'agence et patente (%)", default=0)
	frais_12 = fields.Float("Frais de chantier (%)", default=0)
	frais_13 = fields.Float("Frais d'études et de laboratoire (%)", default=0)
	frais_14 = fields.Float("Assurances (%)", default=0)

	frais_21 = fields.Float("Bénéfice net et impôt sur le bénéfice (%)", default=20)
	frais_22 = fields.Float("Aléas techniques (%)", default=0)
	frais_23 = fields.Float("Aléas de révision de prix (%)", default=0)
	frais_24 = fields.Float("Frais financier (%)", default=0)

	tva = fields.Float("Frais financier", default=20)

	frais_31 = fields.Float("Frais pour les entreprises qui n'ont pas leur siège à Madagascar (%)", default=0)

	coeff = fields.Float("Coefficient de vente K", compute="_compute_coeff")



	@api.depends('frais_11', 'frais_12', 'frais_13', 'frais_14')
	def _compute_frais_1(self):
		for record in self:
			record.frais_1 = record.frais_11 + record.frais_12 + record.frais_13 + record.frais_14

	@api.depends('frais_21', 'frais_22', 'frais_23', 'frais_24')
	def _compute_frais_2(self):
		for record in self:
			record.frais_2 = record.frais_21 + record.frais_22 + record.frais_23 + record.frais_24

	@api.depends('frais_31')
	def _compute_frais_3(self):
		for record in self:
			record.frais_3 = record.frais_31

	@api.depends('frais_1', "frais_2", "frais_3", "tva")
	def _compute_coeff(self):
		for record in self:
			record.coeff = ( (1 + (record.frais_1/100) ) *(1 + (record.frais_2/100) ) ) / (1 - (record.frais_3*(1+(record.tva/100))))





