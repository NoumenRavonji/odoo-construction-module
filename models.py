
# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.api import Environment as env
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from xlrd import open_workbook
import base64
from tempfile import TemporaryFile
import openpyxl
from openpyxl.utils import coordinate_from_string, column_index_from_string

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
		# print vals['rubrique_line_ids'][0][2]['rubrique_bom_line_ids'][0][2]['product_id']
		try:
			ouv_elt = vals['rubrique_line_ids'][0][2]['rubrique_bom_line_ids'][0][2]['product_id']
			self.env['product.template'].browse([product_id]).write({'gent_type': 'chantier'})
			# self.env['product.template'].browse([ouv_elt]).write({'gent_type': 'ouvrage_elementaire'})
			for i in vals['rubrique_line_ids'][0][2]['rubrique_bom_line_ids']:
				j=i[2]['product_id']
				self.env['product.template'].browse([j]).write({'gent_type': 'ouvrage_elementaire'})
		except:
			print "IndexError"
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
	coeff= fields.Many2one(comodel_name="gent.coeff", string="Coefficient de vente K", store=True)

	def onchange_pricelist_id(self, cr, uid, ids, pricelist_id, order_lines, context=None):
		value = {
            'currency_id': self.pool.get('product.pricelist').browse(cr, uid, pricelist_id, context=context).currency_id.id
		}
		return { 'value': value}


	# @api.onchange('coeff')
	# def on_change_coeff(self):
		
	# 	if(self.coeff.coeff):
	# 		for line in self.order_line:			
	# 			print "CHANGE LINE COEFF"
	# 			print self.coeff.coeff
	# 			print line.prix_debourse
	# 			print line.prix_debourse * self.coeff.coeff
	# 			materiaux_line = []
	# 			if(line.materiaux_line):
	# 				for line2 in line.materiaux_line:
	# 					materiaux_line.append((0,False, {
	# 							'product_id': line2.product_id.id,
	# 							'product_uom_qty': line2.product_uom_qty,
	# 							'product_uom': line2.product_uom.id,
	# 							'price_unit': line2.price_unit,
	# 							'price_subtotal': line2.price_subtotal
	# 							}))
	# 			line.price_unit= line.prix_debourse * self.coeff.coeff
	# 			order_line.append((1, line.id,{
	# 				'product_id': line.product_id.id,
	# 				'product_uom': line.product_uom.id,
	# 				'product_uom_qty': line.product_uom_qty,
	# 				'price_unit': line.price_unit,
	# 				'prix_debourse': line.prix_debourse,
	# 				'price_subtotal': line.price_subtotal,
	# 				'materiaux_line': materiaux_line,
	# 				'ouvrage_elementaire': line.ouvrage_elementaire.id
	# 				}))
	# 	return {'value':{'order_line': order_line}}
					



	# @api.onchange('coeff')
	# def on_change_coeff(self):
	# 	for record in self:
	# 		for line in record.order_line:
	# 			print "CHANGE coef"
	# 			print line
	# 			print line.prix_debourse
	# 			print line.price_unit
	# 			if(self.coeff.coeff):
	# 				print "COEFF HERE"
	# 				print line.id
	# 				print self.coeff.coeff
	# 				print line.prix_debourse
	# 				print line.prix_debourse * self.coeff.coeff
	# 				line.price_unit = line.prix_debourse * self.coeff.coeff
	# 				mo_line = []
	# 				materiaux_line = []
	# 				materiel_line = []
	# 				if(line.mo_line):
	# 					for line2 in line.mo_line:
	# 						mo_line.append([0,0,{
	# 							'product_id': line2.product_id,
	# 							'price_unit': line2.price_unit,
	# 							'price_subtotal': line2.price_subtotal,
	# 							'product_uom_qty': line2.product_uom_qty,
	# 							'product_uom': line2.product_uom.id,
	# 							'gent_mo_order_line_id': line.id
	# 							}])
	# 				if(line.materiaux_line):
	# 					for line2 in line.materiaux_line:
	# 						materiaux_line.append([0,0,{
	# 							'product_id': line2.product_id.id,
	# 							'price_unit': line2.price_unit,
	# 							'price_subtotal': line2.price_subtotal,
	# 							'product_uom_qty': line2.product_uom_qty,
	# 							'product_uom': line2.product_uom.id,
	# 							'gent_materiaux_order_line_id': line.id
	# 							}])
	# 				if(line.materiel_line):
	# 					for line2 in line.materiel_line:
	# 						materiel_line.append([0,0,{
	# 							'product_id': line2.product_id.id,
	# 							'price_unit': line2.price_unit,
	# 							'price_subtotal': line2.price_subtotal,
	# 							'product_uom_qty': line2.product_uom_qty,
	# 							'product_uom': line2.product_uom.id,
	# 							'gent_materiel_order_line_id': line.id
	# 							}])
	# 				line.write( {
	# 					'price_unit': line.prix_debourse * self.coeff.coeff,
	# 					'ouvrage_elementaire': line.ouvrage_elementaire.id,
	# 					'prix_debourse' : line.prix_debourse,
	# 					"price_subtotal": line.price_subtotal,
	# 					'product_id': line.product_id.id,
	# 					'mo_line': mo_line,
	# 					'materiel_line': materiel_line,
	# 					'materiaux_line': materiaux_line
	# 					})
	# 				print line.price_unit
	# 			else:
	# 				# line.update({
	# 				# 	'price_unit': line.prix_debourse
	# 				# 	})
	# 				line.price_unit = line.prix_debourse
	
	@api.one
	@api.onchange('order_line')
	def on_change_order_line(self):
		print "CHANGE ORDER LINE"
		order_line_result = []
		for record in self:
			print "record"
			print record
			for line in record.order_line:
				somme_mo=0
				somme_materiel=0
				somme_materiaux=0

				for line2 in line.mo_line:
					somme_mo += line2.price_subtotal
				for line2 in line.materiel_line:
					somme_materiel += line2.price_subtotal
				for line2 in line.materiaux_line:
					print "MATERIAUX LINE MODIF"
					print line2.product_id
					somme_materiaux += line2.price_subtotal
			
				# line.write({
				# 	'prix_debourse': somme_mo + somme_materiel + somme_materiaux,
				# 	'price_unit': somme_mo + somme_materiel + somme_materiaux
				# 	})


				# if(self.coeff.coeff):
				# 	print "COEFF HERE"
				# 	print line.id
				# 	print self.coeff.coeff
				# 	print line.prix_debourse
				# 	print line.prix_debourse * self.coeff.coeff
				# 	line.write({
				# 		'prix_debourse': line.price_unit,
				# 		'price_unit': line.prix_debourse * self.coeff.coeff
				# 		})
				# else:
				# 	print "NOT COEFF"
				# 	print line.prix_debourse
				# 	line.write({
				# 		'price_unit': line.prix_debourse
				# 		})

			record.currency_id = self.env.ref('base.main_company').currency_id


	# def create(self, cr, uid, values, context=None):
	# 	if values.get('order_id') and values.get('product_id') and  any(f not in values for f in ['name', 'price_unit', 'product_uom_qty', 'product_uom']):
	# 		order = self.pool['sale.order'].read(cr, uid, values['order_id'], ['pricelist_id', 'partner_id', 'date_order', 'fiscal_position'], context=context)
	# 		defaults = self.product_id_change(cr, uid, [], order['pricelist_id'][0], values['product_id'],
	# 			qty=float(values.get('product_uom_qty', False)),
	# 			uom=values.get('product_uom', False),
	# 			qty_uos=float(values.get('product_uos_qty', False)),
	# 			uos=values.get('product_uos', False),
	# 			name=values.get('name', False),
	# 			partner_id=order['partner_id'][0],
	# 			date_order=order['date_order'],
	# 			fiscal_position=order['fiscal_position'][0] if order['fiscal_position'] else False,
	# 			flag=False,  # Force name update
	# 			context=dict(context or {}, company_id=values.get('company_id'))
 #            )['value']
	# 		if defaults.get('tax_id'):
	# 			defaults['tax_id'] = [[6, 0, defaults['tax_id']]]
	# 		values = dict(defaults, **values)

	# 	if(!self.pool['gent.ouvrage.elementaire'].search([('product_id', '=', values.get('product_id'))])):
			# self.pool['gent.ouvrage.elementaire'].create({
			# 	'product_id': values.get('product_id'),

			# 	})

	# 	return super(sale_order_line, self).create(cr, uid, values, context=context)
	# @api.model
	# def create(self,vals, context=None):
	# 	print "BDE a Voir"
	# 	if context is None:
	# 		context = {}
	# 	if vals.get('name', '/') == '/':
	# 		vals['name'] = self.pool.get('ir.sequence').get(self.env.cr, self.env.uid, 'sale.order', context=context) or '/'
	# 	if vals.get('partner_id') and any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id', 'fiscal_position']):
	# 		defaults = self.onchange_partner_id(self.env.cr, self.env.uid, [], vals['partner_id'], context=context)['value']
	# 		if not vals.get('fiscal_position') and vals.get('partner_shipping_id'):
	# 			delivery_onchange = self.onchange_delivery_id(self.env.cr, self.env.uid, [], vals.get('company_id'), None, vals['partner_id'], vals.get('partner_shipping_id'), context=context)
	# 			defaults.update(delivery_onchange['value'])
	# 		vals = dict(defaults, **vals)
	# 	ctx = dict(context or {}, mail_create_nolog=True)
	# 	try:
	# 		for i in vals['order_line'][0][2]['materiaux_line']:
	# 			print "ITO NY I[2]"
	# 			print i[2]
	# 			if(i[2]['product_id']):
	# 				j=i[2]['product_id']
	# 				self.env['product.template'].browse([j]).write({'gent_type': 'composant_materiaux'})
	# 	except KeyError:
	# 		print "Erreur d'index"
	# 	try:
	# 		for i in vals['order_line'][0][2]['materiel_line']:
	# 			if(i[2]['product_id']):
	# 				j=i[2]['product_id']
	# 				self.env['product.template'].browse([j]).write({'gent_type': 'composant_materiel'})
	# 	except KeyError:
	# 		print "Erreur d'index"
	# 	try:
	# 		for i in vals['order_line'][0][2]['mo_line']:
	# 			if(i[2]['product_id']):
	# 				j=i[2]['product_id']
	# 				self.env['product.template'].browse([j]).write({'gent_type': 'composant_main_d_oeuvre'})
	# 	except KeyError:
	# 		print "Erreur d'index"
	# 	new_id = super(Bde, self).create(vals, context=ctx)
	# 	self.message_post(self.env.cr, self.env.uid, [new_id], body=_("Quotation created"), context=ctx)
	# 	return {new_id,super(Bde,self).create(vals)}


	def create(self, cr, uid, vals, context=None):
		print "BDE a Voir"
		# print vals
		if context is None:
			context = {}
		if vals.get('name', '/') == '/':
			vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'sale.order', context=context) or '/'
		if vals.get('partner_id') and any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id', 'fiscal_position']):
			defaults = self.onchange_partner_id(cr, uid, [], vals['partner_id'], context=context)['value']
			if not vals.get('fiscal_position') and vals.get('partner_shipping_id'):
				delivery_onchange = self.onchange_delivery_id(cr, uid, [], vals.get('company_id'), None, vals['partner_id'], vals.get('partner_shipping_id'), context=context)
				defaults.update(delivery_onchange['value'])
			vals = dict(defaults, **vals)
		ctx = dict(context or {}, mail_create_nolog=True)


		try:
			for k in range(0,len(vals['order_line'])):
				# print (vals['order_line'][k])
				try:
					for i in range (0,len(vals['order_line'][k][2]['materiel_line'])):
						if(len(vals['order_line'][k][2]['materiel_line'][i][2])!=0):
						# print (vals['order_line'][k][2]['materiel_line'][i][2]['product_id'])
							mll=vals['order_line'][k][2]['materiel_line'][i][2]['product_id']
							self.pool.get('product.template').browse(cr,uid,mll).write({'gent_type': 'composant_materiel'})
				except:
					print ("no materiel line")
				try:
					for i in range (0,len(vals['order_line'][k][2]['materiaux_line'])):
						if(len(vals['order_line'][k][2]['materiaux_line'][i][2])!=0):
						# print (vals['order_line'][k][2]['materiaux_line'][i][2]['product_id'])
							ml=vals['order_line'][k][2]['materiaux_line'][i][2]['product_id']
							self.pool.get('product.template').browse(cr,uid,ml).write({'gent_type': 'composant_materiaux'})
				except:
					print ("no materiaux line")
				try:
					for i in range (0,len(vals['order_line'][0][2]['mo_line'])):
						if(len(vals['order_line'][k][2]['mo_line'][i][2])!=0):
						# print (vals['order_line'][k][2]['mo_line'][i][2]['product_id'])
							mo=vals['order_line'][k][2]['mo_line'][i][2]['product_id']
							self.pool.get('product.template').browse(cr,uid,mo).write({'gent_type': 'composant_main_d_oeuvre'})
				except:
					print ("no mo line")
		except:
			print ("no")
		new_id = super(Bde, self).create(cr, uid, vals, context=ctx)

		self.message_post(cr, uid, [new_id], body=_("Quotation created"), context=ctx)

		return new_id



	def write(self,cr, uid, ids,vals,context=None):
		print "Modifier"
		# self.button_dummy(cr,uid, ids,vals)
		print vals
		if('coeff' in vals):
			coeff = self.pool.get('gent.coeff').browse(cr,uid,[vals["coeff"]]).coeff
			order_line = self.pool.get("sale.order").browse(cr,uid,ids)
			print order_line
			for line in self.pool.get("sale.order").browse(cr,uid,ids).order_line:
				print "Line"
				print line
				line.write({
					'price_unit': line.prix_debourse * coeff
				})
				print line.price_unit

		if('order_line' in vals):
			for i in range(0,len(vals['order_line'])):
				if vals['order_line'][i][2] != False:
					try:
						for k in range(0,len(vals['order_line'][i][2]['materiaux_line'])):
							print vals['order_line'][i][2]['materiaux_line'][k][2]
							if vals['order_line'][i][2]['materiaux_line'][k][2] != False:
								mll = vals['order_line'][i][2]['materiaux_line'][k][2]['product_id']
								self.pool.get('product.template').browse(cr,uid,mll).write({'gent_type': 'composant_materiaux'})
					except:
						print("aucune modification materiaux_line")
					try:
						for k in range(0,len(vals['order_line'][i][2]['materiel_line'])):
							print vals['order_line'][i][2]['materiel_line'][k][2]
							if vals['order_line'][i][2]['materiel_line'][k][2] != False:
								ml= vals['order_line'][i][2]['materiel_line'][k][2]['product_id']
								self.pool.get('product.template').browse(cr,uid,ml).write({'gent_type': 'composant_materiel'})
					except:
						print("aucune modification materiel_line")
					try:
						for k in range(0,len(vals['order_line'][i][2]['mo_line'])):
							print vals['order_line'][i][2]['mo_line'][k][2]
							if vals['order_line'][i][2]['mo_line'][k][2] != False:
								mo = vals['order_line'][i][2]['mo_line'][k][2]['product_id'] 
								self.pool.get('product.template').browse(cr,uid,mo).write({'gent_type': 'composant_main_d_oeuvre'})
					except:
						print "aucune modification mo_line"
		return super(Bde, self).write(cr, uid,ids, vals, context)


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



	@api.one
	def button_dummy(self, vals):
		res = super(Bde, self).button_dummy()
		print "button_dummy vals"
		print vals
		if(self.coeff.coeff):
			for record in self:
				for line in record.order_line:
					print "BUTTON DUMMY"
					line.price_unit = line.prix_debourse * self.coeff.coeff
					print line.price_unit
		return res


