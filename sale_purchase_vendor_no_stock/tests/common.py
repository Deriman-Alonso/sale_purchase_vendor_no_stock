from odoo.tests import Form, common


class TestSalePurchaseVendorNoStockBase(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})
        cls.vendor_a = cls.env["res.partner"].create({"name": "Test vendor A"})
        cls.vendor_b = cls.env["res.partner"].create({"name": "Test vendor B"})
        cls.vendor_c = cls.env["res.partner"].create({"name": "Test vendor C"})
        cls.product_a = cls.env["product.product"].create(
            {
                "name": "Test product A",
                "detailed_type": "service",
                "service_to_purchase": "True",
                "seller_ids": [
                    (0, 0, {"partner_id": cls.vendor_a.id, "min_qty": 1, "price": 40}),
                    (0, 0, {"partner_id": cls.vendor_b.id, "min_qty": 1, "price": 50}),
                ],
            }
        )
        cls.product_b = cls.env["product.product"].create(
            {
                "name": "Test product B",
            }
        )
        cls.product_c = cls.env["product.product"].create(
            {
                "name": "Test product C",
                "detailed_type": "service",
                "service_to_purchase": "False",
                "seller_ids": [
                    (0, 0, {"partner_id": cls.vendor_a.id, "min_qty": 1, "price": 40}),
                    (0, 0, {"partner_id": cls.vendor_b.id, "min_qty": 1, "price": 50}),
                    (0, 0, {"partner_id": cls.vendor_c.id, "min_qty": 1, "price": 10}),
                ],
            }
        )
        cls.sale_order = cls._create_sale_order(cls)

    def _create_sale_order(self):
        order_form = Form(self.env["sale.order"])
        order_form.partner_id = self.partner
        for product in [self.product_a, self.product_b, self.product_c]:
            with order_form.order_line.new() as line_form:
                line_form.product_id = product
                line_form.vendor_id = self.vendor_b

        return order_form.save()
