import json
from odoo import models, fields, api
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

class AccountBalanceSheet(models.Model):
    _name = 'account.balance_sheet'
    _description = 'Balance Sheet'

    balance_sheet_lines = fields.One2many('account.balance_sheet.lines')

    first_day_last_month = datetime.now().replace(day=1) - timedelta(days=1)
    first_day_last_month = first_day_last_month.replace(day=1)
    last_day_last_month = datetime.now().replace(day=1) - timedelta(days=1)
    date_from = fields.Date(string='Desde', default=first_day_last_month)
    date_to = fields.Date(string='Hasta', default=last_day_last_month)
    partner_id = fields.Many2one('res.partner', string='Partner')
    account_id_from = fields.Many2one('account.account', string='From Account')
    account_id_to = fields.Many2one('account.account', string='To Account')