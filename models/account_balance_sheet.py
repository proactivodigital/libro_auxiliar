import json
from odoo import models, fields, api
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

class AccountBalanceSheet(models.Model):
    _name = 'account.balance_sheet'
    _description = 'Balance Sheet'

    first_day_last_month = datetime.now().replace(day=1) - timedelta(days=1)
    first_day_last_month = first_day_last_month.replace(day=1)
    last_day_last_month = datetime.now().replace(day=1) - timedelta(days=1)

    date_from = fields.Date(string='Desde', default=first_day_last_month)
    date_to = fields.Date(string='Hasta', default=last_day_last_month)
    partner_id = fields.Many2one('res.partner', string='Partner')
    account_id_from = fields.Many2one('account.account', string='From Account')
    account_id_to = fields.Many2one('account.account', string='To Account')

    code_digits = fields.Char(string='Codigos')
    account = fields.Char(string='Cuentas')
    user = fields.Char(string='Terceros')
    debit = fields.Float(string='Debitos', digits=(16, 2), default=0.0)
    credit = fields.Float(string='Creditos', digits=(16, 2), default=0.0)
    final_balance = fields.Float(string='Balance final', digits=(16, 2), default=0.0)
    start_balance = fields.Float(string='Balance inicial', digits=(16, 2), default=0.0)
    company_doc = fields.Char(string='Documento Tercero')
    date = fields.Date(string="Date")

    def generate_report(self):
        if not self.date_from or not self.date_to:
            raise UserError("Debes completar las fechas 'Desde' y 'Hasta'.")

        date_from = self.date_from.strftime("%Y-%m-%d")
        date_to = self.date_to.strftime("%Y-%m-%d")

        partner_domain = [('date', '>=', date_from), ('date', '<=', date_to)]
        if self.account_id_from:
            partner_domain.append(('account_id.code', '>=', self.account_id_from.code))
        if self.account_id_to:
            partner_domain.append(('account_id.code', '<=', self.account_id_to.code))
        if self.partner_id:
            partner_domain.append(('partner_id', '=', self.partner_id.id))

        self.env['account.balance_sheet'].search([]).unlink()
        excluded_codes = []
        partner_domain.append(('account_id.code', 'not in', excluded_codes))

        moves = self.env['account.move.line'].search(partner_domain)

        for move in moves:
            move_json = json.dumps(move, default=str)
            _logger.info('Datos del movimiento en JSON: %s', move_json)
            self.env['account.balance_sheet'].create({
                'account': f"{move.account_id.name}",
                'code_digits': move.account_id.code,
                'user': move.partner_id.name,
                'company_doc': move.partner_id.vat,
                'start_balance': move.cumulated_balance,
                'debit': move.debit,
                'credit': move.credit,
                'final_balance': move.balance,
            })

    def show_report(self):
        self.generate_report()
        return {
            'name': 'Balance general',
            'type': 'ir.actions.act_window',
            'res_model': 'account.balance_sheet',
            'view_mode': 'tree',
            'target': 'current',
        }