#!/bin/bash
#IN=inCMS_20181030
IN=nevents_request_alt_20181108
OUT=nevents_request_alt_150bw_20181108

#for model in {B-L,Q,T3L,PSI,SSM}
#do
#    python PlotZPrimeMassesTogether.py -in $IN -out $OUT -zp $model 
#done

python PlotZPrimeMassesTogether.py -in $IN -out $OUT -zp Q