class GentSaleOrderLine(models.Model):
	_inherit = "sale.order.line"

	ouvrage_elementaire = fields.Many2one('gent.ouvrage.elementaire', 'Ouvrage élémentaire', store=True)

	prix_debourse = fields.Float('Prix déboursé', store=True, compute='_compute_oe_pu')

	mo_line = fields.One2many('gent.bde.composant', 'gent_mo_order_line_id', "Main d'oeuvre")
	materiel_line = fields.One2many('gent.bde.composant', 'gent_materiel_order_line_id', "Matériels")
	materiaux_line = fields.One2many('gent.bde.composant', 'gent_materiaux_order_line_id', "Matériaux")

	mo_lines_subtotal = fields.Float('Total')
	price_unit= fields.Float('Unit Price', digits_compute= dp.get_precision('Product Price'), store=True, readonly=True)

	price_subtotal = fields.Float('Montant', digits_compute= dp.get_precision('Product Price'), store=True, readonly=True,compute='_compute_order_line_montant')

	product_id =  fields.Many2one('product.product', 'Product', domain=[('sale_ok', '=', True), ('gent_type', '=', 'ouvrage_elementaire')], change_default=True, readonly=True, states={'draft': [('readonly', False)]}, ondelete='restrict')


	@api.depends('price_unit','product_uom_qty')
	def _compute_order_line_montant(self):
		for record in self:
			record.price_subtotal= record.price_unit * record.product_uom_qty

	@api.one
	@api.depends('mo_line','materiaux_line','materiel_line')
	def _compute_oe_pu(self):
		somme_mo=0
		somme_materiel=0
		somme_materiaux=0
		# try:
		# 	for record in self:
		# 		somme_mo = sum(record.price_subtotal for line in record.mo_line)
		# 		somme_materiaux = sum(record.price_subtotal for line in record.materiel_line)
		# 		somme_materiel = sum(record.price_subtotal for line in record.materiaux_line)
		# except:
		# 	print "Erreur d'index"
		for record in self:
			for line in record.mo_line:
				somme_mo += line.price_subtotal
			for line in record.materiel_line:
				somme_materiel += line.price_subtotal
			for line in record.materiaux_line:
				somme_materiaux += line.price_subtotal
	
		self.prix_debourse = somme_mo + somme_materiel + somme_materiaux
		self.price_unit = somme_mo + somme_materiel + somme_materiaux
		print self.prix_debourse
		print self.price_unit

		# somme_mo = 0
		# somme_materiaux = 0
		# somme_materiel = 0
		# for i in vals['order_line'][0][2]['mo_line']:
		# 	somme_mo += i[2]['price_unit']
		# for i in vals['order_line'][0][2]['materiaux_line']:
		# 	somme_materiel += i[2]['price_unit']
		# for i in vals['order_line'][0][2]['materiel_line']:
		# 	somme_materiel += i[2]['price_unit']
		# pu = somme_materiel+somme_mo+somme_materiaux
		# vals['order_line'][0][2]['price_unit'] = pu
	def create(self, cr, uid, values, context=None):
		print "CREATING SALE ORDER"
		if values.get('order_id') and values.get('product_id') and  any(f not in values for f in ['name', 'price_unit', 'product_uom_qty', 'product_uom']):
			order = self.pool['sale.order'].read(cr, uid, values['order_id'], ['pricelist_id', 'partner_id', 'date_order', 'fiscal_position'], context=context)
			defaults = self.product_id_change(cr, uid, [], order['pricelist_id'][0], values['product_id'],
				qty=float(values.get('product_uom_qty', False)),
				uom=values.get('product_uom', False),
				qty_uos=float(values.get('product_uos_qty', False)),
				uos=values.get('product_uos', False),
				name=values.get('name', False),
				partner_id=order['partner_id'][0],
				date_order=order['date_order'],
				fiscal_position=order['fiscal_position'][0] if order['fiscal_position'] else False,
				flag=False,  # Force name update
                context=dict(context or {}, company_id=values.get('company_id'))
			)['value']
			if defaults.get('tax_id'):
				defaults['tax_id'] = [[6, 0, defaults['tax_id']]]
			values = dict(defaults, **values)
		return super(GentSaleOrderLine, self).create(cr, uid, values, context=context)

	@api.onchange('ouvrage_elementaire')
	def on_change_ouvrage_elementaire(self):
		if(self.ouvrage_elementaire.mo_line):
			self.mo_line = None
			
			for line in self.ouvrage_elementaire.mo_line:
				self.mo_line +=self.mo_line.new({
						'product_id': line.product_id,
						'price_unit': line.price_unit,
						'price_subtotal': line.price_subtotal,
						'product_uom_qty': line.product_uom_qty,
						'product_uom': line.product_uom,
						'gent_mo_order_line_id': self.id

					})
		if(self.ouvrage_elementaire.materiaux_line):
			for line3 in self.materiaux_line:
				line3 = False
			for line in self.ouvrage_elementaire.materiaux_line:
				self.materiaux_line +=self.materiaux_line.new({
						'product_id': line.product_id,
						'price_unit': line.price_unit,
						'price_subtotal': line.price_subtotal,
						'product_uom_qty': line.product_uom_qty,
						'product_uom': line.product_uom,
						'gent_materiaux_order_line_id': self.id

					})
		if(self.ouvrage_elementaire.materiel_line):
			self.materiel_line = self.ouvrage_elementaire.materiel_line
			for line in self.ouvrage_elementaire.materiel_line:
				self.materiel_line +=self.materiel_line.new({
						'product_id': line.product_id,
						'price_unit': line.price_unit,
						'price_subtotal': line.price_subtotal,
						'product_uom_qty': line.product_uom_qty,
						'product_uom': line.product_uom,
						'gent_materiel_order_line_id': self.id

					})


