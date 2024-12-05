import json
from odoo import models, fields, api
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

class AccountBalanceSheet(models.Model):
    _name = 'account.balance_sheet'
    _description = 'Balance Sheet'

    balance_sheet_lines = fields.One2many('account.balance_sheet.lines', 'balance_sheet_id')
    date = fields.Date(string='Fecha de generación', default=fields.Date.context_today)
    name = fields.Char(string='Nombre', compute='_compute_name', store=True)

    first_day_last_month = datetime.now().replace(day=1) - timedelta(days=1)
    first_day_last_month = first_day_last_month.replace(day=1)
    last_day_last_month = datetime.now().replace(day=1) - timedelta(days=1)
    date_from = fields.Date(string='Desde', default=first_day_last_month)
    date_to = fields.Date(string='Hasta', default=last_day_last_month)
    partner_id = fields.Many2one('res.partner', string='Partner')
    account_id_from = fields.Many2one('account.account', string='From Account')
    account_id_to = fields.Many2one('account.account', string='To Account')

    @api.depends('date')
    def _compute_name(self):
        for record in self:
            if record.date:
                record.name = f"balance_general_{record.date.strftime('%Y_%m_%d')}"

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

        excluded_codes = []
        partner_domain.append(('account_id.code', 'not in', excluded_codes))

        moves = self.env['account.move.line'].search(partner_domain)

        lines = []
        for move in moves:
            if move.account_id.code:
                lines.append((0, 0, {
                    'account': f"{move.account_id.name}",
                    'code_digits': move.account_id.code,
                    'user': move.partner_id.name,
                    'company_doc': move.partner_id.vat,
                    'start_balance': move.cumulated_balance,
                    'debit': move.debit,
                    'credit': move.credit,
                    'final_balance': move.balance,
                }))

        if not lines:
            raise UserError("No se encontraron movimientos contables para las fechas seleccionadas.")

        self.balance_sheet_lines = sorted(lines, key=lambda m: m[2]['code_digits'])