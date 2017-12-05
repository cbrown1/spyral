function f = erb2hz(e);
tmp = exp((e-43) / 11.17);
f = (0.312 - 14.675*tmp) / (tmp - 1.0)*1000;
if f <= 0
    f = 1;
end