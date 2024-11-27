# routes.py
from flask import request, jsonify
from datetime import datetime
from models import db, Product, Prescriber, Patient, PrescriptionHeader, PrescriptionLines
from sqlalchemy.exc import SQLAlchemyError  # Ensure this is imported

############  Products endpoint data  ########################

# Existing POST endpoint
def add_product():
    # Get data from the POST request (expects JSON)
    data = request.get_json()
    
    # Validate data
    if not data or 'name' not in data or 'cost_price' not in data or 'retail_price' not in data or 'sale_price' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create a new product instance
    new_product = Product(
        name=data['name'],
        cost_price=data['cost_price'],
        retail_price=data['retail_price'],
        sale_price=datetime.strptime(data['sale_price'], '%Y-%m-%d').date() if 'sale_price' in data else None,
        is_pom=data.get('is_pom', 0),
        created=datetime.utcnow(),
        updated=datetime.utcnow(),
        created_by=data.get('created_by', None),
        updated_by=data.get('updated_by', None)
    )

    # Add product to the session and commit to the database
    db.session.add(new_product)
    db.session.commit()

    # Return success response with the product data
    return jsonify({
        'id': new_product.id,
        'name': new_product.name,
        'cost_price': new_product.cost_price,
        'retail_price': new_product.retail_price,
        'sale_price': new_product.sale_price.isoformat(),
        'is_pom': new_product.is_pom,
        'created': new_product.created.isoformat(),
        'updated': new_product.updated.isoformat(),
        'created_by': new_product.created_by,
        'updated_by': new_product.updated_by
    }), 201

# New GET endpoint to fetch a product by its ID
def get_product(product_id):
    try:
        # Fetch the product from the database
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Return the product data
        return jsonify({
            'id': product.id,
            'name': product.name,
            'cost_price': product.cost_price,
            'retail_price': product.retail_price,
            'sale_price': product.sale_price.isoformat(),
            'is_pom': product.is_pom,
            'created': product.created.isoformat(),
            'updated': product.updated.isoformat(),
            'created_by': product.created_by,
            'updated_by': product.updated_by
        })
    
    except SQLAlchemyError as e:
        # Handle SQLAlchemy errors
        return jsonify({'error': str(e)}), 500

# New GET endpoint to fetch all products
def get_all_products():
    try:
        # Fetch all products from the database
        products = Product.query.all()
        
        # If no products are found
        if not products:
            return jsonify({'error': 'No products found'}), 404
        
        # Convert the list of products to a list of dictionaries
        product_list = []
        for product in products:
            product_list.append({
                'id': product.id,
                'name': product.name,
                'cost_price': product.cost_price,
                'retail_price': product.retail_price,
                'sale_price': product.sale_price.isoformat(),
                'is_pom': product.is_pom,
                'created': product.created.isoformat(),
                'updated': product.updated.isoformat(),
                'created_by': product.created_by,
                'updated_by': product.updated_by
            })
        
        # Return the list of products
        return jsonify(product_list)
    
    except SQLAlchemyError as e:
        # Handle SQLAlchemy errors
        return jsonify({'error': str(e)}), 500

# New PUT endpoint to update a product by ID
def update_product(product_id):
    try:
        # Fetch the product from the database
        product = Product.query.get(product_id)

        # If product is not found
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        # Get data from the PUT request (expects JSON)
        data = request.get_json()

        # Update fields with the provided data (use defaults if not provided)
        if 'name' in data:
            product.name = data['name']
        if 'cost_price' in data:
            product.cost_price = data['cost_price']
        if 'retail_price' in data:
            product.retail_price = data['retail_price']
        if 'sale_price' in data:
            product.sale_price = datetime.strptime(data['sale_price'], '%Y-%m-%d').date()
        if 'is_pom' in data:
            product.is_pom = data['is_pom']
        if 'updated_by' in data:
            product.updated_by = data['updated_by']
        
        # Update the 'updated' timestamp
        product.updated = datetime.utcnow()

        # Commit the changes to the database
        db.session.commit()

        # Return the updated product data
        return jsonify({
            'id': product.id,
            'name': product.name,
            'cost_price': product.cost_price,
            'retail_price': product.retail_price,
            'sale_price': product.sale_price.isoformat(),
            'is_pom': product.is_pom,
            'created': product.created.isoformat(),
            'updated': product.updated.isoformat(),
            'created_by': product.created_by,
            'updated_by': product.updated_by
        })
    
    except SQLAlchemyError as e:
        # Handle SQLAlchemy errors
        return jsonify({'error': str(e)}), 500

