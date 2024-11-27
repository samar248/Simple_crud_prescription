# app.py
from flask import Flask,render_template
from flask_migrate import Migrate
from config import Config
from models import db
import routes

# Initialize Flask app
app = Flask(__name__)

# Load configuration from the config.py file
app.config.from_object(Config)

# Initialize SQLAlchemy and Flask-Migrate
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return render_template("index.html")
@app.route("/products")
def products():
    return render_template("products.html")
@app.route("/prescribers")
def prescribers():
    return render_template("prescribers.html")
@app.route("/patients")
def patients():
    return render_template("patients.html")
@app.route("/prescriptions")
def prescriptions():
    return render_template("prescriptions.html")


################ this is products crud endpoints #################

# Define the route for adding a product (POST)
app.add_url_rule('/add-product', methods=['POST'], view_func=routes.add_product)

# Define the route for getting a product by ID (GET)
app.add_url_rule('/get-product/<int:product_id>', methods=['GET'], view_func=routes.get_product)

# Define the route for getting all products (GET)
app.add_url_rule('/get-products', methods=['GET'], view_func=routes.get_all_products)

# Define the route for updating a product by ID (PUT)
app.add_url_rule('/update-product/<int:product_id>', methods=['PUT'], view_func=routes.update_product)

# Define the route for deleting a product by ID (DELETE)
app.add_url_rule('/delete-product/<int:product_id>', methods=['DELETE'], view_func=routes.delete_product)

################ this is prescriber crud endpoints #################

# Define the route for adding a prescriber (POST)
app.add_url_rule('/add-prescriber', methods=['POST'], view_func=routes.add_prescriber)
# Define the route for getting all prescribers (GET)
app.add_url_rule('/get-prescribers', methods=['GET'], view_func=routes.get_all_prescribers)
# Define the route for getting a prescribers by ID (GET)
app.add_url_rule('/get-prescribers/<int:id>', methods=['GET'], view_func=routes.get_prescriber)
# Define the route for updating a prescribers by ID (PUT)
app.add_url_rule('/prescriber/<int:id>', methods=['PUT'], view_func=routes.update_prescriber)
# Define the route for deleting a prescribers by ID (DELETE)
app.add_url_rule('/del_prescriber/<int:id>', methods=['DELETE'], view_func=routes.delete_prescriber)

################ this is patient crud endpoints #################

# Define the route for adding a patient (POST)
app.add_url_rule('/add-patient', methods=['POST'], view_func=routes.add_patient)
# GET endpoint to fetch all patients
app.add_url_rule('/get-patients', methods=['GET'], view_func=routes.get_all_patients)
# GET endpoint to fetch a specific patient by ID
app.add_url_rule('/get-patients/<int:id>', methods=['GET'], view_func=routes.get_patient_by_id)
# PUT endpoint to update a patient by ID
app.add_url_rule('/patients/<int:id>', methods=['PUT'], view_func=routes.update_patient)
# DELETE endpoint to remove a patient by ID
app.add_url_rule('/del_patient/<int:id>', methods=['DELETE'], view_func=routes.delete_patient)

################ this is PrescriptionHeader crud endpoints #################

# Define the route for adding a prescription-headers (POST)
app.add_url_rule('/prescription-headers', methods=['POST'], view_func=routes.add_prescription_header)
# GET endpoint to fetch all prescription-headers
app.add_url_rule('/get-prescription-headers', methods=['GET'], view_func=routes.get_all_prescription_headers)
#Get a Specific PrescriptionHeader by ID
app.add_url_rule('/get-prescription-headers/<int:id>', methods=['GET'], view_func=routes.get_prescription_header_by_id)
#Update a PrescriptionHeader
app.add_url_rule('/prescription-headers/<int:id>', methods=['PUT'], view_func=routes.update_prescription_header)
#Remove a PrescriptionHeader
app.add_url_rule('/del-prescription-headers/<int:id>', methods=['DELETE'], view_func=routes.delete_prescription_header)

################################ Prescription Line model endpoints ##################################
#Post endpoints Prescription Line model
app.add_url_rule('/prescription-lines', methods=['POST'], view_func=routes.add_prescription_line)
#Get enpoints prescription-lines
app.add_url_rule('/get-prescription-lines', methods=['GET'], view_func=routes.get_all_prescription_lines)
#Get a Specific Prescription Line by ID
app.add_url_rule('/get-prescription-lines/<int:id>', methods=['GET'], view_func=routes.get_prescription_line_by_id)
#Update a Prescription Line
app.add_url_rule('/prescription-lines/<int:id>', methods=['PUT'], view_func=routes.update_prescription_line)
#Remove a Prescription Line
app.add_url_rule('/prescription-lines/<int:id>', methods=['DELETE'], view_func=routes.delete_prescription_line)




if __name__ == '__main__':
    app.run(debug=True)
