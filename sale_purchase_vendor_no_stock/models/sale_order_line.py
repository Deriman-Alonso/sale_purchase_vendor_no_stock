from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_purchase_force_vendor_restrict = fields.Boolean(
        related="company_id.sale_purchase_force_vendor_restrict"
    )


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    vendor_id = fields.Many2one(
        comodel_name="res.partner",
        string="Vendor",
    )
    vendor_id_domain = fields.Binary(
        compute="_compute_vendor_id_domain",
        readonly=True,
        store=False,
    )

    @api.depends("product_id")
    def _compute_vendor_id_domain(self):
        for item in self:
            domain = (
                [("id", "in", item.product_id.variant_seller_ids.partner_id.ids)]
                if item.order_id.sale_purchase_force_vendor_restrict
                else []
            )
            item.vendor_id_domain = domain

    def _retrieve_purchase_partner(self):
        res = super()._retrieve_purchase_partner()
        self.ensure_one()
        if self.vendor_id:
            return self.vendor_id
        return res