# New DELETE endpoint to delete a product by ID
def delete_product(product_id):
    try:
        # Fetch the product from the database
        product = Product.query.get(product_id)

        # If product is not found
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        # Delete the product from the database
        db.session.delete(product)
        db.session.commit()

        # Return success message
        return jsonify({'message': f'Product with ID {product_id} has been deleted successfully'}), 200
    
    except SQLAlchemyError as e:
        # Handle SQLAlchemy errors
        return jsonify({'error': str(e)}), 500
    

############# prescriber model endpoints #####################

#add prescriber
def add_prescriber():
    # Get data from the POST request (expects JSON)
    data = request.get_json()

    # Validate input data
    if not data or 'first_name' not in data or 'last_name' not in data or 'email' not in data or 'registration_number' not in data or 'signature' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    # Create a new Prescriber object
    new_prescriber = Prescriber(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        registration_number=data['registration_number'],
        signature=data['signature'],
        created=datetime.utcnow(),
        updated=datetime.utcnow(),
        created_by=data.get('created_by'),
        updated_by=data.get('updated_by')
    )

    # Add and commit the new prescriber to the database
    db.session.add(new_prescriber)
    db.session.commit()

    # Return a success response with the newly created prescriber details
    return jsonify({
        'id': new_prescriber.id,
        'first_name': new_prescriber.first_name,
        'last_name': new_prescriber.last_name,
        'email': new_prescriber.email,
        'registration_number': new_prescriber.registration_number,
        'signature': new_prescriber.signature,
        'created': new_prescriber.created.isoformat(),
        'updated': new_prescriber.updated.isoformat(),
        'created_by': new_prescriber.created_by,
        'updated_by': new_prescriber.updated_by
    }), 201


# GET endpoint to fetch all prescribers
def get_all_prescribers():
    prescribers = Prescriber.query.all()  # Fetch all prescribers

    # If no prescribers are found, return an empty list
    if not prescribers:
        return jsonify({'message': 'No prescribers found'}), 404

    # Return a list of prescribers
    return jsonify([{
        'id': prescriber.id,
        'first_name': prescriber.first_name,
        'last_name': prescriber.last_name,
        'email': prescriber.email,
        'registration_number': prescriber.registration_number,
        'signature': prescriber.signature,
        'created': prescriber.created.isoformat(),
        'updated': prescriber.updated.isoformat(),
        'created_by': prescriber.created_by,
        'updated_by': prescriber.updated_by
    } for prescriber in prescribers]), 200

# GET endpoint to fetch a single prescriber by ID
def get_prescriber(id):
    prescriber = Prescriber.query.get(id)  # Fetch a single prescriber by ID

    # If the prescriber is not found, return a 404 error
    if not prescriber:
        return jsonify({'error': 'Prescriber not found'}), 404

    # Return the prescriber data
    return jsonify({
        'id': prescriber.id,
        'first_name': prescriber.first_name,
        'last_name': prescriber.last_name,
        'email': prescriber.email,
        'registration_number': prescriber.registration_number,
        'signature': prescriber.signature,
        'created': prescriber.created.isoformat(),
        'updated': prescriber.updated.isoformat(),
        'created_by': prescriber.created_by,
        'updated_by': prescriber.updated_by
    }), 200


# PUT endpoint to update a prescriber

