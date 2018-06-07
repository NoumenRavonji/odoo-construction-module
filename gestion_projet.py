import openpyxl
from tempfile import TemporaryFile
from openerp import models, fields, api
from openerp.api import Environment as env
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from xlrd import open_workbook
import base64
from tempfile import TemporaryFile
import openpyxl
from openpyxl.utils import coordinate_from_string, column_index_from_string
import unicodedata

class GentMrpProduction(models.Model):
	_inherit="mrp.production"
	
# class GentAttachement(models.Model):
# 	_name = "gent.attachement"

class GentProjectAttachement(models.Model):
	_inherit="account.analytic.account"
	
	# name = fields.Char(string="Nom")
	session_ids = fields.One2many('gent.attachement', 'attachement_id', string="Sessions")