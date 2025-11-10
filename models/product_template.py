from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    supplier_code = fields.Char(
        string="Código de Proveedor",
        index=True,
        copy=False,
        help="Código único de proveedor para productos sin variantes."
    )
    brand = fields.Char(string="Marca")

    @api.constrains('supplier_code')
    def _check_unique_supplier_code_template(self):
        """
        Evita duplicados entre templates (sin variantes) y variantes.
        Si el template tiene variantes, no se valida el código.
        """
        for record in self:
            if not record.supplier_code or record.product_variant_count > 1:
                # Si tiene variantes o está vacío, no validamos
                continue

            # Verifica duplicado en otros templates sin variantes
            exists_in_template = self.search_count([
                ('id', '!=', record.id),
                ('supplier_code', '=', record.supplier_code),
                ('product_variant_count', '=', 1)
            ])

            # Verifica duplicado en variantes
            exists_in_variant = self.env['product.product'].search_count([
                ('supplier_code', '=', record.supplier_code)
            ])

            if exists_in_template or exists_in_variant:
                raise ValidationError("El código de proveedor debe ser único entre productos y variantes.")

    # ------------------------------------------------------------------
    # Limpieza automática de códigos de proveedor cuando hay variantes
    # ------------------------------------------------------------------
    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.product_variant_count > 1 and record.supplier_code:
            # Si el producto tiene variantes, limpiamos el código del template
            record.supplier_code = False
        return record

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            if rec.product_variant_count > 1 and rec.supplier_code:
                # Si al modificar pasa a tener variantes, borramos el código
                rec.supplier_code = False
        return res

 