def update_prescriber(id):
    # Fetch the prescriber by ID
    prescriber = Prescriber.query.get(id)

    # Check if the prescriber exists
    if not prescriber:
        return jsonify({'error': 'Prescriber not found'}), 404

    # Get the JSON data from the request
    data = request.get_json()

    # Validate input
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Update fields if they are provided
    prescriber.first_name = data.get('first_name', prescriber.first_name)
    prescriber.last_name = data.get('last_name', prescriber.last_name)
    prescriber.email = data.get('email', prescriber.email)
    prescriber.registration_number = data.get('registration_number', prescriber.registration_number)
    prescriber.signature = data.get('signature', prescriber.signature)
    prescriber.updated = datetime.utcnow()  # Update the `updated` timestamp
    prescriber.updated_by = data.get('updated_by', prescriber.updated_by)

    # Commit the changes to the database
    db.session.commit()

    # Return the updated prescriber details
    return jsonify({
        'id': prescriber.id,
        'first_name': prescriber.first_name,
        'last_name': prescriber.last_name,
        'email': prescriber.email,
        'registration_number': prescriber.registration_number,
        'signature': prescriber.signature,
        'created': prescriber.created.isoformat(),
        'updated': prescriber.updated.isoformat(),
        'created_by': prescriber.created_by,
        'updated_by': prescriber.updated_by
    }), 200

# DELETE endpoint to remove a prescriber by ID
def delete_prescriber(id):
    # Fetch the prescriber by ID
    prescriber = Prescriber.query.get(id)

    # Check if the prescriber exists
    if not prescriber:
        return jsonify({'error': 'Prescriber not found'}), 404

    # Delete the prescriber from the database
    db.session.delete(prescriber)
    db.session.commit()

    # Return a success message
    return jsonify({'message': f'Prescriber with ID {id} has been deleted successfully'}), 200


############# Patient model endpoints #####################
# POST endpoint to add a new patient
def add_patient():
    # Get JSON data from the request
    data = request.get_json()

    # Validate the required fields
    required_fields = ['first_name', 'last_name', 'email', 'dob', 'prescriber_id']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    # Validate if prescriber_id exists
    prescriber = Prescriber.query.get(data['prescriber_id'])
    if not prescriber:
        return jsonify({'error': 'Prescriber with the given ID does not exist'}), 404

    try:
        # Create a new Patient instance
        new_patient = Patient(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            dob=datetime.strptime(data['dob'], '%Y-%m-%d').date(),
            prescriber_id=data['prescriber_id'],
            created=datetime.utcnow(),
            updated=datetime.utcnow(),
            created_by=data.get('created_by', None),
            updated_by=data.get('updated_by', None)
        )

        # Add the new patient to the database
        db.session.add(new_patient)
        db.session.commit()

        # Return the created patient details
        return jsonify({
            'id': new_patient.id,
            'first_name': new_patient.first_name,
            'last_name': new_patient.last_name,
            'email': new_patient.email,
            'dob': new_patient.dob.isoformat(),
            'prescriber_id': new_patient.prescriber_id,
            'created': new_patient.created.isoformat(),
            'updated': new_patient.updated.isoformat(),
            'created_by': new_patient.created_by,
            'updated_by': new_patient.updated_by
        }), 201

    except Exception as e:
        return jsonify({'error': 'An error occurred while adding the patient', 'details': str(e)}), 500
    

# GET endpoint to fetch all patients

def get_all_patients():
    try:
        # Query all patients from the database
        patients = Patient.query.all()

        # Serialize the patients into a list of dictionaries
        patient_list = [
            {
                'id': patient.id,
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'email': patient.email,
                'dob': patient.dob.isoformat(),
                'prescriber_id': patient.prescriber_id,
                'created': patient.created.isoformat(),
                'updated': patient.updated.isoformat(),
                'created_by': patient.created_by,
                'updated_by': patient.updated_by
            }
            for patient in patients
        ]

        # Return the list of patients
        return jsonify(patient_list), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching patients', 'details': str(e)}), 500
    

# GET endpoint to fetch a specific patient by ID

