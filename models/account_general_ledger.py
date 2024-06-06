from odoo import models, fields, api
import logging
from datetime import datetime, timedelta

class AccountGeneralLedger(models.Model):
    _name = 'account.general_ledger'
    _description = 'Libro auxiliar'

    first_day_last_month = datetime.now().replace(day=1) - timedelta(days=1)
    first_day_last_month = first_day_last_month.replace(day=1)
    last_day_last_month = datetime.now().replace(day=1) - timedelta(days=1)

    date_from = fields.Date(string='Desde', default=first_day_last_month)
    date_to = fields.Date(string='Hasta', default=last_day_last_month)
    partner_id = fields.Many2one('res.partner', string='Tercero')
    account_id_from = fields.Many2one('account.account', string='Desde cuenta', domain="[('code', 'not in', ['111001', '111002', '111003'])]")
    account_id_to = fields.Many2one('account.account', string='Hasta cuenta', domain="[('code', 'not in', ['111001', '111002', '111003'])]")

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

        self.env['generated.report'].search([]).unlink()
        excluded_codes = ['111001', '111002', '111003']
        partner_domain.append(('account_id.code', 'not in', excluded_codes))

        moves = self.env['account.move.line'].search(partner_domain)
        valid_moves = [move for move in moves if move.account_id and move.account_id.code]
        sorted_moves = sorted(valid_moves, key=lambda x: x.account_id.code, reverse=False)

        before_account = None
        before_account_code = None
        before_account_total = {'debit': 0.0, 'credit': 0.0, 'start_balance': 0.0, 'final_balance': 0.0}
        total = {'debit': 0.0, 'credit': 0.0, 'start_balance': 0.0, 'final_balance': 0.0}

        for move in sorted_moves:
            if before_account_code != move.account_id.code:
                if before_account:
                    self.env['generated.report'].create({
                        'code_digits': before_account.code,
                        'account': before_account.name,
                        'user': 'Total',
                        'analytic': [(6, 0, [])],
                        'start_balance': before_account_total['start_balance'],
                        'debit': before_account_total['debit'],
                        'credit': before_account_total['credit'],
                        'final_balance': before_account_total['final_balance'],
                        'is_total': True
                    })

                before_account = move.account_id
                before_account_code = move.account_id.code
                before_account_total = {'debit': 0.0, 'credit': 0.0, 'start_balance': 0.0, 'final_balance': 0.0}

            before_account_total['start_balance'] += move.cumulated_balance
            before_account_total['credit'] += move.credit
            before_account_total['debit'] += move.debit
            before_account_total['final_balance'] += move.balance
            total['start_balance'] += move.cumulated_balance
            total['credit'] += move.credit
            total['debit'] += move.debit
            total['final_balance'] += move.balance

            self.env['generated.report'].create({
                'code_digits': move.account_id.code,
                'account': move.account_id.name,
                'user': move.partner_id.name,
                'detail': move.move_name,
                'notes': move.ref,
                'analytic': [(6, 0, move.analytic_line_ids.ids)],
                'start_balance': move.cumulated_balance,
                'debit': move.debit,
                'credit': move.credit,
                'final_balance': move.balance,
            })

        if before_account:
            self.env['generated.report'].create({
                'code_digits': before_account.code,
                'account': before_account.name,
                'user': 'Total',
                'analytic': [(6, 0, [])],
                'start_balance': before_account_total['start_balance'],
                'debit': before_account_total['debit'],
                'credit': before_account_total['credit'],
                'final_balance': before_account_total['final_balance'],
                'is_total': True
            })

        self.env['generated.report'].create({
            'user': 'Total',
            'analytic': [(6, 0, [])],
            'start_balance': total['start_balance'],
            'debit': total['debit'],
            'credit': total['credit'],
            'final_balance': total['final_balance'],
            'is_total': True
        })

    def show_report(self):
        self.generate_report()
        return {
            'name': 'Generated Report',
            'type': 'ir.actions.act_window',
            'res_model': 'generated.report',
            'view_mode': 'tree',
            'target': 'current',
        }
