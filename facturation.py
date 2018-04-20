# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Facture_libelle(models.Model):
	_inherit = "sale.advance.payment.inv"

	# def _create_invoices(self, cr, uid, inv_values, sale_id, context=None):
 #        inv_obj = self.pool.get('account.invoice')
 #        sale_obj = self.pool.get('sale.order')
 #        inv_id = inv_obj.create(cr, uid, inv_values, context=context)
 #        inv_obj.button_reset_taxes(cr, uid, [inv_id], context=context)
 #        # add the invoice to the sales order's invoices
 #        sale_obj.write(cr, uid, sale_id, {'invoice_ids': [(4, inv_id)]}, context=context)
 #        return inv_id

	def create_invoices(self, cr, uid, ids, context=None):
		""" create invoices for the active sales orders """
		sale_obj = self.pool.get('sale.order')
		act_window = self.pool.get('ir.actions.act_window')
		wizard = self.browse(cr, uid, ids[0], context)
		sale_ids = context.get('active_ids', [])
		if wizard.advance_payment_method == 'percentage':
			print "ETO"
			print sale_ids[0]
			# id_avantmetre = self.browse(cr,uid,[('id', '=', sale_ids[0])])
			id_avantmetre = self.pool.get('sale.order').browse(cr, uid, sale_ids[0], context=context).avantmetre.id
			nom_avantmetre = self.pool.get('gent.avantmetre').browse(cr, uid, id_avantmetre, context=context).name
			id_avantmetre = self.pool.get('product.product').search(cr, uid, [('name_template', '=',nom_avantmetre)], context=context)

			print "AVANTMETRE"
			print id_avantmetre[0]
			print "AVANTMETRE"

		if wizard.advance_payment_method == 'all':
			# create the final invoices of the active sales orders
			res = sale_obj.manual_invoice(cr, uid, sale_ids, context)
			if context.get('open_invoices', False):
				return res
			return {'type': 'ir.actions.act_window_close'}

		if wizard.advance_payment_method == 'lines':
			# open the list view of sales order lines to invoice
			res = act_window.for_xml_id(cr, uid, 'sale', 'action_order_line_tree2', context)
			res['context'] = {
				'search_default_uninvoiced': 1,
				'search_default_order_id': sale_ids and sale_ids[0] or False,
			}
			return res
		assert wizard.advance_payment_method in ('fixed', 'percentage')

		inv_ids = []
		for sale_id, inv_values in self._prepare_advance_invoice_vals(cr, uid, ids, context=context):
			if wizard.advance_payment_method == 'percentage':
				inv_values['invoice_line'][0][2]['product_id']=id_avantmetre[0]
			# inv_values['invoice_line'][0][2]['account_id'] = 515
			inv_ids.append(self._create_invoices(cr, uid, inv_values, sale_id, context=context))
			print "VALUES"
			# print inv_values

		if context.get('open_invoices', False):
			return self.open_invoices( cr, uid, ids, inv_ids, context=context)
		return {'type': 'ir.actions.act_window_close'}

# ids1 = super(account_account, self).search(cr, uid, [('user_type', 'in', ids3)])