def get_patient_by_id(id):
    try:
        # Query the patient by ID
        patient = Patient.query.get(id)

        # If the patient does not exist, return a 404 error
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404

        # Serialize the patient data into a dictionary
        patient_data = {
            'id': patient.id,
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'email': patient.email,
            'dob': patient.dob.isoformat(),
            'prescriber_id': patient.prescriber_id,
            'created': patient.created.isoformat(),
            'updated': patient.updated.isoformat(),
            'created_by': patient.created_by,
            'updated_by': patient.updated_by
        }

        # Return the patient data
        return jsonify(patient_data), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching the patient', 'details': str(e)}), 500


# PUT endpoint to update a patient by ID
def update_patient(id):
    # Get the JSON data from the request
    data = request.get_json()

    # Fetch the patient by ID
    patient = Patient.query.get(id)

    # If the patient doesn't exist, return a 404 error
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    # Update fields if provided in the request
    try:
        if 'first_name' in data:
            patient.first_name = data['first_name']
        if 'last_name' in data:
            patient.last_name = data['last_name']
        if 'email' in data:
            patient.email = data['email']
        if 'dob' in data:
            patient.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
        if 'prescriber_id' in data:
            # Validate the provided prescriber_id
            prescriber = Prescriber.query.get(data['prescriber_id'])
            if not prescriber:
                return jsonify({'error': 'Prescriber with the given ID does not exist'}), 404
            patient.prescriber_id = data['prescriber_id']
        if 'updated_by' in data:
            patient.updated_by = data['updated_by']

        # Update the `updated` timestamp
        patient.updated = datetime.utcnow()

        # Commit the changes to the database
        db.session.commit()

        # Return the updated patient details
        return jsonify({
            'id': patient.id,
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'email': patient.email,
            'dob': patient.dob.isoformat(),
            'prescriber_id': patient.prescriber_id,
            'created': patient.created.isoformat(),
            'updated': patient.updated.isoformat(),
            'created_by': patient.created_by,
            'updated_by': patient.updated_by
        }), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while updating the patient', 'details': str(e)}), 500
    

# DELETE endpoint to remove a patient by ID

def delete_patient(id):
    try:
        # Fetch the patient by ID
        patient = Patient.query.get(id)

        # If the patient does not exist, return a 404 error
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404

        # Delete the patient record
        db.session.delete(patient)
        db.session.commit()

        # Return a success message
        return jsonify({'message': f'Patient with ID {id} has been deleted successfully'}), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': 'An error occurred while deleting the patient', 'details': str(e)}), 500
    


############# PrescriptionHeader model endpoints #####################
#post endpoints
def add_prescription_header():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate required fields
        if not data or 'patient_id' not in data or 'prescriber_id' not in data:
            return jsonify({'error': 'Missing required fields: patient_id, prescriber_id'}), 400

        # Validate the patient_id and prescriber_id
        patient = Patient.query.get(data['patient_id'])
        prescriber = Prescriber.query.get(data['prescriber_id'])
        if not patient:
            return jsonify({'error': 'Patient with the given ID does not exist'}), 404
        if not prescriber:
            return jsonify({'error': 'Prescriber with the given ID does not exist'}), 404

        # Create a new PrescriptionHeader instance
        new_prescription_header = PrescriptionHeader(
            patient_id=data['patient_id'],
            prescriber_id=data['prescriber_id'],
            created=datetime.utcnow(),
            updated=datetime.utcnow(),
            created_by=data.get('created_by', None),
            updated_by=data.get('updated_by', None)
        )

        # Add and commit the record
        db.session.add(new_prescription_header)
        db.session.commit()

        # Return the created prescription header
        return jsonify({
            'id': new_prescription_header.id,
            'patient_id': new_prescription_header.patient_id,
            'prescriber_id': new_prescription_header.prescriber_id,
            'created': new_prescription_header.created.isoformat(),
            'updated': new_prescription_header.updated.isoformat(),
            'created_by': new_prescription_header.created_by,
            'updated_by': new_prescription_header.updated_by
        }), 201

    except Exception as e:
        return jsonify({'error': 'An error occurred while creating the prescription header', 'details': str(e)}), 500
    

####get prescription headers#######

