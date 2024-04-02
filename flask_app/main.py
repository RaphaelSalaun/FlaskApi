from typing import Union
import os
from sqlalchemy import func
from flask import Flask, request, abort
import xml.etree.ElementTree as ET
from models import db, Files, Prices


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRES_URI")

db.init_app(app)


@app.get("/started")
@app.get("/")
def read_root():
    return "True"


@app.get("/uploader_form")
def html_form():
    """
    Helper endpoint to provide a simple HTML form
    to upload and test XML files
    """

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="upload" method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/upload', methods=['POST'])
def receive_file():
    """
    Main function where we upload XML files.
    We check if the file's filename is blank, if the file has the xml extension
    We insert a line in database to say we have started a file processing

    After we pass through the file content to our XML library,
    using a generator to iterate through the file so we can manage large files
    We insert prices periodically in database by chunks of 1000
    We finally update file status to True meaning we processed it entirely
    and return it's file_id to query in our other endpoint
    """
    file = request.files['file']

    if file.filename == '':
        return abort(code=404,
                     description="Filename is not set, aborting")

    if file.filename[-4:] != '.xml':
        return abort(code=404,
                     description="File doesn't seem to be XML, aborting")

    file_stream = file.stream

    try:
        insert_file_query = db.insert(Files).values({
            "filename": file.filename,
            "status": False
        }).returning(Files.id)
        file_id = db.session.execute(insert_file_query).first()[0]
        db.session.commit()

        prices = []

        for event, element in ET.iterparse(file_stream):
            # we only care about prices, disregard other XML elements
            if element.tag != 'prix':
                continue

            gas_type = element.get("nom")
            gas_price = float(element.get("valeur"))

            if gas_type and gas_price:

                prices.append(
                    {
                        "gas_type": gas_type,
                        "gas_price": gas_price,
                        "file_id": file_id
                    }
                )

            if len(prices) % 1000 == 0:
                query = db.insert(Prices).values(
                    prices
                )
                db.session.execute(query)
                db.session.commit()

                prices = []

        query = db.insert(Prices).values(
            prices
        )
        db.session.execute(query)
        db.session.commit()

        validate_file_id = db.update(Files).values({
            "status": True
        }).where(Files.id == file_id)

        db.session.execute(validate_file_id)
        db.session.commit()

    except ET.ParseError:
        return abort(code=500,
                     description="Couldn't parse your XML file, \
                                    check for formatting errors")

    except Exception as e:
        return abort(code=500,
                     description=f"Server error processing your file : {str(e)}")

    return {
        "message": f"File {file.filename} correctly processed",
        "file_id": file_id
    }


@app.route('/mean_price', methods=['GET'])
@app.route('/mean_price/<file_id>', methods=['GET'])
def mean_price(file_id: Union[int, None] = None):
    """
    Endpoint to give the average price of all prices received
    in all files received when file_id is empty;
    otherwise give the average for the file specified
    """

    if file_id is None:
        general_average_query = db.select(
            Prices.gas_type,
            func.avg(Prices.gas_price)
        ).group_by(Prices.gas_type)

        general_mean_price = db.session.execute(general_average_query).all()

        return {k: round(v, 3) for k, v in general_mean_price}

    get_mean_prices_query = db.select(
        Prices.gas_type,
        func.avg(Prices.gas_price)
    ).where(Prices.file_id == file_id).group_by(Prices.gas_type)

    file_mean_prices = db.session.execute(get_mean_prices_query).all()

    return {
        **{"file_id": file_id},
        **{k: round(v, 3) for k, v in file_mean_prices}
    }


if __name__ == '__main__':

    app.run(debug=True)
