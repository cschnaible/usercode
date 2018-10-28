#!/bin/bash

for model in {B-L,Q,T3L,PSI,SSM}
do
    python PlotZPrimeMassesTogether.py -in 20181026 -out 20181026 -zp $model 
done
