#!/bin/bash
IN=inCMS_20181030
OUT=inCMS_20181102
python PlotPDFsTogether.py -in $IN -out $OUT -zp B-L -m 4000
python PlotPDFsTogether.py -in $IN -out $OUT -zp B-L -m 6000
python PlotPDFsTogether.py -in $IN -out $OUT -zp SSM -m 6000
python PlotPDFsTogether.py -in $IN -out $OUT -zp T3L -m 6000
python PlotPDFsTogether.py -in $IN -out $OUT -zp Q -m 6000
python PlotPDFsTogether.py -in $IN -out $OUT -zp Q -m 9000
