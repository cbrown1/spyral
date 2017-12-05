function e = hz2erb(f);
fkHz = f/1000;
e = 11.17*log((fkHz + 0.312) / (fkHz + 14.675))+43;
if e <= 0
    e = 0.1;
end