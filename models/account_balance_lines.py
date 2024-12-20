from odoo import models, fields

class GeneratedReport(models.Model):
    _name = 'account.balance_sheet.lines'
    _description = 'Reporte'
    
    balance_sheet_id = fields.Many2one('account.balance_sheet', string='ipbu', required=False, ondelete='cascade')

    is_total = fields.Boolean(string='¿Es Total?')
    code_digits = fields.Char(string='Codigos')
    account = fields.Char(string='Cuentas')
    user = fields.Char(string='Terceros')
    detail = fields.Char(string='Detalles')
    notes = fields.Char(string='Notas')
    analytic = fields.Many2many(
        'account.analytic.line',
        'generated_report_analytic_line_rel',
        'generated_report_id',
        'analytic_line_id',
        string='Centro de costo'
    )
    debit = fields.Float(string='Debitos', digits=(16, 2), default=0.0)
    credit = fields.Float(string='Creditos', digits=(16, 2), default=0.0)
    final_balance = fields.Float(string='Balance final', digits=(16, 2), default=0.0)
    start_balance = fields.Float(string='Balance inicial', digits=(16, 2), default=0.0)
    date = fields.Date(string="Date")
    company_doc = fields.Char(string='Documento Tercero')
