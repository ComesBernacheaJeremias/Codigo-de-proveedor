from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductProduct(models.Model):
    _inherit = 'product.product'

    supplier_code = fields.Char(
        string="Código de Proveedor",
        index=True,
        copy=False,
        help="Código único de proveedor para esta variante."
    )

    @api.constrains('supplier_code')
    def _check_unique_supplier_code_variant(self):
        """
        Evita duplicados entre variantes y templates sin variantes.
        """
        for record in self:
            if not record.supplier_code:
                continue

            # Buscar otro product.product con el mismo código
            exists_in_variant = self.search_count([
                ('id', '!=', record.id),
                ('supplier_code', '=', record.supplier_code)
            ])

            # Buscar templates sin variantes con ese código
            exists_in_template = self.env['product.template'].search_count([
                ('supplier_code', '=', record.supplier_code),
                ('product_variant_count', '=', 1)
            ])

            if exists_in_variant or exists_in_template:
                raise ValidationError("El código de proveedor debe ser único entre productos y variantes.")
