from flask import Flask, render_template, request
import qrcode
import io
import base64

app = Flask(__name__, template_folder='templates', static_folder='static')

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert the PIL image to a byte buffer
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")

    # Encode the image as a base64 string
    img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    # Create the data URI
    data_uri = f"data:image/png;base64,{img_str}"

    return data_uri

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get data from the form
        name = request.form.get("name")
        phone = request.form.get("phone")
        address = request.form.get("address")
        
        # Combine data into a string
        user_data = f"Name: {name}\nPhone: {phone}\nAddress: {address}"

        # Generate the QR code data URI
        qr_code_uri = generate_qr_code(user_data)
        
        # Render the result page with the QR code URI
        return render_template("result.html", user_data=user_data, qr_code_uri=qr_code_uri)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