def get_all_prescription_headers():
    try:
        # Query all prescription headers
        prescription_headers = PrescriptionHeader.query.all()

        # Serialize the data
        header_list = [
            {
                'id': header.id,
                'patient_id': header.patient_id,
                'prescriber_id': header.prescriber_id,
                'created': header.created.isoformat(),
                'updated': header.updated.isoformat(),
                'created_by': header.created_by,
                'updated_by': header.updated_by
            }
            for header in prescription_headers
        ]

        return jsonify(header_list), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching prescription headers', 'details': str(e)}), 500


#Get a Specific PrescriptionHeader by ID

def get_prescription_header_by_id(id):
    try:
        # Query the prescription header by ID
        header = PrescriptionHeader.query.get(id)

        # If the header does not exist, return a 404 error
        if not header:
            return jsonify({'error': 'Prescription header not found'}), 404

        # Serialize the data
        return jsonify({
            'id': header.id,
            'patient_id': header.patient_id,
            'prescriber_id': header.prescriber_id,
            'created': header.created.isoformat(),
            'updated': header.updated.isoformat(),
            'created_by': header.created_by,
            'updated_by': header.updated_by
        }), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching the prescription header', 'details': str(e)}), 500

#Update a PrescriptionHeader

def update_prescription_header(id):
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Fetch the prescription header by ID
        header = PrescriptionHeader.query.get(id)
        if not header:
            return jsonify({'error': 'Prescription header not found'}), 404

        # Update fields if provided
        if 'patient_id' in data:
            # Validate the patient_id
            patient = Patient.query.get(data['patient_id'])
            if not patient:
                return jsonify({'error': 'Patient with the given ID does not exist'}), 404
            header.patient_id = data['patient_id']
        if 'prescriber_id' in data:
            # Validate the prescriber_id
            prescriber = Prescriber.query.get(data['prescriber_id'])
            if not prescriber:
                return jsonify({'error': 'Prescriber with the given ID does not exist'}), 404
            header.prescriber_id = data['prescriber_id']
        if 'updated_by' in data:
            header.updated_by = data['updated_by']

        # Update the `updated` timestamp
        header.updated = datetime.utcnow()

        # Commit the changes
        db.session.commit()

        # Return the updated record
        return jsonify({
            'id': header.id,
            'patient_id': header.patient_id,
            'prescriber_id': header.prescriber_id,
            'created': header.created.isoformat(),
            'updated': header.updated.isoformat(),
            'created_by': header.created_by,
            'updated_by': header.updated_by
        }), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while updating the prescription header', 'details': str(e)}), 500
    
#Remove a PrescriptionHeader

def delete_prescription_header(id):
    try:
        # Fetch the prescription header by ID
        header = PrescriptionHeader.query.get(id)

        # If the header does not exist, return a 404 error
        if not header:
            return jsonify({'error': 'Prescription header not found'}), 404

        # Delete the record
        db.session.delete(header)
        db.session.commit()

        # Return a success message
        return jsonify({'message': f'Prescription header with ID {id} has been deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while deleting the prescription header', 'details': str(e)}), 500


################################ Prescription Line model endpoints ##################################

#Post endpoints Prescription Line model 

def add_prescription_line():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate required fields
        required_fields = ['product_id', 'prescription_id', 'quantity', 'price']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Missing required fields: {", ".join(required_fields)}'}), 400

        # Validate product_id and prescription_id
        product = Product.query.get(data['product_id'])
        prescription = PrescriptionHeader.query.get(data['prescription_id'])
        if not product:
            return jsonify({'error': 'Product with the given ID does not exist'}), 404
        if not prescription:
            return jsonify({'error': 'Prescription header with the given ID does not exist'}), 404

        # Create a new PrescriptionLines instance
        new_line = PrescriptionLines(
            product_id=data['product_id'],
            prescription_id=data['prescription_id'],
            quantity=data['quantity'],
            price=data['price'],
            directions=data.get('directions', None),
            created=datetime.utcnow(),
            updated=datetime.utcnow(),
            created_by=data.get('created_by', None),
            updated_by=data.get('updated_by', None)
        )

        # Add and commit the record
        db.session.add(new_line)
        db.session.commit()

        # Return the created prescription line
        return jsonify({
            'id': new_line.id,
            'product_id': new_line.product_id,
            'prescription_id': new_line.prescription_id,
            'quantity': new_line.quantity,
            'price': str(new_line.price),
            'directions': new_line.directions,
            'created': new_line.created.isoformat(),
            'updated': new_line.updated.isoformat(),
            'created_by': new_line.created_by,
            'updated_by': new_line.updated_by
        }), 201

    except Exception as e:
        return jsonify({'error': 'An error occurred while creating the prescription line', 'details': str(e)}), 500
    

