# Copyright 2021 ForgeFlow, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_customer = fields.Boolean(
        compute="_compute_is_customer",
        inverse="_inverse_is_customer",
        store=True,
        readonly=False,
        string="Is a Customer",
        default=lambda self: self._default_is_customer(),
    )
    is_supplier = fields.Boolean(
        compute="_compute_is_supplier",
        inverse="_inverse_is_supplier",
        store=True,
        readonly=False,
        string="Is a Supplier",
        default=lambda self: self._default_is_supplier(),
    )

    @api.depends("customer_rank")
    def _compute_is_customer(self):
        for partner in self:
            if not partner.is_customer:
                partner.is_customer = bool(partner.customer_rank)

    @api.depends("supplier_rank")
    def _compute_is_supplier(self):
        for partner in self:
            if not partner.is_supplier:
                partner.is_supplier = bool(partner.supplier_rank)

    def _inverse_is_customer(self):
        for partner in self:
            partners = partner | partner.commercial_partner_id
            if partner.is_customer:
                partners._increase_rank("customer_rank")
            else:
                partners.customer_rank = 0

    def _inverse_is_supplier(self):
        for partner in self:
            partners = partner | partner.commercial_partner_id
            if partner.is_supplier:
                partners._increase_rank("supplier_rank")
            else:
                partners.supplier_rank = 0

    def _default_is_customer(self):
        return self.env.context.get("res_partner_search_mode") == "customer"

    def _default_is_supplier(self):
        return self.env.context.get("res_partner_search_mode") == "supplier"
