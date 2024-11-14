from odoo import http
from odoo.http import request
import logging


class QuoteController(http.Controller):
    _logger = logging.getLogger(__name__)

    @http.route(
        "/api/wordpress_data", type="json", auth="public", methods=["POST"], csrf=False
    )
    def create_or_update_property(self, **kwargs):
        # Directly retrieve the JSON data
        try:
            data = request.httprequest.get_json()
        except Exception as e:
            self._logger.error(f"Error parsing JSON request: {e}")
            return {"status": "error", "message": "Invalid JSON data."}

        self._logger.info(f"Received JSON data: {data}")  # Log the received data

        # Extract the initial data sent from WordPress
        property_type = data.get("property_type")
        domestic_sub_property_type = data.get("domestic_sub_property_type")
        commercial_sub_property_type = data.get("commercial_sub_property_type")
        name = data.get("name")
        email = data.get("email")
        telephone = data.get("telephone")

        #Extract additional fields if provided
        panel_size = data.get("panel_size")
        battery_capacity = data.get("battery_capacity")
        inverter = data.get("inverter")
        total_price = data.get("total_price")
        address = data.get("address")


        #Check if this is an inital or follow-up submission
        quote_record = request.env["onquote.quotation"].sudo().search(
            [('name', '=', name), ('email', '=', email), ('telephone', '=', telephone)], limit=1
        )


        # Validate that required fields are present
        # if not property_type:
        #     self._logger.error("Missing property_type!")
        #     return {"status": "error", "message": "Property type is required."}

        # Create a new property record in Odoo
        initial_quote_data = {
            "property_type": property_type,
            "domestic_sub_property_type": domestic_sub_property_type,
            "commercial_sub_property_type": commercial_sub_property_type,
            "name": name,
            "email": email,
            "telephone": telephone,
        }

        # Define additional data for updating exisiting records
        additional_data ={}
        if panel_size:
            additional_data["panel_size"] = panel_size
        if battery_capacity:
            additional_data["battery_capacity"] = battery_capacity
        if inverter:
            additional_data["inverter"] = inverter
        if total_price:
            additional_data["total_price"] = total_price
        if address:
            additional_data["address"] = address

        # If record exists, update with additional data; otherwise, create a new record
        if quote_record:
            quote_record.sudo.write(additional_data)
            message = "Quote data has been updated!"

        request.env["onquote.quotation"].sudo().create(quote_data)

        return {"status": "success", "message": "Quote data has been saved."}