#Get endpoints prescription-lines
def get_all_prescription_lines():
    try:
        # Query all prescription lines
        prescription_lines = PrescriptionLines.query.all()

        # Serialize the data
        lines_list = [
            {
                'id': line.id,
                'product_id': line.product_id,
                'prescription_id': line.prescription_id,
                'quantity': line.quantity,
                'price': str(line.price),
                'directions': line.directions,
                'created': line.created.isoformat(),
                'updated': line.updated.isoformat(),
                'created_by': line.created_by,
                'updated_by': line.updated_by
            }
            for line in prescription_lines
        ]

        return jsonify(lines_list), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching prescription lines', 'details': str(e)}), 500
    

#Get a Specific Prescription Line by ID
def get_prescription_line_by_id(id):
    try:
        # Query the prescription line by ID
        line = PrescriptionLines.query.get(id)

        # If the line does not exist, return a 404 error
        if not line:
            return jsonify({'error': 'Prescription line not found'}), 404

        # Serialize the data
        return jsonify({
            'id': line.id,
            'product_id': line.product_id,
            'prescription_id': line.prescription_id,
            'quantity': line.quantity,
            'price': str(line.price),
            'directions': line.directions,
            'created': line.created.isoformat(),
            'updated': line.updated.isoformat(),
            'created_by': line.created_by,
            'updated_by': line.updated_by
        }), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching the prescription line', 'details': str(e)}), 500
    

#Update a Prescription Line
def update_prescription_line(id):
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Fetch the prescription line by ID
        line = PrescriptionLines.query.get(id)
        if not line:
            return jsonify({'error': 'Prescription line not found'}), 404

        # Update fields if provided
        if 'product_id' in data:
            product = Product.query.get(data['product_id'])
            if not product:
                return jsonify({'error': 'Product with the given ID does not exist'}), 404
            line.product_id = data['product_id']
        if 'prescription_id' in data:
            prescription = PrescriptionHeader.query.get(data['prescription_id'])
            if not prescription:
                return jsonify({'error': 'Prescription header with the given ID does not exist'}), 404
            line.prescription_id = data['prescription_id']
        if 'quantity' in data:
            line.quantity = data['quantity']
        if 'price' in data:
            line.price = data['price']
        if 'directions' in data:
            line.directions = data['directions']
        if 'updated_by' in data:
            line.updated_by = data['updated_by']

        # Update the `updated` timestamp
        line.updated = datetime.utcnow()

        # Commit the changes
        db.session.commit()

        # Return the updated record
        return jsonify({
            'id': line.id,
            'product_id': line.product_id,
            'prescription_id': line.prescription_id,
            'quantity': line.quantity,
            'price': str(line.price),
            'directions': line.directions,
            'created': line.created.isoformat(),
            'updated': line.updated.isoformat(),
            'created_by': line.created_by,
            'updated_by': line.updated_by
        }), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while updating the prescription line', 'details': str(e)}), 500
    

#Remove a Prescription Line


def delete_prescription_line(id):
    try:
        # Fetch the prescription line by ID
        line = PrescriptionLines.query.get(id)

        # If the line does not exist, return a 404 error
        if not line:
            return jsonify({'error': 'Prescription line not found'}), 404

        # Delete the record
        db.session.delete(line)
        db.session.commit()

        # Return a success message
        return jsonify({'message': f'Prescription line with ID {id} has been deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while deleting the prescription line', 'details': str(e)}), 500




