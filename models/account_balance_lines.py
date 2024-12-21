from odoo import models, fields

class GeneratedReport(models.Model):
    _name = 'account.balance_sheet.lines'  # Define the model name in Odoo
    _description = 'Report'  # A brief description of what this model represents
    
    # Many2one relationship with the 'account.balance_sheet' model. 
    # This field links each line to a specific balance sheet.
    balance_sheet_id = fields.Many2one('account.balance_sheet', string='Balance Sheet', required=False, ondelete='cascade')

    # Boolean field to indicate whether this line represents a total or not.
    # Useful for aggregating or summarizing data in reports.
    is_total = fields.Boolean(string='Is Total?')

    # Char field to store the account code (e.g., '1010', '2010') associated with this line.
    code_digits = fields.Char(string='Account Codes')

    # Char field to store the account name, typically used to describe the account linked to this balance sheet line.
    account = fields.Char(string='Account')

    # Char field for storing the partner associated with this balance sheet line (e.g., the third party).
    user = fields.Char(string='Partners')

    # Char field for storing additional details or context about this line item in the balance sheet.
    detail = fields.Char(string='Details')

    # Char field for any additional notes related to this balance sheet line.
    notes = fields.Char(string='Notes')

    # Many2many relationship with 'account.analytic.line', used to link this line to cost centers.
    # Allows tracking financial transactions by cost center for more granular analysis.
    analytic = fields.Many2many(
        'account.analytic.line',  # Related model
        'generated_report_analytic_line_rel',  # Relation table name
        'generated_report_id',  # Field in the relation table for the current model's ID
        'analytic_line_id',  # Field in the relation table for the related model's ID
        string='Cost Center'  # Field label in the UI
    )

    # Float field for storing debit amounts, with precision of 16 digits and 2 decimal places.
    # Default value is set to 0.0.
    debit = fields.Float(string='Debits', digits=(16, 2), default=0.0)

    # Float field for storing credit amounts, also with precision of 16 digits and 2 decimal places.
    # Default value is set to 0.0.
    credit = fields.Float(string='Credits', digits=(16, 2), default=0.0)

    # Float field for storing the final balance after applying debits and credits.
    # Default value is set to 0.0.
    final_balance = fields.Float(string='Final Balance', digits=(16, 2), default=0.0)

    # Float field for storing the initial balance before debits and credits are applied.
    # Default value is set to 0.0.
    start_balance = fields.Float(string='Initial Balance', digits=(16, 2), default=0.0)

    # Date field to store the date of the balance sheet line. It helps in sorting and organizing data over time.
    date = fields.Date(string="Date")

    # Char field to store the partner's document (e.g., VAT number) linked to this balance sheet line.
    company_doc = fields.Char(string='Partner Document')