class BdeLine(models.Model):
	_name = 'gent.bde.composant'

	gent_mo_order_line_id = fields.Many2one('sale.order.line', 'Parent Order Line',ondelete='restrict', select=True, readonly=True)
	gent_materiel_order_line_id = fields.Many2one('sale.order.line', 'Parent Order Line',ondelete='restrict', select=True, readonly=True)
	gent_materiaux_order_line_id = fields.Many2one('sale.order.line', 'Parent Order Line',ondelete='restrict', select=True, readonly=True)

	gent_oe_mo_line_id = fields.Many2one('gent.ouvrage.elementaire', 'Parent Order Line',ondelete='restrict', select=True, readonly=True)
	gent_oe_materiel_id = fields.Many2one('gent.ouvrage.elementaire', 'Parent Order Line',ondelete='restrict', select=True, readonly=True)
	gent_oe_materaux_id = fields.Many2one('gent.ouvrage.elementaire', 'Parent Order Line',ondelete='restrict', select=True, readonly=True)

	product_id =  fields.Many2one('product.product', 'Product', domain=[('sale_ok', '=', True)], change_default=True, ondelete='restrict', required=True)
	price_unit = fields.Float('Unit Price', required=True, digits_compute= dp.get_precision('Product Price'))



	price_subtotal =  fields.Float('Montant',compute='_compute_subtotal')
	product_uom_qty =  fields.Float('Quantity', digits_compute= dp.get_precision('Product UoS'), required=True)
	product_uom = fields.Many2one('product.uom', 'Unit of Measure ', required=True)

	@api.one
	@api.depends('price_unit','product_uom_qty')
	def _compute_subtotal(self):
		for record in self:
			record.price_subtotal = record.price_unit * record.product_uom_qty


