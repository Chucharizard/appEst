from flask import Blueprint, render_template, request
from .charts import process_chart_data

from . import graficos_bp

@graficos_bp.route("/graficos", methods=["GET", "POST"])
def view_graficos():
    chart_data = None
    error = None

    if request.method == "POST":
        chart_data, error = process_chart_data(request.form)

    return render_template("graficos_index.html", chart_data=chart_data, error=error)
