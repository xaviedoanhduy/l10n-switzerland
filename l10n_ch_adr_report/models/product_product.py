# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import _, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    adr_report_class_display_name = fields.Char(
        "Name, as required for the DG report",
        compute="_compute_adr_report_class_display_name",
    )

    def _compute_adr_report_class_display_name(self):
        for record in self:
            adr_good = record.adr_goods_id
            res = _(f"UN {adr_good.un_number}, {adr_good.name}")
            if record.nag:
                res += _(f" {record.nag}")

            if record.label_first:
                res += f", {record._get_name_from_selection('label_first')}"

            if record.label_second and record.label_third:
                string_label_second = record._get_name_from_selection("label_second")
                string_label_third = record._get_name_from_selection("label_third")
                res += f", ({string_label_second}, {string_label_third})"
            elif record.label_second:
                res += f", ({record._get_name_from_selection('label_second')})"

            if record.packaging_group:
                res += f", {record._get_name_from_selection('packaging_group')}"

            if adr_good.tunnel_restriction_code:
                string_tunnel_restriction_code = record._get_name_from_selection(
                    "adr_tunnel_restriction_code"
                )
                res += f", ({string_tunnel_restriction_code})"

            if record.envir_hazardous == "yes":
                res += _("Environmentally hazardous")

            record.adr_report_class_display_name = res

    def _get_name_from_selection(self, field_name):
        selection = self._fields[field_name].selection
        if isinstance(selection, list):
            temp_dict = dict(selection)
        else:
            temp_dict = dict(selection(self))
        return temp_dict.get(getattr(self, field_name))
