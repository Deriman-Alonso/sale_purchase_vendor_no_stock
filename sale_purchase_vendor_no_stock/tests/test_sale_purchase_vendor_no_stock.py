from .common import TestSalePurchaseVendorNoStockBase


class TestSalePurchaseVendorNoStock(TestSalePurchaseVendorNoStockBase):
    def test_misc(self):
        self.sale_order.action_confirm()
        purchase_orders = self.sale_order._get_purchase_orders()
        self.assertEqual(len(purchase_orders), 1)
        self.assertNotIn(self.vendor_a, purchase_orders.partner_id)
        self.assertIn(self.vendor_b, purchase_orders.partner_id)
        self.assertEqual(purchase_orders.partner_id, self.vendor_b)

    def test_misc_force_vendor_restrict(self):
        self.env.company.sale_purchase_force_vendor_restrict = True
        self.sale_order.action_confirm()
        line_0 = self.sale_order.order_line[0]
        partners = self.env["res.partner"].search(line_0.vendor_id_domain)
        self.assertNotIn(self.partner, partners)
        self.assertIn(self.vendor_a, partners)
        self.assertIn(self.vendor_b, partners)

    def test_misc_not_force_vendor_restrict(self):
        self.env.company.sale_purchase_force_vendor_restrict = False
        self.sale_order.action_confirm()
        line_0 = self.sale_order.order_line[0]
        self.assertEqual(line_0.vendor_id_domain, [])
