from odoo import models, fields, api, exceptions

class AddButtonAccountAnalytic(models.Model):
    _inherit = 'account.analytic.account'
    
    movement_count = fields.Integer(string="Movimientos de stock", compute="_compute_movement_count")
    
    def _compute_movement_count(self):
        self.movement_count = len(self.env['stock.picking'].search([('analytic_account', '=', self.id)]).ids)
    
    def view_stock_movement(self):        
        picking_ids = self.env['stock.picking'].search([
            ('analytic_account', '=', self.id)
        ]).ids
        
        move_ids = self.env['stock.move'].search([
            ('picking_id', 'in', picking_ids)
        ]).ids
        
        return {
            'name': "Movimientos de Stock",
            'type': 'ir.actions.act_window',
            'res_model': 'stock.move',
            'view_mode': 'list',
            'views': [(self.env.ref('account_analytic_with_stock.stock_movement_view_list').id, 'list')],
            'target': 'current',
            'domain': [('id', 'in', move_ids)],
            'context': {'default_picking_id': self.id}
        }

class AddProdductsIDs(models.Model):
    _inherit = 'account.analytic.line'
    
    products_ids = fields.Many2many('product.product', string="Productos", readonly=True)

class AddAnalyticModelToStock(models.Model):
    _inherit = 'stock.picking'
    
    analytic_account = fields.Many2one('account.analytic.account', store=True, string="Cuenta analitica")
    
    def button_validate(self):
        if not self.analytic_account:
            return super(AddAnalyticModelToStock, self).button_validate()
        
        if not self.move_ids or len(self.move_ids) <= 0:
            raise exceptions.UserError('No se han agregado productos.')
        
        inventory_name = (
            f'Movimiento de inventario: {self.display_name} '
            f'Cuenta: {self.analytic_account.display_name} '
        )
        
        existing_line = self.env['account.analytic.line'].search([
            ('account_id', '=', self.analytic_account.id),
            ('name', '=',  inventory_name),
        ], limit=1)
        
        total_value = sum(line.product_id.standard_price * line.product_uom_qty for line in self.move_ids)
        total_qty = sum(line.product_uom_qty for line in self.move_ids)
        total_products = [(6,0,[line.product_id.id for line in self.move_ids ])]
                               
        if existing_line:
            existing_line.write({
                'account_id': self.analytic_account.id,
                'name': inventory_name,
                'date': fields.Date.today(),
                'amount': -total_value,
                'general_account_id': False,
                'user_id': self.env.user.id,
                'company_id': self.env.company.id,
                'ref': self.display_name,
                'unit_amount': total_qty,
                'products_ids': total_products
            })
            
        else:
            self.env['account.analytic.line'].create({
                'account_id': self.analytic_account.id,
                'name': inventory_name,
                'date': fields.Date.today(),
                'amount': -total_value,
                'general_account_id': False,
                'user_id': self.env.user.id,
                'company_id': self.env.company.id,
                'ref': self.display_name,
                'unit_amount': total_qty,
                'products_ids': total_products
            })
            
        return super(AddAnalyticModelToStock, self).button_validate()