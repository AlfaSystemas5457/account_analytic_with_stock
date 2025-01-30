from odoo import fields, models, api, exceptions

class Productcategory(models.Model):
    _inherit = 'product.category'
    
    property_cost_method = fields.Selection(
        selection_add=[('lifo', 'UEPS (últimas Entradas, Primeras Salidas)')]
    )
    

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    @api.depends('product_variant_ids.standard_price')
    def _compute_standard_price(self):
        for product in self:
            if product.categ_id.property_cost_method == "lifo":
                valuation_layers = self.env['purchase.order.line'].search([
                    ('product_id', 'in', product.product_variant_ids.ids),
                    ('product_qty', '>', 0)
                ], order='create_date DESC')
                                
                if valuation_layers:
                    product.standard_price = valuation_layers[0].price_unit
            else:
                super()._compute_standard_price()