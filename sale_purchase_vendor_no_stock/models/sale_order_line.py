from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    vendor_id = fields.Many2one(
        "res.partner", string="Vendor", search="_search_vendor_id"
    )
    vendor_id_domain = fields.Binary(
        compute="_compute_vendor_id_domain", store=False, readonly=True
    )

    @api.depends("product_id")
    def _compute_vendor_id_domain(self):
        for item in self:
            # domain = (
            #     [("id", "in", item.product_id.variant_seller_ids.ids)]
            #     if item.order_id
            #     else []
            # )
            # item.vendor_id_domain = json.dumps(domain)
            # import wdb;wdb.set_trace()
            item.vendor_id_domain = item.product_id.variant_seller_ids.ids

    def _prepare_procurement_values(self, group_id=False):
        """Inject in the procurement values the preferred vendor if any, and create
        supplierinfo record for it if it doesn't exist.
        """
        res = super()._prepare_procurement_values(group_id=group_id)
        if self.vendor_id:
            product = self.product_id
            suppinfo = product.with_company(self.company_id.id)._select_seller(
                partner_id=self.vendor_id,
                quantity=self.product_uom_qty,
                uom_id=self.product_uom,
            )
            if not suppinfo:
                suppinfo = self.env["product.supplierinfo"].create(
                    {
                        "product_tmpl_id": product.product_tmpl_id.id,
                        "name": self.vendor_id.id,
                        "min_qty": 0,
                        "company_id": self.company_id.id,
                    }
                )
            res["supplierinfo_id"] = suppinfo
        return res
