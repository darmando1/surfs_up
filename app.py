{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "aac7f902",
   "metadata": {},
   "outputs": [],
   "source": [
    "import datetime as dt\n",
    "import numpy as np\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "cf667852",
   "metadata": {},
   "outputs": [],
   "source": [
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "bcfd9f5f",
   "metadata": {},
   "outputs": [],
   "source": [
    "from flask import Flask, jsonify"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "559f5007",
   "metadata": {},
   "outputs": [],
   "source": [
    "engine = create_engine(\"sqlite:///hawaii.sqlite\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "b8dcc58e",
   "metadata": {},
   "outputs": [],
   "source": [
    "Base = automap_base()\n",
    "Base.prepare(engine, reflect=True)\n",
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station\n",
    "session = Session(engine)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f9282531",
   "metadata": {},
   "outputs": [],
   "source": [
    "app = Flask(__name__)\n",
    "import app\n",
    "\n",
    "print(\"example __name__ = %s\", __name__)\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    print(\"example is being run directly.\")\n",
    "else:\n",
    "    print(\"example is being imported\")\n",
    "\n",
    "@app.route(\"/\")\n",
    "def welcome():\n",
    "    return(\n",
    "    '''\n",
    "    Welcome to the Climate Analysis API!\n",
    "    Available Routes:\n",
    "    /api/v1.0/precipitation\n",
    "    /api/v1.0/stations\n",
    "    /api/v1.0/tobs\n",
    "    /api/v1.0/temp/start/end\n",
    "    ''')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5a868a10",
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "def precipitation():\n",
    "   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)\n",
    "   precipitation = session.query(Measurement.date, Measurement.prcp).\\\n",
    "    filter(Measurement.date >= prev_year).all()\n",
    "   precip = {date: prcp for date, prcp in precipitation}\n",
    "   return jsonify(precip)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6be7103c",
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/stations\")\n",
    "def stations():\n",
    "    results = session.query(Station.station).all()\n",
    "    stations = list(np.ravel(results))\n",
    "    return jsonify(stations=stations)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "bdad6777",
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/tobs\")\n",
    "def temp_monthly():\n",
    "    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)\n",
    "    results = session.query(Measurement.tobs).\\\n",
    "      filter(Measurement.station == 'USC00519281').\\\n",
    "      filter(Measurement.date >= prev_year).all()\n",
    "    temps = list(np.ravel(results))\n",
    "    return jsonify(temps=temps)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7173b71a",
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/temp/<start>\")\n",
    "@app.route(\"/api/v1.0/temp/<start>/<end>\")\n",
    "def stats(start=None, end=None):\n",
    "    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]\n",
    "\n",
    "    if not end:\n",
    "        results = session.query(*sel).\\\n",
    "            filter(Measurement.date >= start).all()\n",
    "        temps = list(np.ravel(results))\n",
    "        return jsonify(temps)\n",
    "\n",
    "    results = session.query(*sel).\\\n",
    "        filter(Measurement.date >= start).\\\n",
    "        filter(Measurement.date <= end).all()\n",
    "    temps = list(np.ravel(results))\n",
    "    return jsonify(temps)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
