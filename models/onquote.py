import requests

from odoo import models, fields, api
from datetime import datetime


class OnQuote(models.Model):
    _name = "onquote.quotation"
    _description = "Online Quotation"

    property_type = fields.Selection(
        [("domestic", "Domestic"), ("commercial", "Commercial")],
        string="Property Type",
        required=True,
    )
    domestic_sub_property_type = fields.Char(string="Domestic Sub Property Type")
    commercial_sub_property_type = fields.Char(string="Commercial Sub Property Type")
    # number_of_rooms = fields.Integer(string="Number of Rooms")
    panel_size = fields.Float(string="Panel size")
    battery_capacity = fields.Float(string="Battery Capacity")
    inverter = fields.Float(string="inverter")
    total_price = fields.Float(string="Total Price")
    address = fields.Char(string="Address", required=True)
    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email", required=True)
    telephone = fields.Char(string="Telephone", required=True)
    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now)