class OuvrageElementaire(models.Model):
	_name = "gent.ouvrage.elementaire.import"
	excel_file = fields.Binary(string='Excel File')

	@api.multi
	def import_excel(self):
		print "IMPORT EXCEL"
		# Generating of the excel file to be read by openpyxl
		my_file = self.excel_file.decode('base64')
		excel_fileobj = TemporaryFile('wb+')
		excel_fileobj.write(my_file)
		excel_fileobj.seek(0)

		# Create workbook
		wb = openpyxl.load_workbook(excel_fileobj, data_only=True)
		# Get the first sheet of excel file
		ws = wb[wb.get_sheet_names()[0]]

		print "DISPLAYING EXCEL"
		a=list()
		d=dict()
		c=0
		cle=str()
		for row in ws:
			if(row[0].value=="N DE PRIX:001"):
				d={}
				cle=str()
				d['nom_section']=row[1].value
				d['MATERIAUX']=list()
				d['MATERIELS']=list()
				d['MO']=list()
			if row[0].value in ['TOTAL MATERIAUX','TOTAL MATERIELS','DESIGNATION']:
				continue
			if(row[0].value=="MATERIAUX"):
				cle='MATERIAUX'
				continue
			if(row[0].value=="MATERIELS"):
				cle='MATERIELS'
				continue
			if(row[0].value=="MAIN D'OEUVRE"):
				cle='MO'
				continue
			if(row[0].value==None):
				if(row[3].value==None):
					continue	
				else:
					row[0].value=cle+'-'+d['nom_section']
			if(row[0].value=="TOTAL MAIN D\'OEUVRE"):
				cle=str()
				continue
			if(row[1].value==None):
				row[1].value='u'
			# if(row[1].value==None):
			# 	continue
			try:
				d[cle].append({'Designation':row[0].value,'Unite':row[1].value,'Quantite':row[2].value,'Prix Unitaire':row[3].value})
			except KeyError:
				pass
			
			# Insertion de la section dans la liste
			if(d in a):
				continue
			else:
				a.append(d)
			# print d['nom_section']

		for ouvrage in a:
			if (self.env['product.product'].search([['name', '=',ouvrage['nom_section']]])):
				print "Bonjour! :",self.env['product.product'].search([('name','=',ouvrage['nom_section'])]).id
			else:
				self.env['product.template'].create({'name':ouvrage['nom_section'],'gent_type':'ouvrage_elementaire'})
			id_ouv = self.env['product.product'].search([('name','=',ouvrage['nom_section'])]).id
			if (self.env['gent.ouvrage.elementaire'].search([['product_id','=',id_ouv]])):
				print "ouvrage elementaire existant"
			else:
				self.env['gent.ouvrage.elementaire'].create({'product_id':id_ouv,'product_uom':1})
			id_line = self.env['gent.ouvrage.elementaire'].search([['product_id','=',id_ouv]])
			print ouvrage['nom_section'], ":",id_line.id

			for materiaux in ouvrage['MATERIAUX']:
				print "MATERIAUX ",materiaux['Designation']
				if materiaux['Unite'] == 'u':
					materiaux['Unite']='Unité(s)'
				elif materiaux['Unite'] == 'l':
					materiaux['Unite']='Litre(s)'
				elif materiaux['Unite'] == 'Fft':
					materiaux['Unite'] = 'fft'
				elif materiaux['Unite'] == None:
					continue
				if(self.env['product.uom'].search([['name','=',materiaux['Unite']]])):
					id_unit_mo = self.env['product.uom'].search([('name','=',materiaux['Unite'])]).id
					print id_unit_mo
				else:
					print "unite qui n'existe pas encore"
					self.env['product.uom'].create({'name':materiaux['Unite'],'category_id':1})
				if(self.env['product.product'].search([['name','=',materiaux['Designation']]])):
					print "Le produit existe deja"
				else:
					self.env['product.template'].create({'name':materiaux['Designation'],'gent_type':'composant_materiaux'})
				id_mo = self.env['product.product'].search([('name','=',materiaux['Designation'])]).id
				print id_mo
				id_unit_mo = self.env['product.uom'].search([('name','=',materiaux['Unite'])]).id
				print "ID_LINE : ",id_line.id
				
				if(self.env['gent.bde.composant'].search([['product_id','=',id_mo],['product_uom','=',id_unit_mo],['price_unit','=',materiaux['Prix Unitaire']],['product_uom_qty','=',materiaux['Quantite']],['gent_oe_materaux_id','=',id_line.id]])):
					print "BDE_composant existant"
				else:
					self.env['gent.bde.composant'].create({'product_id':id_mo,'product_uom':id_unit_mo,'price_unit':materiaux['Prix Unitaire'],'product_uom_qty':materiaux['Quantite'],'gent_oe_materaux_id':id_line.id})
			for materiel in ouvrage['MATERIELS']:

				if materiel['Unite'] == 'u':
					materiel['Unite']='Unité(s)'
				elif materiel['Unite'] == 'l':
					materiel['Unite']='Litre(s)'
				elif materiel['Unite'] == 'Fft':
					materiel['Unite'] = 'fft'
				elif materiel['Unite'] == None:
					continue
				if(self.env['product.uom'].search([['name','=',materiel['Unite']]])):
					id_unit_mo = self.env['product.uom'].search([('name','=',materiel['Unite'])]).id
					print id_unit_mo
				else:
					print "unite qui n'existe pas encore"
					self.env['product.uom'].create({'name':materiel['Unite'],'category_id':1})
				if(self.env['product.product'].search([['name','=',materiel['Designation']]])):
					print "Le produit existe deja"
				else:
					self.env['product.template'].create({'name':materiel['Designation'],'gent_type':'composant_materiel'})
				id_mo = self.env['product.product'].search([('name','=',materiel['Designation'])]).id
				print id_mo
				id_unit_mo = self.env['product.uom'].search([('name','=',materiaux['Unite'])]).id
				print "ID_LINE : ",id_line.id
				
				if(self.env['gent.bde.composant'].search([['product_id','=',id_mo],['product_uom','=',id_unit_mo],['price_unit','=',materiel['Prix Unitaire']],['product_uom_qty','=',materiel['Quantite']],['gent_oe_materiel_id','=',id_line.id]])):
					print "BDE_composant existant"
				else:
					self.env['gent.bde.composant'].create({'product_id':id_mo,'product_uom':id_unit_mo,'price_unit':materiel['Prix Unitaire'],'product_uom_qty':materiel['Quantite'],'gent_oe_materiel_id':id_line.id})
			for mo in ouvrage['MO']:
				print "MO ",mo['Designation']
				if mo['Unite'] in ['','u','u ']:
					mo['Unite']='Unité(s)'
				elif mo['Unite'] == 'l':
					mo['Unite']='Litre(s)'
				elif mo['Unite'] == 'Fft':
					mo['Unite'] = 'fft'
				elif mo['Unite'] == None:
					continue
				if(self.env['product.uom'].search([['name','=',mo['Unite']]])):
					id_unit_mo = self.env['product.uom'].search([('name','=',mo['Unite'])]).id
					print id_unit_mo
				else:
					print "unite qui n'existe pas encore"
					self.env['product.uom'].create({'name':mo['Unite'],'category_id':1})
				if(self.env['product.product'].search([['name','=',mo['Designation']]])):
					print "Le produit existe deja"
				else:
					self.env['product.template'].create({'name':mo['Designation'],'gent_type':'composant_main_d_oeuvre'})
				id_mo = self.env['product.product'].search([('name','=',mo['Designation'])]).id
				print id_mo
				id_unit_mo = self.env['product.uom'].search([('name','=',mo['Unite'])]).id
				print "ID_LINE : ",id_line.id
				print "HELLO"
				if(self.env['gent.bde.composant'].search([['product_id','=',id_mo],['product_uom','=',id_unit_mo],['price_unit','=',mo['Prix Unitaire']],['product_uom_qty','=',mo['Quantite']],['gent_oe_mo_line_id','=',id_line.id]])):
					print "BDE_composant existant"
				else:
					self.env['gent.bde.composant'].create({'product_id':id_mo,'product_uom':id_unit_mo,'price_unit':mo['Prix Unitaire'],'product_uom_qty':mo['Quantite'],'gent_oe_mo_line_id':id_line.id})
	
