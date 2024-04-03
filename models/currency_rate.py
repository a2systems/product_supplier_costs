from odoo import fields, models, _, api
from datetime import date

class ResCurrencyRate(models.Model):
    _inherit = "res.currency.rate"

    @api.model
    def create(self, vals):
        res = super(ResCurrencyRate, self).create(vals)
        currency_id = res.currency_id
        product_tmpl_ids = self.env['product.template'].search([('currency_id','=',currency_id.id)])
        for product_tmpl in product_tmpl_ids:
            if product_tmpl.seller_ids:
                currency = product_tmpl.seller_ids[0].currency_id
                price = product_tmpl.seller_ids[0].price
                new_price = currency._convert(price,currency_id,company=self.env.user.company_id,date=date.today())
                product_tmpl.standard_price = new_price
        seller_ids = self.env['product.supplierinfo'].search([('currency_id','=',currency_id.id)])
        for seller in seller_ids:
            local_currency = seller.currency_id
            currency = product_tmpl.currency_id
            price = seller.price
            new_price = local_currency._convert(price,currency_id,company=self.env.user.company_id,date=date.today())
            product_tmpl.standard_price = new_price
        return res

