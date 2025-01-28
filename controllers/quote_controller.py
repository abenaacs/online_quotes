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
        address = data.get("address")

        # Extract additional fields if provided
        panel_size = data.get("panel_size")
        battery_capacity = data.get("battery_capacity")
        inverter = data.get("inverter")
        total_price = data.get("total_price")

        # Validate that required fields are present
        if not all([name, email, telephone, address]):
            missing_fields = [
                field
                for field in ["name", "email", "telephone", "address"]
                if not data.get(field)
            ]
            self._logger.error(f"Missing required fields: {missing_fields}")
            return {
                "status": "error",
                "message": f"The following fields are required: {', '.join(missing_fields)}.",
            }

        # Check if this is an initial or follow-up submission
        quote_record = (
            request.env["onquote.quotation"]
            .sudo()
            .search(
                [
                    ("name", "=", name),
                    ("email", "=", email),
                    ("telephone", "=", telephone),
                ],
                limit=1,
            )
        )

        # Prepare the data for creating or updating the record
        initial_quote_data = {
            "property_type": property_type,
            "domestic_sub_property_type": domestic_sub_property_type,
            "commercial_sub_property_type": commercial_sub_property_type,
            "name": name,
            "email": email,
            "telephone": telephone,
            "address": address,
        }

        additional_data = {}
        if panel_size:
            additional_data["panel_size"] = panel_size
        if battery_capacity:
            additional_data["battery_capacity"] = battery_capacity
        if inverter:
            additional_data["inverter"] = inverter
        if total_price:
            additional_data["total_price"] = total_price

        # If record exists, update with additional data; otherwise, create a new record
        try:
            if quote_record:
                quote_record.sudo().write(additional_data)
                message = "Quote data has been updated!"
            else:
                # Combined initial and additional data for creating a new record
                quote_record = (
                    request.env["onquote.quotation"]
                    .sudo()
                    .create({**initial_quote_data, **additional_data})
                )
                message = "Quote data has been saved."

            return {"status": "success", "message": message}

        except Exception as e:
            self._logger.error(f"Error while saving quote data: {e}")
            return {
                "status": "error",
                "message": "An error occurred while processing your request. Please try again.",
            }
