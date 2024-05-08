from odoo import models, fields, api
from bs4 import BeautifulSoup

class GeneratedReport(models.Model):
    _name = 'generated.report'
    _description = 'Reporte'
    is_total = fields.Boolean(string='¿Es Total?')
    code_digits = fields.Char(string='Codigos')
    account = fields.Char(string='Cuentas')
    user = fields.Char(string='Terceros')
    detail = fields.Char(string='Detalles')
    notes = fields.Char(string='Notas')
    debit = fields.Char(string='Debitos')
    credit = fields.Char(string='Creditos')
    final_balance = fields.Char(string='Balance final')
    start_balance = fields.Char(string='Balance inicial')