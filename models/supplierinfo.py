from odoo import fields, models, _, api
from datetime import date

class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    def update_supplier_cost(self, vals):
        return True

    @api.model
    def create(self, vals):
        res = super(SupplierInfo, self).create(vals)
        product_tmpl_id = vals.get('product_tmpl_id')
        currency_id = vals.get('currency_id')
        price = vals.get('price')
        product_tmpl = self.env['product.template'].browse(product_tmpl_id)
        currency = self.env['res.currency'].browse(currency_id)
        new_price = currency._convert(price,product_tmpl.currency_id,company=self.env.user.company_id,date=date.today())
        product_tmpl.standard_price = new_price
        return res

    def write(self, vals):
        res = super(SupplierInfo, self).write(vals)
        for rec in self:
            currency = rec.currency_id
            price = rec.price
            product_tmpl = rec.product_tmpl_id
            new_price = currency._convert(price,product_tmpl.currency_id,company=self.env.user.company_id,date=date.today())
            product_tmpl.standard_price = new_price
        return res
