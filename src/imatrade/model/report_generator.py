"""This module contains the ReportGenerator class 
which is responsible for generating the close report."""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


class ReportGenerator:
    """This class is responsible for generating the close report."""

    def get_templates_environment(self):
        """Return the templates environment"""
        path = Path(__file__)
        path_report = path.parent.parent / "trading_reports"

        env = Environment(
            loader=FileSystemLoader(path_report),
            autoescape=select_autoescape(["html", "xml"]),
        )
        return env

    def save_report(self, report):
        """Save the report to a file"""

        path = Path(__file__)
        path_report_dir = path.parent.parent / "trading_reports"

        file_number = 1
        file_name = f"{file_number}_close_report.html"

        # Create the full path to the report
        path_report = path_report_dir / file_name

        # Check if file already exists
        while path_report.is_file():
            # If it does, increment the file number and generate a new file name
            file_number += 1
            file_name = f"{file_number}_close_report.html"
            path_report = path_report_dir / file_name

        with path_report.open("w") as file:
            file.write(report)

    def generate_close_report(self, market_data_processor):
        """Generate the close report"""
        env = self.get_templates_environment()
        template = env.get_template("close_report.html.j2")

        position_handler = market_data_processor.get_position_handler()
        financial_management = position_handler.get_financial_management()
        closed_positions = position_handler.get_closed_positions()
        stratgy = market_data_processor.get_startegy()

        # Render the template with the given data
        rendered_report = template.render(
            strategy=stratgy,
            initial_capital=financial_management.initial_capital,
            current_capital=financial_management.current_capital,
            risk_per_trade=financial_management.risk_per_trade,
            total_pnl=financial_management.pnl,
            total_trades=financial_management.trades,
            winning_trades=financial_management.win_trades,
            losing_trades=financial_management.loss_trades,
            stop_loss=financial_management.stop_loss,
            take_profit=financial_management.take_profit,
            closed_positions=closed_positions,  # This should be a list of dictionaries
        )

        self.save_report(rendered_report)