class OuvrageElementaire(models.Model):
	_name = "gent.ouvrage.elementaire"
	_rec_name="product_id"

	product_id =  fields.Many2one('product.product', 'Product', domain=[('sale_ok', '=', True), ('gent_type', '=', 'ouvrage_elementaire')], change_default=True, required=True, ondelete='restrict')

	prix_debourse = fields.Float('Prix déboursé', store=True, compute='_compute_oe_pu')

	mo_line = fields.One2many('gent.bde.composant', 'gent_oe_mo_line_id', "Main d'oeuvre", copy=True)
	materiel_line = fields.One2many('gent.bde.composant', 'gent_oe_materiel_id', "Matériels", copy=True)
	materiaux_line = fields.One2many('gent.bde.composant', 'gent_oe_materaux_id', "Matériaux", copy=True)
	price_unit= fields.Float('Unit Price', store=True, readonly=True)
	product_uom_qty= fields.Float('Quantity',default=1, digits_compute= dp.get_precision('Product UoS'), required=True, readonly=True)
	product_uom =  fields.Many2one('product.uom', 'Unit of Measure ', required=True)

	price_subtotal = fields.Float('Montant', digits_compute= dp.get_precision('Product Price'), store=True, readonly=True,compute='_compute_order_line_montant')
	

	# @api.multi
	# def import_excel(self):
	# 	print "IMPORT EXCEL"
	# 	# Generating of the excel file to be read by openpyxl
	# 	my_file = self.excel_file.decode('base64')
	# 	excel_fileobj = TemporaryFile('wb+')
	# 	excel_fileobj.write(my_file)
	# 	excel_fileobj.seek(0)

	# 	# Create workbook
	# 	wb = openpyxl.load_workbook(excel_fileobj, data_only=True)
	# 	# Get the first sheet of excel file
	# 	ws = wb[wb.get_sheet_names()[0]]

	# 	print "DISPLAYING EXCEL"
	# 	# Iteration on each rows in excel
	# 	a=list()
	# 	d=dict()
	# 	c=0
	# 	cle=str()
	# 	for row in ws:
	# 		if(row[0].value=="N DE PRIX:001"):
	# 			d={}
	# 			cle=str()
	# 			d['nom_section']=row[1].value
	# 			d['MATERIAUX']=list()
	# 			d['MATERIELS']=list()
	# 			d['MO']=list()
	# 		if row[0].value in ['TOTAL MATERIAUX','TOTAL MATERIELS','TOTAL MAIN D\'OEUVRE','DESIGNATION']:
	# 			continue
	# 		if(row[0].value=="MATERIAUX"):
	# 			cle='MATERIAUX'
	# 			continue
	# 		if(row[0].value=="MATERIELS"):
	# 			cle='MATERIELS'
	# 			continue
	# 		if(row[0].value=="MAIN D'OEUVRE"):
	# 			cle='MO'
	# 			continue
	# 		if(row[0].value=="TOTAL MAIN D\'OEUVRE"):
	# 			cle=str()
	# 			continue
	# 		try:
	# 			d[cle].append({'Designation':row[0].value,'Unite':row[1].value,'Quantite':row[2].value,'Prix Unitaire':row[3].value})
	# 		except KeyError:
	# 			pass
			
	# 		# Insertion de la section dans la liste
	# 		if(d in a):
	# 			continue
	# 		else:
	# 			a.append(d)
	# 		print a
		# self.env['product.template'].create({'name':'produit_valeur'})
		

	@api.one
	@api.depends('mo_line','materiaux_line','materiel_line')
	def _compute_oe_pu(self):
		somme_mo=0
		somme_materiel=0
		somme_materiaux=0
		# try:
		# 	for record in self:
		# 		somme_mo = sum(record.price_subtotal for line in record.mo_line)
		# 		somme_materiaux = sum(record.price_subtotal for line in record.materiel_line)
		# 		somme_materiel = sum(record.price_subtotal for line in record.materiaux_line)
		# except:
		# 	print "Erreur d'index"
		for record in self:
			for line in record.mo_line:
				somme_mo += line.price_subtotal
			for line in record.materiel_line:
				somme_materiel += line.price_subtotal
			for line in record.materiaux_line:
				somme_materiaux += line.price_subtotal
	
		self.prix_debourse = somme_mo + somme_materiel + somme_materiaux
		self.price_unit = somme_mo + somme_materiel + somme_materiaux
		print self.prix_debourse
		print self.price_unit

	@api.depends('price_unit','product_uom_qty')
	def _compute_order_line_montant(self):
		for record in self:
			record.price_subtotal= record.price_unit * record.product_uom_qty


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


class GentSaleLayout(models.Model):
	_inherit="sale_layout.category"

class GencInvoice(models.Model):
	_inherit="account.invoice"

class GencInvoiceLine(models.Model):
	_inherit="account.invoice.line"

class GentStockMove(models.Model):
	_inherit="stock.move"

class GentStockPicking(models.Model):
	_inherit="stock.picking"

class GentProductProduct(models.Model):
	_inherit="product.product"

class GentProductUom(models.Model):
	_inherit="product.uom"

class GentProductPriceHistory(models.Model):
	_inherit="product.price.history"
