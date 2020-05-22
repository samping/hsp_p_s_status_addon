from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging


_logger = logging.getLogger(__name__)


class sale_order(models.Model):
    _inherit = "sale.order"

    hsp_move_status = fields.Selection([('no','未发货'),('part_ship','部分发货'),('shipped','全部发货')],string='发货情况',default='no',compute='_compute_hsp_move_status')
    hsp_invoice_status = fields.Selection([('no','未开发票'),('invoiced','已开发票')],string='发票情况',default='no',compute='_compute_hsp_invoice_status')
    hsp_payment_status = fields.Selection([('no','未完成收款'),('part_payment','部分收款'),('paymented','已收款')],string='收款情况',default='no',compute='_compute_hsp_payment_status')

    hsp_invoice_date = fields.Date(string='发票日期')
    hsp_invoice_ref = fields.Char(string='发票参考')

    def _compute_hsp_move_status(self):
        for sale in self:
            tem_qty = 0
            tem_qty_delivered = 0
            for line in sale.order_line:
                tem_qty = tem_qty + line.product_uom_qty
                tem_qty_delivered = tem_qty_delivered + line.qty_delivered
            if tem_qty_delivered == 0 :
                sale.hsp_move_status = 'no'
            elif tem_qty_delivered < tem_qty:
                sale.hsp_move_status = 'part_ship'
            elif tem_qty_delivered == tem_qty:
                sale.hsp_move_status = 'shipped'

    def _compute_hsp_payment_status(self):
        for sale in self:
            for line in sale.order_line:
                tem_qty = 0
                tem_qty_invoiced = 0
                for line in sale.order_line:
                    tem_qty = tem_qty + line.product_uom_qty
                    tem_qty_invoiced = tem_qty_invoiced + line.qty_invoiced
                if tem_qty_invoiced < tem_qty:
                    sale.hsp_payment_status = 'no'
                elif tem_qty_invoiced == tem_qty:
                    sale.hsp_payment_status = 'no'
                    invoice_ids = self.env['account.invoice'].sudo().search([('origin','=',sale.name)])
                    for invoice in invoice_ids:
                        if invoice.state == 'paid' :
                            sale.hsp_payment_status = 'paymented'

    def _compute_hsp_invoice_status(self):
        for sale in self:
            if sale.hsp_invoice_date:
                sale.hsp_invoice_status='invoiced'
            else:
                sale.hsp_invoice_status='no'

# class purchase_order_line(models.Model):
#     _inherit = "purchase.order.line"

#     hsp_payment_status = 